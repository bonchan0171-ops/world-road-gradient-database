import pytest

from wrgd.analysis.difficulty import calculate_difficulty
from wrgd.analysis.score import calculate_score
from wrgd.io.dem_loader import DEMLoader
from wrgd.models.coordinate import Coordinate
from wrgd.models.difficulty import DifficultyLevel
from wrgd.models.network_edge import NetworkEdge
from wrgd.models.network_node import NetworkNode
from wrgd.models.network_path import NetworkPath
from wrgd.network import RoadNetwork


class FakeDEMLoader:
    """Test double for the existing DEMLoader interface."""

    def __init__(self, elevations: dict[tuple[float, float], float]) -> None:
        self.elevations = elevations

    def get_elevation(self, lat: float, lon: float) -> float:
        try:
            return self.elevations[(lat, lon)]
        except KeyError as error:
            raise ValueError("Elevation is unavailable.") from error


def create_network(
    distance: float = 100.0,
) -> tuple[RoadNetwork, NetworkNode, NetworkNode]:
    """Create a two-node network for elevation tests."""
    start_node = NetworkNode(1, 35.0, 139.0, None)
    end_node = NetworkNode(2, 35.001, 139.002, None)
    network = RoadNetwork()
    network.add_node(start_node)
    network.add_node(end_node)
    network.add_edge(
        NetworkEdge(
            id=1,
            start_node=start_node,
            end_node=end_node,
            distance=distance,
            average_gradient=99.0,
            road_type="primary",
            oneway=False,
            geometry=[],
        )
    )
    return network, start_node, end_node


def test_apply_elevation_uses_dem_loader() -> None:
    """DEMLoader からノード標高を取得する。"""
    loader = DEMLoader("tests/data/sample_dem.tif")
    loader.load()
    start_node = NetworkNode(1, 35.7700, 139.7250, None)
    network = RoadNetwork()
    network.add_node(start_node)

    network.apply_elevation(loader)

    assert start_node.elevation == loader.get_elevation(35.7700, 139.7250)


def test_apply_elevation_sets_multiple_nodes_and_gradient() -> None:
    """複数ノードの標高とEdge勾配を設定する。"""
    network, start_node, end_node = create_network()
    loader = FakeDEMLoader(
        {
            (start_node.latitude, start_node.longitude): 100.0,
            (end_node.latitude, end_node.longitude): 110.0,
        }
    )

    network.apply_elevation(loader)  # type: ignore[arg-type]

    assert start_node.elevation == 100.0
    assert end_node.elevation == 110.0
    assert network.get_edge(1).average_gradient == 10.0


def test_apply_elevation_handles_unavailable_elevation() -> None:
    """標高を取得できない場合は標高と勾配を安全に初期化する。"""
    network, start_node, end_node = create_network()
    loader = FakeDEMLoader({(start_node.latitude, start_node.longitude): 100.0})

    network.apply_elevation(loader)  # type: ignore[arg-type]

    assert start_node.elevation == 100.0
    assert end_node.elevation is None
    assert network.get_edge(1).average_gradient == 0.0


def test_apply_elevation_without_dem_clears_values() -> None:
    """DEM未指定の場合は標高をNone、勾配を0にする。"""
    network, start_node, end_node = create_network()
    start_node.elevation = 100.0
    end_node.elevation = 110.0

    network.apply_elevation()

    assert start_node.elevation is None
    assert end_node.elevation is None
    assert network.get_edge(1).average_gradient == 0.0


def test_apply_elevation_handles_zero_distance() -> None:
    """距離が0の場合は勾配を0にする。"""
    network, start_node, end_node = create_network(distance=0.0)
    loader = FakeDEMLoader(
        {
            (start_node.latitude, start_node.longitude): 100.0,
            (end_node.latitude, end_node.longitude): 110.0,
        }
    )

    network.apply_elevation(loader)  # type: ignore[arg-type]

    assert network.get_edge(1).average_gradient == 0.0


def add_network_edge(
    network: RoadNetwork,
    edge_id: int,
    start_node: NetworkNode,
    end_node: NetworkNode,
    distance: float,
    oneway: bool = False,
    geometry: list[Coordinate] | None = None,
) -> None:
    """Add a test edge to a network."""
    network.add_edge(
        NetworkEdge(
            id=edge_id,
            start_node=start_node,
            end_node=end_node,
            distance=distance,
            average_gradient=0.0,
            road_type="residential",
            oneway=oneway,
            geometry=geometry or [],
        )
    )


def create_path_network(node_count: int) -> tuple[RoadNetwork, list[NetworkNode]]:
    """Create numbered nodes for shortest path tests."""
    network = RoadNetwork()
    nodes = [NetworkNode(index, 35.0, 139.0, None) for index in range(node_count)]
    for node in nodes:
        network.add_node(node)
    return network, nodes


def test_shortest_path_on_a_straight_graph() -> None:
    """単純な直線グラフの最短経路を返す。"""
    network, nodes = create_path_network(3)
    add_network_edge(network, 1, nodes[0], nodes[1], 10.0)
    add_network_edge(network, 2, nodes[1], nodes[2], 20.0)

    assert network.shortest_path(0, 2) == [0, 1, 2]


