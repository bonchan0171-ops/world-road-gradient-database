# Examples

このディレクトリには、README で案内している基本的な利用方法を実行できるサンプルが含まれています。

## 目的

- `demo.py` は、プロジェクトの標準的なデモ実行です。
- `quickstart.py` は README の Quick Start に対応する最短サンプルです。
- `python_api_example.py` は Python API の最小構成例です。
- `cli_export_example.py` は CLI で CSV / JSON / PNG を同時に出力する例です。
- `segment_geojson.py` は、道路セグメントごとの勾配と色属性を持つ GeoJSON を出力する例です。

## 代表的な実行方法

```bash
python -m examples.quickstart
python -m examples.python_api_example
python -m examples.cli_export_example
```

## Segment GeoJSON

道路をセグメント単位で GeoJSON に出力できます。

```bash
python -m examples.segment_geojson
output/segments.geojson

出力先の画像や JSON / CSV は `output/` 配下に生成されます。
