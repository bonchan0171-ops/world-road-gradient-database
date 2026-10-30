import pytest

from wrgd.models.coordinate import Coordinate
from wrgd.models.network_edge import NetworkEdge
from wrgd.models.network_node import NetworkNode
from wrgd.models.road_network_topology_summary import RoadNetworkTopologySummary
from wrgd.network import RoadNetwork, analyze_network_topology


def create_network(node_ids: list[int]) -> RoadNetwork:
    network = RoadNetwork()
    for node_id in node_ids:
        network.add_node(NetworkNode(node_id, 35.0, 139.0, None))
    return network


def add_edge(
    network: RoadNetwork,
    edge_id: int,
    start_node_id: int,
    end_node_id: int,
    *,
    oneway: bool = False,
) -> None:
    start_node = NetworkNode(start_node_id, 35.0, 139.0, None)
    end_node = NetworkNode(end_node_id, 35.0, 139.0, None)
    network.add_edge(
        NetworkEdge(
            id=edge_id,
            start_node=start_node,
            end_node=end_node,
            distance=1.0,
            average_gradient=0.0,
            road_type="residential",
            oneway=oneway,
            geometry=[Coordinate(35.0, 139.0), Coordinate(35.0, 139.0)],
        )
    )


def test_analyze_empty_network() -> None:
    summary = analyze_network_topology(RoadNetwork())

    assert summary == RoadNetworkTopologySummary(
        node_count=0,
        edge_count=0,
        component_count=0,
        node_degrees={},
        isolated_node_ids=[],
        dead_end_node_ids=[],
        intersection_node_ids=[],
        connected_components=[],
    )


def test_analyze_multiple_nodes_without_edges() -> None:
    summary = analyze_network_topology(create_network([9, 1, 4]))

    assert summary.node_degrees == {1: 0, 4: 0, 9: 0}
    assert summary.isolated_node_ids == [1, 4, 9]
    assert summary.connected_components == [[1], [4], [9]]
    assert summary.component_count == 3


def test_analyze_three_node_chain_and_ignores_oneway() -> None:
    network = create_network([3, 1, 2])
    add_edge(network, 20, 2, 3, oneway=True)
    add_edge(network, 10, 1, 2)

    summary = analyze_network_topology(network)

    assert summary.node_degrees == {1: 1, 2: 2, 3: 1}
    assert summary.dead_end_node_ids == [1, 3]
    assert summary.intersection_node_ids == []
    assert summary.connected_components == [[1, 2, 3]]


def test_analyze_t_junction() -> None:
    network = create_network([7, 5, 1, 3])
    add_edge(network, 1, 5, 1)
    add_edge(network, 2, 5, 3)
    add_edge(network, 3, 5, 7)

    summary = analyze_network_topology(network)

    assert summary.node_degrees == {1: 1, 3: 1, 5: 3, 7: 1}
    assert summary.dead_end_node_ids == [1, 3, 7]
    assert summary.intersection_node_ids == [5]
    assert summary.connected_components == [[1, 3, 5, 7]]


def test_analyze_multiple_components_and_stable_order() -> None:
    network = create_network([9, 7, 5, 3, 1])
    add_edge(network, 4, 7, 5)
    add_edge(network, 2, 3, 1)

    summary = analyze_network_topology(network)

    assert summary.node_degrees == {1: 1, 3: 1, 5: 1, 7: 1, 9: 0}
    assert summary.isolated_node_ids == [9]
    assert summary.dead_end_node_ids == [1, 3, 5, 7]
    assert summary.connected_components == [[1, 3], [5, 7], [9]]
    assert summary.component_count == 3


def test_parallel_edges_each_increase_degree() -> None:
    network = create_network([2, 1])
    add_edge(network, 1, 1, 2)
    add_edge(network, 2, 1, 2, oneway=True)

    summary = analyze_network_topology(network)

    assert summary.node_degrees == {1: 2, 2: 2}
    assert summary.dead_end_node_ids == []
    assert summary.connected_components == [[1, 2]]


def test_self_loop_increases_degree_by_two() -> None:
    network = create_network([8])
    add_edge(network, 10, 8, 8)

    summary = analyze_network_topology(network)

    assert summary.node_degrees == {8: 2}
    assert summary.isolated_node_ids == []
    assert summary.dead_end_node_ids == []
    assert summary.connected_components == [[8]]


@pytest.mark.parametrize(
    ("start_node_id", "end_node_id", "missing_node_id"),
    [(1, 99, 99), (98, 1, 98)],
)
def test_edge_with_unregistered_endpoint_raises_value_error(
    start_node_id: int,
    end_node_id: int,
    missing_node_id: int,
) -> None:
    network = create_network([1])
    add_edge(network, 42, start_node_id, end_node_id)

    with pytest.raises(ValueError, match=rf"Edge 42.*node {missing_node_id}"):
        analyze_network_topology(network)
