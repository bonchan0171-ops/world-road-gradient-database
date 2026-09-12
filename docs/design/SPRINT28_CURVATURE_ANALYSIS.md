# Sprint28 Step1: 曲率解析設計

- ステータス: 設計
- 対象: 道路中心線の平面曲率解析
- 本ステップの範囲: 設計文書の作成のみ
- 実装予定: Sprint28 Step2 以降

## 1. 曲率解析の目的

道路中心線の形状から、各地点の曲がり具合と曲率半径を算出する。勾配解析が道路の鉛直方向の特徴を表すのに対し、曲率解析は水平方向の道路形状を表す指標とする。

主な利用目的は以下のとおり。

- 急カーブ（Sharp Curve）の抽出
- ナビゲーション、走行安全性、物流経路評価のための道路属性作成
- 道路区間ごとの形状比較および統計集計
- 将来のGeoJSON、GeoPackage、データベースへの属性出力

本設計の曲率は、緯度・経度と標高からなる道路の3次元曲線ではなく、道路中心線を水平面へ投影した2次元平面曲率とする。標高は曲率計算には使用せず、既存の勾配解析と独立して扱う。

### 前提と制約

- 入力座標は既存の `RoadSegment` と同じ `(latitude, longitude)` の順序とする。
- 計算に用いる距離と半径の単位はメートルとする。
- 緯度・経度をそのままユークリッド座標として計算しない。各3点の周辺を局所的なメートル座標へ変換してから計算する。
- 3点未満の入力では曲率を計算できない。
- 曲率は入力点の間隔と位置精度に依存するため、結果にはサンプリング密度と座標品質の影響がある。

## 2. 3点法アルゴリズム

連続する3点 `P0`、`P1`、`P2` を1つの解析窓として、中央点 `P1` における曲率を計算する。入力点列が `n` 点の場合、結果は `n - 2` 件となる。結果 `i` は `(Pi, Pi+1, Pi+2)` に対応する。

### 2.1 局所メートル座標への変換

各解析窓の中央点 `P1 = (lat1, lon1)` を原点とし、東向きを `x`、北向きを `y` とする局所座標へ変換する。小さな道路区間では、次の正距近似を初期実装の候補とする。

```text
x = (longitude - lon1) * cos(radians(lat1)) * EARTH_RADIUS_RAD
 y = (latitude - lat1) * EARTH_RADIUS_RAD
```

ここで、`EARTH_RADIUS_RAD = EARTH_RADIUS * pi / 180`、`EARTH_RADIUS` は既存の距離計算で使用する地球平均半径とする。実装時は共通の距離定数を再利用し、距離計算と単位系を一致させる。

長距離区間や高緯度地域での精度要件が明確になった場合は、測地線計算または適切な投影座標系へ置き換えられるよう、座標変換を曲率計算本体から分離する。

### 2.2 外接円の計算

局所座標上の点を `p0`、`p1`、`p2` とし、次を計算する。

```text
v01 = p1 - p0
v12 = p2 - p1
v02 = p2 - p0
cross = v01.x * v12.y - v01.y * v12.x
area2 = abs(cross)

R = |v01| * |v12| * |v02| / (2 * area2)
curvature = 1 / R
```

`area2` は三角形の面積の2倍である。3点が一直線上にある場合は外接円を定義できないため、曲率を `0.0`、曲率半径を正の無限大として扱う。重複点または長さ0の辺を含む場合は、無効な計算結果と区別できるよう、実装では入力エラーまたは無効結果の扱いを定義する。

### 2.3 計算結果の符号

曲率の大きさは `abs(cross)` から求め、常に0以上とする。左右の向きは別属性として、次の符号を `turn_direction` に対応させる。

- `cross > 0`: 左 turn
- `cross < 0`: 右 turn
- `cross == 0`: straight

座標系は東をX、北をYとする。方向判定は曲率の大きさと分離し、右左の符号規約を変更しても数値曲率の意味が変わらないようにする。

## 3. Turn Angle の定義

Turn Angle は、中央点 `P1` で進行方向が変化した角度とする。進入ベクトル `v01 = P1 - P0` と退出ベクトル `v12 = P2 - P1` を使い、次式で定義する。

```text
turn_angle_rad = atan2(abs(cross), dot(v01, v12))
turn_angle_deg = degrees(turn_angle_rad)
```

