# Examples

このディレクトリには、README で案内している正式Exampleが含まれています。

## 目的

- `quickstart.py` は README の Quick Start に対応する基本Exampleです。
- `curvature_statistics.py` は、曲率半径とSharp Curve統計を表示する例です。
- `network_route.py` は、OSMネットワークの最短経路をGeoJSONに出力する例です。
- `interactive_map.py` は、生成済みGeoJSONからLeafletマップを生成する例です。
- `python_api_example.py` は Python API の最小構成例です。
- `cli_export_example.py` は CLI で CSV / JSON / PNG を同時に出力する例です。
- `segment_geojson.py` は、道路セグメントごとの勾配と色属性を持つ GeoJSON を出力する例です。

`demo.py` は `quickstart.py` の互換用エントリーポイントです。
`leaflet_demo.py` と `leaflet_map.py` は低レベルの地図ヘルパーとして残していますが、
正式Example一覧には含めません。

## 代表的な実行方法

```bash
python -m examples.quickstart
python -m examples.curvature_statistics
python -m examples.network_route \
	--network roads.osm.xml \
	--start-node 100 \
	--end-node 200 \
	--output output/route.geojson
python -m examples.interactive_map
python -m examples.python_api_example
python -m examples.cli_export_example
python -m examples.segment_geojson
```

## Segment GeoJSON

道路をセグメント単位で GeoJSON に出力できます。

```bash
python -m examples.segment_geojson
output/segments.geojson

出力先の画像や JSON / CSV は `output/` 配下に生成されます。
