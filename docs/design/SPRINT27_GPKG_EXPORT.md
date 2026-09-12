# Sprint27 Step1: GeoPackage エクスポート設計

- ステータス: 設計
- 対象: `wrgd analyze` の道路セグメント出力
- 本ステップの範囲: 設計文書の作成のみ
- 実装予定: Sprint27 Step2 以降

## 1. GeoPackage 採用理由

GeoPackage（`.gpkg`）を、既存の GeoJSON 出力に追加する GIS 向けの交換・保存形式として採用する。

採用理由は以下のとおり。

1. **単一ファイルで配布できる**
   - GeoPackage は SQLite をベースとするため、道路セグメントと空間メタデータを 1 ファイルにまとめられる。
   - 付随するインデックスや設定ファイルを別途配布する必要がない。

2. **GIS ソフトウェアとの相互運用性が高い**
   - GeoPackage は OGC 標準であり、主要な GIS ソフトウェアで読み込める形式を目指せる。
   - QGIS、GDAL などでの確認・加工・再利用を想定する。

3. **属性を SQL で検索できる**
   - `gradient_pct`、`distance_m`、`difficulty` などを SQL で抽出・集計できる。
   - GeoJSON のようにファイル全体を読み込まず、条件に合うセグメントだけを扱える。

4. **空間参照系をファイル内に記録できる**
   - `gpkg_spatial_ref_sys` とレイヤー定義に CRS を記録し、座標の解釈を明確にできる。
   - 本設計では `EPSG:4326` を採用する（6. 参照）。

5. **将来のレイヤー追加に対応できる**
   - Step1 では `road_segments` のみを定義する。
   - 将来、道路中心線、標高サンプル、処理メタデータなどを同一ファイルに追加できる。

既存の GeoJSON、CSV、JSON 出力は廃止しない。GeoPackage は同じ解析結果を別の利用目的に提供する任意の追加出力とする。

## 2. CLI 仕様（`--gpkg`）

### 2.1 コマンド形式

`--gpkg` は `analyze` サブコマンドの任意オプションとする。

```text
wrgd analyze \
  --route data/sample/sample.gpx \
  --dem data/raw/output_hh.tif \
  --gpkg output/segments.gpkg
```

既存の省略形である以下の形式でも利用できるようにする。

```text
wrgd \
  --route data/sample/sample.gpx \
  --dem data/raw/output_hh.tif \
  --gpkg output/segments.gpkg
```

### 2.2 入出力契約

| 項目 | 仕様 |
|---|---|
| オプション名 | `--gpkg` |
| 型 | `Path` 相当の出力パス |
| 必須性 | 任意。指定しない場合は GeoPackage を作成しない |
| 出力形式 | OGC GeoPackage |
| 既定レイヤー名 | `road_segments` |
| CRS | `EPSG:4326` |
| ジオメトリ | セグメントごとの 2 点 `LineString` |
| 親ディレクトリ | 存在しない場合は作成する |
| 既存ファイル | 設計時点では上書き方針とする。誤上書き防止の詳細は実装時に確定する |

`--gpkg` を指定した場合、既存のルート読込、DEM 読込、`RoadSegmentBuilder` による標高・距離・勾配計算は変更しない。計算済みの `RoadSegment` を GeoPackage Writer に渡して出力する。

`--csv`、`--json`、`--output`、`--interactive` との併用を許可する。各オプションの出力先と内容は変更しない。

### 2.3 エラー方針

- 入力ルートまたは DEM が存在しない場合は、既存 CLI と同じ入力検証を行う。
- セグメントが 2 点未満の場合は出力せず、既存の `RoadSegment` 検証エラーを利用する。
- 出力先を作成または書き込みできない場合は、原因が分かるエラーを表示する。
- GeoPackage として必要なテーブルまたは CRS 情報を作成できない場合は、部分的な成功として扱わない。

## 3. Python API 仕様