def test_shortest_path_selects_the_shorter_route() -> None:
    """複数経路では距離の短い経路を選択する。"""
    network, nodes = create_path_network(4)
    add_network_edge(network, 1, nodes[0], nodes[1], 10.0)
    add_network_edge(network, 2, nodes[1], nodes[3], 10.0)
    add_network_edge(network, 3, nodes[0], nodes[2], 3.0)
    add_network_edge(network, 4, nodes[2], nodes[3], 4.0)

    assert network.shortest_path(0, 3) == [0, 2, 3]


def test_shortest_path_respects_oneway_edges() -> None:
    """oneway Edge の逆方向を経路探索に使用しない。"""
    network, nodes = create_path_network(2)
    add_network_edge(network, 1, nodes[0], nodes[1], 10.0, oneway=True)

    assert network.shortest_path(0, 1) == [0, 1]
    assert network.shortest_path(1, 0) is None


def test_shortest_path_returns_none_when_unreachable() -> None:
    """到達不能なNodeには None を返す。"""
    network, nodes = create_path_network(2)

    assert network.shortest_path(nodes[0].id, nodes[1].id) is None


def test_shortest_path_returns_start_for_same_node() -> None:
    """開始Nodeと終点Nodeが同じ場合は自身だけを返す。"""
    network, _ = create_path_network(1)

    assert network.shortest_path(0, 0) == [0]


def test_shortest_path_raises_key_error_for_unknown_node() -> None:
    """存在しないNode IDには既存APIと同じ KeyError を返す。"""
    network, _ = create_path_network(1)

    with pytest.raises(KeyError):
        network.shortest_path(0, 99)


def test_shortest_route_contains_nodes_edges_and_distance() -> None:
    """NetworkPathにNode列、Edge列、合計距離を設定する。"""
    network, nodes = create_path_network(3)
    add_network_edge(network, 10, nodes[0], nodes[1], 12.5)
    add_network_edge(network, 20, nodes[1], nodes[2], 7.5)

    route = network.shortest_route(0, 2)

    assert route is not None
    assert route.node_ids == [0, 1, 2]
    assert route.edge_ids == [10, 20]
    assert route.distance == 20.0


def test_shortest_route_selects_matching_shortest_edges() -> None:
    """NetworkPathは距離の短い経路に対応するEdgeを返す。"""
    network, nodes = create_path_network(4)
    add_network_edge(network, 10, nodes[0], nodes[1], 10.0)
    add_network_edge(network, 20, nodes[1], nodes[3], 10.0)
    add_network_edge(network, 30, nodes[0], nodes[2], 3.0)
    add_network_edge(network, 40, nodes[2], nodes[3], 4.0)

    route = network.shortest_route(0, 3)

    assert route is not None
    assert route.node_ids == [0, 2, 3]
    assert route.edge_ids == [30, 40]
    assert route.distance == 7.0


def test_shortest_route_respects_oneway_edges() -> None:
    """NetworkPathもoneway Edgeの方向制約を尊重する。"""
    network, nodes = create_path_network(2)
    add_network_edge(network, 10, nodes[0], nodes[1], 10.0, oneway=True)

    route = network.shortest_route(0, 1)

    assert route is not None
    assert route.node_ids == [0, 1]
    assert route.edge_ids == [10]
    assert network.shortest_route(1, 0) is None


def test_shortest_route_returns_none_when_unreachable() -> None:
    """到達不能な場合はNetworkPathを返さない。"""
    network, nodes = create_path_network(2)

    assert network.shortest_route(nodes[0].id, nodes[1].id) is None


def test_shortest_route_returns_empty_edges_for_same_node() -> None:
    """同一NodeのNetworkPathはNode自身と距離0を返す。"""
    network, _ = create_path_network(1)

    route = network.shortest_route(0, 0)

    assert route is not None
    assert route.node_ids == [0]
    assert route.edge_ids == []
    assert route.distance == 0.0


def test_shortest_route_raises_key_error_for_unknown_node() -> None:
    """存在しないNode IDにはKeyErrorを返す。"""
    network, _ = create_path_network(1)

    with pytest.raises(KeyError):
        network.shortest_route(0, 99)


def test_calculate_statistics_from_network_path() -> None:
    """NetworkPathからRoadStatisticsを生成する。"""
    network, nodes = create_path_network(4)
    for node, elevation in zip(nodes, [100.0, 120.0, 110.0, 140.0]):
        node.elevation = elevation

    add_network_edge(network, 10, nodes[0], nodes[1], 100.0)
    add_network_edge(network, 20, nodes[1], nodes[2], 100.0)
    add_network_edge(network, 30, nodes[2], nodes[3], 100.0)
    network.get_edge(10).average_gradient = 20.0
    network.get_edge(20).average_gradient = -10.0
    network.get_edge(30).average_gradient = 30.0

    statistics = network.calculate_statistics(
        NetworkPath(
            node_ids=[0, 1, 2, 3],
            edge_ids=[10, 20, 30],
            distance=300.0,
        )
    )

    assert statistics.distance == 300.0
    assert statistics.ascent == 50.0
    assert statistics.descent == 10.0
    assert statistics.highest_elevation == 140.0
    assert statistics.lowest_elevation == 100.0
    assert statistics.max_gradient == 30.0
    assert statistics.average_gradient == pytest.approx(13.3333333333)


