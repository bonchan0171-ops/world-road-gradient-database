# Examples

このディレクトリには、README で案内している正式Exampleが含まれています。

## 目的

- `quickstart.py` は README の Quick Start に対応する基本Exampleです。
- `curvature_statistics.py` は、曲率半径とSharp Curve統計を表示する例です。
- `network_route.py` は、下記のNetwork Route Analysis Exampleを参照してください。
- `interactive_map.py` は、生成済みGeoJSONからLeafletマップを生成する例です。
- `python_api_example.py` は Python API の最小構成例です。
- `cli_export_example.py` は CLI で CSV / JSON / PNG を同時に出力する例です。
- `segment_geojson.py` は、道路セグメントごとの勾配と色属性を持つ GeoJSON を出力する例です。

`demo.py` は `quickstart.py` の互換用エントリーポイントです。
`leaflet_demo.py` と `leaflet_map.py` は低レベルの地図ヘルパーとして残していますが、
正式Example一覧には含めません。

## Network Route Analysis Example

`network_route.py` は、OSM道路ネットワークから最短経路を求め、DEMを使って
標高・勾配・曲率を分析する正式Exampleです。外部データを取得せず、同梱fixtureで実行できます。

必要な入力:

- OSM network file: `tests/data/sample_network.osm`
- DEM GeoTIFF: `tests/data/sample_dem.tif`
- start node ID: `1`
- end node ID: `3`（fixture内のWayで到達可能）
- `--output`: 出力GeoJSONのパス
- `--json`: 任意のFull Analysis JSON出力パス

実行例:

```bash
python -m examples.network_route \
	--network tests/data/sample_network.osm \
	--dem tests/data/sample_dem.tif \
	--start-node 1 \
	--end-node 3 \
	--output output/network-route.geojson \
	--json output/network-route-analysis.json
```

出力:

- ターミナルに経路summaryと `RoadStatistics`（標高・勾配・曲率統計）を表示
- GeoJSONに経路座標と分析propertiesを出力
- `--json` 指定時はsummaryとstatisticsを含むFull Analysis JSONを出力

経路summaryから `bridge_count`、`tunnel_count`、`road_type_counts` を取得できます。
OSMの橋・トンネル属性は対応するWay tagに基づきます。

## 代表的な実行方法

```bash
python -m examples.quickstart
python -m examples.curvature_statistics
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