既存の `GeoJSONWriter` と責務を分け、GeoPackage 出力専用の Writer API を追加する。クラス名は `GeoPackageWriter` とする。

### 3.1 コンストラクター

```text
GeoPackageWriter(
    filepath: str | Path,
    layer_name: str = "road_segments",
    crs: str = "EPSG:4326",
)
```

| 引数 | 仕様 |
|---|---|
| `filepath` | `.gpkg` ファイルの出力先 |
| `layer_name` | 出力レイヤー名。既定値は `road_segments` |
| `crs` | レイヤーの CRS。Step1 の CLI では `EPSG:4326` 固定 |

### 3.2 セグメント出力メソッド

```text
write_segments(
    road_segment: RoadSegment,
    difficulty: DifficultyLevel | None = None,
    score: float | None = None,
) -> None
```

仕様は以下のとおりとする。

- `RoadSegment.coordinates` の隣接点から 1 セグメント 1 フィーチャーを作成する。
- `distances[index]` と `gradients[index]` を同じ `segment_id` の属性として保存する。
- `RoadSegment.elevations[index]` はセグメント始点の標高として `elevation_m` に保存する。
- `difficulty` と `score` が渡された場合だけ、対応する属性を保存する。未指定時は `NULL` とする。
- `GeoJSONWriter.write_segments()` と同じく、セグメント数と距離・勾配配列の整合性を検証する。
- 返り値は持たず、書き込みに失敗した場合は例外で通知する。

### 3.3 CLI からの利用

CLI は解析済みの `RoadSegment`、`DifficultyLevel`、スコアを `GeoPackageWriter.write_segments()` に渡す。Writer が DEM 読込、距離計算、勾配計算を行ってはならない。これにより、既存のドメイン処理と保存処理を分離する。

Step1 では読み込み API、レイヤー結合、属性更新 API は定義しない。

## 4. `road_segments` レイヤー定義

### 4.1 レイヤー基本定義

| 項目 | 定義 |
|---|---|
| テーブル名 | `road_segments` |
| `gpkg_contents.data_type` | `features` |
| ジオメトリ列 | `geom` |
| ジオメトリ型 | `LINESTRING` |
| 次元 | 2D（Z/M なし） |
| CRS | `EPSG:4326` |
| 識別子 | `segment_id` |
| セグメント順序 | 0 始まり。入力座標列の隣接点順を保持 |
| 空間インデックス | 実装時に GeoPackage の標準的な RTree 作成を検討する |

`geom` は隣接する始点・終点の 2 点を持つ `LineString` とする。座標の格納順は GeoPackage の XY 順に従い、`X=経度`、`Y=緯度` とする。内部モデルが `(latitude, longitude)` である点に注意し、出力時に順序を変換する。

### 4.2 GeoPackage 標準メタデータ

実装時は、少なくとも次の GeoPackage 標準テーブルへ整合した値を登録する。

- `gpkg_contents`: `road_segments` のテーブル名、データ種別、範囲、識別子、CRS
- `gpkg_geometry_columns`: `geom` の型、次元、SRID
- `gpkg_spatial_ref_sys`: `EPSG:4326` の定義

これらは WRGD 独自テーブルとして再定義しない。標準スキーマとの互換性を優先する。

## 5. 属性一覧

属性名は GeoPackage の列名として使用する。単位を列名または設計書で明示し、曖昧な単位なしの列名を追加しない。

| 列名 | 型 | NULL | 内容 |
|---|---|---:|---|
| `segment_id` | `INTEGER` | 不可 | セグメント識別子。入力座標列の隣接点に対応する 0 始まりの連番 |
| `distance_m` | `REAL` | 不可 | セグメント長。メートル。既存 `RoadSegment.distances` の値 |
| `gradient_pct` | `REAL` | 不可 | 勾配。パーセント。既存 `RoadSegment.gradients` の値 |
| `elevation_m` | `REAL` | 可 | セグメント始点の標高。メートル。標高列が利用できない場合は NULL |
| `color` | `TEXT` | 可 | 勾配可視化用の `#RRGGBB` 形式。既存の `gradient_to_color()` と整合させる |
| `difficulty` | `TEXT` | 可 | 難易度名。`DifficultyLevel.name`。指定されない場合は NULL |
| `score` | `REAL` | 可 | 道路評価スコア。0–100。指定されない場合は NULL |