値域は `0 <= turn_angle_deg <= 180` とする。

- `0°`: 直進
- `0°` より大きい値: 曲がり
- `180°`: 進行方向が反転する形状

左右の向きを必要とする場合は、絶対値を取らない次式の符号を使用する。

```text
signed_turn_angle_rad = atan2(cross, dot(v01, v12))
```

`cross > 0` を左、`cross < 0` を右とする。Turn Angle は方向変化の指標であり、同じ角度でも点間距離が異なれば曲率半径は異なる。そのため、Sharp Curve 判定ではTurn Angleだけでなく曲率半径も併用する。

## 4. Curvature = 1 / Radius の定義

曲率 `Curvature` は曲率半径 `Radius` の逆数として定義する。

$$
\kappa = \frac{1}{R}
$$

- `R`: 3点を通る外接円の半径（m）
- `κ`: 曲率（1/m）
- `κ >= 0`: 本設計では曲率の大きさを保存する
- `κ = 0`: 直線、または実質的に曲率を持たない区間

外接円を計算できる非直線の3点では、`R` と `κ` は有限の正値になる。3点が一直線の場合は `R = infinity`、`κ = 0` とする。曲率を左右付きで利用する将来要件が発生した場合は、`turn_direction` または符号付き曲率を別途追加し、既存の大きさの定義を変更しない。

## 5. Sharp Curve 判定基準

Sharp Curve は、道路利用上の注意が必要な曲線を抽出するための派生判定とする。判定に使う入力は以下の2つとする。

- `turn_angle_deg`: 方向変化の大きさ
- `radius_m`: 曲率半径

初期の既定値は次の候補とする。値は実装前にサンプル道路データで妥当性を確認し、必要に応じて設定値として調整する。

| 項目 | 初期既定値 | 意味 |
|---|---:|---|
| 最小Turn Angle | 45度 | 中央点前後で一定以上の方向変化がある |
| 最大曲率半径 | 100 m | カーブが一定以上に小さい |

基本判定は次のAND条件とする。

```text
is_sharp_curve = (
    turn_angle_deg >= min_turn_angle_deg
    and radius_m <= max_radius_m
)
```

このAND条件により、点の間隔が粗くてTurn Angleだけが大きいケースや、緩やかな大半径カーブだけをSharp Curveと誤判定することを抑える。`radius_m` が無限大または無効値の場合はSharp Curveを `False` とする。

### 判定上の注意

- 既定値は安全基準や道路設計基準を意味するものではなく、WRGDの抽出用初期値である。
- 道路種別、車両種別、制限速度、点密度によって適切な閾値は異なるため、将来はプロファイル別設定または利用者指定を検討する。
- 点間距離が極端に短い、または座標ノイズが大きい場合は、計算前の簡易平滑化や最小辺長の検証が必要になる。平滑化は元の座標を変更するため、本Stepの必須処理には含めない。
- 判定結果と閾値を同時に保存し、後から再現できるようにすることを実装時の要件とする。

## 6. Python API 仕様

曲率計算は外部ファイルを直接扱わないドメインAPIとして提供する。既存の `wrgd.geometry.distance`、`wrgd.geometry.gradient` と同じく、純粋な計算関数を基本とする。

### 6.1 単一の3点を計算するAPI

```text
calculate_turn_angle(
    point1: tuple[float, float],
    point2: tuple[float, float],
    point3: tuple[float, float],
) -> float
```

`(latitude, longitude)` の3点を受け取り、絶対Turn Angleを度で返す。重複点など、方向ベクトルを構成できない入力は `ValueError` とする。

```text
calculate_curvature(
    point1: tuple[float, float],
    point2: tuple[float, float],
    point3: tuple[float, float],
) -> CurvatureResult
```

3点から次の情報を含む `CurvatureResult` を返す。型は実装時にdataclassとして定義する。

| 属性 | 型 | 内容 |
|---|---|---|
| `turn_angle_deg` | `float` | 絶対Turn Angle。度。 |
| `radius_m` | `float` | 外接円半径。メートル。直線は無限大。 |
| `curvature_per_m` | `float` | `1 / radius_m`。1/m。直線は0。 |
| `turn_direction` | `Literal["left", "right", "straight"]` | 左右または直進。 |
| `is_sharp_curve` | `bool` | 指定閾値による判定結果。 |

