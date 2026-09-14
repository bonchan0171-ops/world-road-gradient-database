from wrgd.models.coordinate import Coordinate
from wrgd.network import OSMReader

OSM_XML = """
<osm version="0.6">
  <node id="1" lat="35.0000" lon="139.0000" />
  <node id="2" lat="35.0010" lon="139.0020" />
  <node id="3" lat="35.0020" lon="139.0040" />
  <node id="4" lat="35.0030" lon="139.0060" />
  <node id="5" lat="35.0040" lon="139.0080" />
  <node id="6" lat="35.0050" lon="139.0100" />
  <way id="100">
    <nd ref="1" />
    <nd ref="2" />
    <nd ref="3" />
    <tag k="highway" v="primary" />
    <tag k="oneway" v="yes" />
  </way>
  <way id="200">
    <nd ref="3" />
    <nd ref="4" />
    <tag k="highway" v="residential" />
    <tag k="oneway" v="no" />
  </way>
  <way id="300">
    <nd ref="4" />
    <nd ref="5" />
    <tag k="highway" v="service" />
  </way>
  <way id="400">
    <nd ref="5" />
    <nd ref="6" />
    <tag k="highway" v="footway" />
  </way>
</osm>
"""


def test_read_supported_ways_and_split_edges(tmp_path):
    """対応する highway の Way を連続した Edge に分割する。"""
    filepath = tmp_path / "roads.osm"
    filepath.write_text(OSM_XML, encoding="utf-8")

    network = OSMReader(filepath).read()

    assert network.node_count() == 5
    assert network.edge_count() == 4
    assert network.get_neighbors(1) == [2]
    assert network.get_neighbors(2) == [3]
    assert network.get_neighbors(3) == [4]
    assert network.get_neighbors(4) == [3, 5]
    assert network.get_neighbors(5) == [4]


def test_edge_attributes_are_converted(tmp_path):
    """Edge の属性、距離、ジオメトリ、標高未使用時の初期値を設定する。"""
    filepath = tmp_path / "roads.osm"
    filepath.write_text(OSM_XML, encoding="utf-8")

    network = OSMReader(filepath).read()
    edge = network.get_edge(1)

    assert edge.start_node.id == 1
    assert edge.end_node.id == 2
    assert edge.road_type == "primary"
    assert edge.oneway is True
    assert edge.average_gradient == 0.0
    assert edge.distance > 0.0
    assert edge.geometry == [
        Coordinate(latitude=35.0, longitude=139.0),
        Coordinate(latitude=35.001, longitude=139.002),
    ]


def test_unspecified_oneway_is_false(tmp_path):
    """oneway 未指定の場合は双方向として扱う。"""
    filepath = tmp_path / "roads.osm"
    filepath.write_text(OSM_XML, encoding="utf-8")

    network = OSMReader(filepath).read()

    assert network.get_edge(3).oneway is False
