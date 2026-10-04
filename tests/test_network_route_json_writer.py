import json

from wrgd.io import write_network_route_json
from wrgd.models.difficulty import DifficultyLevel
from wrgd.models.network_path_summary import NetworkPathSummary
from wrgd.models.network_route_analysis import NetworkRouteAnalysis
from wrgd.models.road_statistics import RoadStatistics


def test_write_network_route_json(tmp_path) -> None:
    output = tmp_path / "network-route.json"
    analysis = NetworkRouteAnalysis(
        summary=NetworkPathSummary(
            distance=1250.0,
            edge_count=3,
            bridge_count=1,
            tunnel_count=2,
            road_type_counts={"primary": 2, "residential": 1},
        ),
        statistics=RoadStatistics(
            distance=1248.0,
            ascent=30.0,
            descent=12.0,
            highest_elevation=130.0,
            lowest_elevation=100.0,
            max_gradient=5.0,
            average_gradient=1.5,
            average_curvature=0.02,
            max_curvature=0.05,
            min_radius=20.0,
            average_radius=50.0,
            sharp_curve_count=1,
        ),
    )
    difficulty = DifficultyLevel(level=2, name="易しい", score=18.0)

    write_network_route_json(
        analysis,
        output,
        difficulty=difficulty,
        score=18.0,
    )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["summary"] == {
        "distance": 1250.0,
        "edge_count": 3,
        "bridge_count": 1,
        "tunnel_count": 2,
        "road_type_counts": {"primary": 2, "residential": 1},
    }
    assert data["statistics"]["distance"] == 1248.0
    assert data["statistics"]["average_curvature"] == 0.02
    assert data["statistics"]["max_curvature"] == 0.05
    assert data["statistics"]["min_radius"] == 20.0
    assert data["statistics"]["average_radius"] == 50.0
    assert data["statistics"]["sharp_curve_count"] == 1
    assert data["statistics"]["difficulty"] == {"level": 2, "name": "易しい"}
    assert data["statistics"]["score"] == 18.0