### 属性に関する決定事項

- GeoJSON に存在する `distance` と `gradient` の短縮名は、GeoPackage では採用しない。単位が明確な `distance_m` と `gradient_pct` を正規名とする。
- `elevation_m` はセグメント全体の平均標高ではなく、既存 GeoJSON 出力との互換性を保つため始点標高を表す。
- `segment_id` はデータベースの内部主キーとは別に、入力ルート上の順序を表す論理識別子とする。内部主キーの要否は実装時に GeoPackage の標準要件に合わせて決定する。
- `difficulty` と `score` は解析結果に付随する任意属性であり、勾配計算そのものの必須入力ではない。

## 6. EPSG:4326 を採用する理由

`road_segments` の CRS は `EPSG:4326`（WGS 84）とする。

1. **入力データとの整合性**
   - WRGD の `Coordinate` は緯度・経度の十進度で表現される。
   - GPX、GeoJSON の既存入出力も地理座標を基本とするため、出力時の変換を最小化できる。

2. **世界規模の道路データに適する**
   - WRGD は特定国の投影座標系ではなく、世界の道路データを扱うことを目的とする。
   - EPSG:4326 は WGS 84 の地理 2D CRS で、世界規模の位置表現に利用できる。

3. **既存 GIS との接続が容易**
   - GPS、Web 地図、GeoJSON などで広く利用される CRS であり、利用者が追加の CRS 情報を推測せずに済む。

4. **解析距離と表示 CRS を分離できる**
   - EPSG:4326 の軸単位は度であるため、GeoPackage のジオメトリ長をメートルとして直接計算しない。
   - 距離と勾配は既存の WRGD の計算結果を `distance_m` と `gradient_pct` に保存する。
   - メートル単位の正確な空間計算が必要な利用者は、利用地域に適した投影 CRS へ変換して行う。

### 座標順序

EPSG:4326 は地理座標系だが、GeoPackage のジオメトリ座標は XY として格納する。したがって、実際の格納値は次の順序とする。

```text
X = longitude
Y = latitude
```

この順序を API、テスト、ドキュメントで一貫させる。内部の `(latitude, longitude)` タプルをそのままバイナリへ書き込んではならない。

## 実装時の検証項目

Step2 以降の実装では、少なくとも以下を検証する。

- GeoPackage が QGIS または GDAL で開けること
- `road_segments` が `LINESTRING`、`EPSG:4326` として認識されること
- 2 点の座標順が経度・緯度であること
- セグメント数、`distance_m`、`gradient_pct` が `RoadSegment` と一致すること
- 任意属性の未指定値が NULL になること
- CSV、JSON、GeoJSON、インタラクティブ地図の既存出力が変わらないこと
- 同じ入力から出力した GeoJSON と GeoPackage のセグメント順および属性値が一致すること

## 参考資料

- Open Geospatial Consortium, **GeoPackage Encoding Standard 1.3.1**: <https://www.geopackage.org/spec131/> （参照日: 2026-09-12）
- Open Geospatial Consortium, **GeoPackage Standard**: <https://www.ogc.org/standards/geopackage/> （参照日: 2026-09-12）
- EPSG Geodetic Parameter Dataset, **EPSG:4326 WGS 84**: <https://epsg.org/crs_4326/WGS-84.html> （参照日: 2026-09-12）
- WRGD 既存実装: `src/wrgd/io/geojson_writer.py`、`src/wrgd/road/segment.py`、`src/wrgd/cli.py`