def test_calculate_statistics_handles_missing_elevation() -> None:
    """標高がNoneの場合は上昇下降と標高統計を安全に処理する。"""
    network, nodes = create_path_network(3)
    nodes[1].elevation = 120.0
    add_network_edge(network, 10, nodes[0], nodes[1], 0.0)
    add_network_edge(network, 20, nodes[1], nodes[2], 100.0)
    network.get_edge(10).average_gradient = 0.0
    network.get_edge(20).average_gradient = 5.0

    statistics = network.calculate_statistics(
        NetworkPath(
            node_ids=[0, 1, 2],
            edge_ids=[10, 20],
            distance=100.0,
        )
    )

    assert statistics.distance == 100.0
    assert statistics.ascent == 0.0
    assert statistics.descent == 0.0
    assert statistics.highest_elevation == 120.0
    assert statistics.lowest_elevation == 120.0
    assert statistics.max_gradient == 5.0
    assert statistics.average_gradient == 2.5


def test_network_path_statistics_integrate_with_difficulty_and_score() -> None:
    """NetworkPathの統計を既存Difficulty/Score APIへ渡せる。"""
    network, nodes = create_path_network(2)
    nodes[0].elevation = 100.0
    nodes[1].elevation = 150.0
    add_network_edge(network, 10, nodes[0], nodes[1], 1000.0)
    network.get_edge(10).average_gradient = 2.0

    path = NetworkPath(
        node_ids=[0, 1],
        edge_ids=[10],
        distance=1000.0,
    )
    statistics = network.calculate_statistics(path)
    difficulty = calculate_difficulty(statistics)
    score = calculate_score(statistics)

    assert difficulty == DifficultyLevel(
        level=1,
        name="非常に易しい",
        score=0.8,
    )
    assert isinstance(score, float)
    assert score == 8.0


def test_path_coordinates_from_one_edge() -> None:
    """1つのEdgeのgeometryからCoordinate列を生成する。"""
    network, nodes = create_path_network(2)
    geometry = [
        Coordinate(35.0, 139.0),
        Coordinate(35.001, 139.001),
        Coordinate(35.002, 139.002),
    ]
    add_network_edge(network, 10, nodes[0], nodes[1], 100.0, geometry=geometry)

    result = network.path_coordinates(NetworkPath([0, 1], [10], 100.0))

    assert result == geometry


def test_path_coordinates_combines_edges_without_duplicate_connection() -> None:
    """複数Edgeを接続点の重複なしで連結する。"""
    network, nodes = create_path_network(3)
    point_a = Coordinate(35.0, 139.0)
    point_b = Coordinate(35.001, 139.001)
    point_c = Coordinate(35.002, 139.002)
    add_network_edge(
        network, 10, nodes[0], nodes[1], 100.0, geometry=[point_a, point_b]
    )
    add_network_edge(
        network, 20, nodes[1], nodes[2], 100.0, geometry=[point_b, point_c]
    )

    result = network.path_coordinates(NetworkPath([0, 1, 2], [10, 20], 200.0))

    assert result == [point_a, point_b, point_c]


def test_path_coordinates_reverses_edge_geometry() -> None:
    """経路がEdgeの定義方向と逆の場合はgeometryを反転する。"""
    network, nodes = create_path_network(2)
    point_a = Coordinate(35.0, 139.0)
    point_b = Coordinate(35.001, 139.001)
    point_mid = Coordinate(35.0005, 139.0005)
    add_network_edge(
        network,
        10,
        nodes[0],
        nodes[1],
        100.0,
        geometry=[point_a, point_mid, point_b],
    )

    result = network.path_coordinates(NetworkPath([1, 0], [10], 100.0))

    assert result == [point_b, point_mid, point_a]


def test_path_coordinates_combines_forward_and_reverse_edges() -> None:
    """正方向と逆方向のEdgeを組み合わせて連結する。"""
    network, nodes = create_path_network(3)
    point_a = Coordinate(35.0, 139.0)
    point_b = Coordinate(35.001, 139.001)
    point_c = Coordinate(35.002, 139.002)
    add_network_edge(
        network, 10, nodes[0], nodes[1], 100.0, geometry=[point_a, point_b]
    )
    add_network_edge(
        network, 20, nodes[2], nodes[1], 100.0, geometry=[point_c, point_b]
    )

    result = network.path_coordinates(NetworkPath([0, 1, 2], [10, 20], 200.0))

    assert result == [point_a, point_b, point_c]


def test_path_coordinates_skips_empty_geometry() -> None:
    """空geometryのEdgeを安全に処理する。"""
    network, nodes = create_path_network(2)
    add_network_edge(network, 10, nodes[0], nodes[1], 100.0, geometry=[])

    result = network.path_coordinates(NetworkPath([0, 1], [10], 100.0))

    assert result == []