閾値を変更できるよう、`min_turn_angle_deg` と `max_radius_m` は既定値を持つキーワード引数として設計する。単一3点APIと複数点APIで既定値を共有し、同じ入力条件から同じ判定結果を得られるようにする。

### 6.2 連続座標列を計算するAPI

```text
analyze_curvature(
    coordinates: Sequence[tuple[float, float]],
    min_turn_angle_deg: float = 45.0,
    max_radius_m: float = 100.0,
) -> list[CurvatureResult]
```

仕様は以下のとおりとする。

- `coordinates[i:i + 3]` を順に解析し、結果を入力順で返す。
- 入力が3点未満の場合は空リストを返す。入力検証方針を例外に変更する場合は実装時にテストとともに決定する。
- 結果の件数は `max(0, len(coordinates) - 2)` とする。
- 入力座標列自体は変更しない。
- DEM読込、ファイル出力、GeoJSON/GPKG生成は行わない。
- 閾値が負値など計算不能な場合は `ValueError` とする。

`RoadSegment` との統合はStep2以降で検討する。統合する場合も、既存の距離・勾配配列の意味と件数を変更せず、曲率結果は中央点または3点窓に対応する別の配列・モデルとして保持する。

## 7. GeoJSON/GPKG への将来拡張方針

曲率計算のドメインモデルとファイル形式のWriterを分離する。Step1ではWriterやスキーマの実装は行わず、将来の属性名と対応単位だけを定義する。

### 7.1 GeoJSON

既存のセグメント出力との互換性を保つため、既存属性を変更せず、曲率属性を追加する。3点窓の結果をどのLineStringフィーチャーへ対応付けるかは、次のいずれかを実装時に選択する。

1. 中央点 `P1` を表すPointフィーチャーとして別レイヤーに出力する。
2. `P0-P1` または `P1-P2` の道路セグメントに、中央点由来の属性として出力する。
3. 複数の3点結果をセグメント単位へ集約し、最大曲率や最小半径を出力する。

初期候補の属性名は以下とする。

| 属性名 | 型 | 単位・内容 |
|---|---|---|
| `turn_angle_deg` | `REAL` | Turn Angle。度。 |
| `radius_m` | `REAL` | 曲率半径。メートル。 |
| `curvature_per_m` | `REAL` | 曲率。1/m。 |
| `turn_direction` | `TEXT` | `left`、`right`、`straight`。 |
| `is_sharp_curve` | `BOOLEAN` | Sharp Curve判定。 |

### 7.2 GeoPackage

既存の `road_segments` レイヤーへ属性を追加する場合は、属性の対応単位を明確にする。3点窓の結果をそのまま格納すると、隣接セグメントと1対1にならないため、次のどちらかを基本方針とする。

- **集約方式**: 道路セグメントごとに、対応する曲率結果の最大値、最小半径、Sharp Curve件数などを保存する。
- **別レイヤー方式**: `road_curvature` レイヤーを追加し、中央点または3点窓の識別子、ジオメトリ、曲率属性を保存する。

既存設計の `EPSG:4326` と `X=longitude, Y=latitude` の格納規約を維持する。`radius_m` と `curvature_per_m` はジオメトリの度単位から再計算せず、WRGDのドメイン計算結果を保存する。

将来の実装では、少なくとも次を検証する。

- GeoJSONとGeoPackageで入力順、中央点またはセグメント対応が一致すること
- 曲率半径の単位がメートルであること
- 直線の `curvature_per_m = 0` と無限半径の表現が形式ごとに一貫すること
- Sharp Curveの閾値と判定結果を再現できること
- 既存の距離、勾配、標高、難易度、スコア属性を変更しないこと
- QGISまたはGDALで属性型、CRS、ジオメトリを正しく解釈できること

## 参考資料

- WRGD [アーキテクチャ概要](../ARCHITECTURE.md)
- WRGD [Sprint27 Step1: GeoPackage エクスポート設計](SPRINT27_GPKG_EXPORT.md)
- WRGD `wrgd.geometry.distance` の既存Haversine距離計算
- WRGD `wrgd.road.segment.RoadSegment` の座標列・距離配列モデル
