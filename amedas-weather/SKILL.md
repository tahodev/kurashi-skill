---
name: amedas-weather
description: 気象庁アメダスの最新観測値(気温・降水量・風・湿度など)を全国約1,300か所の観測所から取得する。今の気温、今雨は降ってる、今の風速、観測時刻の質問に対応。APIキー・ログイン不要。明日以降の予報はjma-weather、雨雲の様子はamagumo、警報・地震はbosai-alertを使う。
license: MIT
metadata:
  category: weather
  locale: ja-JP
---

# amedas-weather

気象庁が防災情報サイトで公開しているアメダス(地域気象観測システム)の最新観測値JSONを読むスキル。全国約1,300か所の観測所の気温・降水量・風向風速・湿度・気圧・日照をカバーする。APIキー不要、curlだけで取れる。2026-09-19に全エンドポイントを実測した。

## 基本の流れ

1. 最新データの時刻を取る
2. 全観測所の最新値JSONを取り、観測所コードで絞る
3. 観測所名・緯度経度は観測所テーブルで引く

### 1. 最新の時刻を取る

```bash
curl -sm 30 https://www.jma.go.jp/bosai/amedas/data/latest_time.txt
```

`2026-09-19T12:30:00+09:00` のようなJSTのISO形式で1行返る(2026-09-19実測)。観測値はこの時刻のもの。**必ずこの時刻をユーザーに添える**(今まさにではなく観測時刻の値。実測では配信が実時刻より十数分遅れることがあった)。

### 2. 最新値JSONを取る

URLの時刻部分は `YYYYMMDDHHMMSS` 形式のJST。手順1の値から組み立てる(推測で丸めない):

```bash
TS=$(curl -sm 30 https://www.jma.go.jp/bosai/amedas/data/latest_time.txt)
STAMP=$(printf '%s' "$TS" | tr -d -- '-:+T' | cut -c1-12)00
curl -sm 30 "https://www.jma.go.jp/bosai/amedas/data/map/${STAMP}.json"
```

全観測所分まとめて1ファイル(2026-09-19実測で約250KB・1,286観測所)。キーが観測所コード。東京(44132)の2026-09-19 12:30の実測例:

```json
"44132": {
  "pressure": [1016.1, 0], "normalPressure": [1018.9, 0],
  "temp": [21.9, 0], "humidity": [92, 0],
  "sun10m": [0, 0], "sun1h": [0.0, 0],
  "precipitation10m": [0.0, 0], "precipitation1h": [1.0, 0],
  "precipitation3h": [1.0, 0], "precipitation24h": [1.0, 0],
  "windDirection": [14, 0], "wind": [2.3, 0]
}
```

過去時刻のファイルも残っている(2026-09-19に前日分を実測して200)。存在しない時刻は404。

### 3. 観測所を引く

```bash
curl -sm 30 https://www.jma.go.jp/bosai/amedas/const/amedastable.json
```

観測所コード → `{type, elems, lat, lon, alt, kjName, knName, enName}`(2026-09-19実測、1,286件)。`kjName` が漢字名(「東京」)、`lat`/`lon` は [度, 分] の配列。駅名などからの逆引きはこのテーブルで行い、最寄りは緯度経度で距離計算する。`type` は観測所区分("A"など)、`elems` はその観測所が持つ観測要素のフラグ列。

### (応用) 1観測所の10分値時系列

```bash
# 観測所コード/YYYYMMDD_HH.json。HHは3時間ブロック(00,03,...,21)
curl -sm 30 "https://www.jma.go.jp/bosai/amedas/data/point/44132/20260919_12.json"
```

10分ごとの観測値が時刻キーで返る(2026-09-19実測で200)。その日の気温の推移や雨が降り始めた時刻を答えるのに使う。

## レスポンスの読み方

各要素は `[値, 品質フラグ]` の2要素配列。

- `temp`: 気温(℃)。`humidity`: 湿度(%)。`pressure`/`normalPressure`: 現地気圧/海面気圧(hPa)。
- `precipitation10m`/`1h`/`3h`/`24h`: 降水量(mm)。0.0は「雨なし」。
- `wind`: 風速(m/s)。`windDirection`: 風向の16方位コード(0=静穏、1=北、2=北北東、3=北東、4=東北東、5=東、6=東南東、7=南東、8=南南東、9=南、10=南南西、11=南西、12=西南西、13=西、14=西北西、15=北西、16=北北西。2026-09-19の全観測所で値域0〜16を確認)。
- `sun10m`/`sun1h`: 日照時間(10分値は分、1時間値は時間)。
- 品質フラグは 0=正常。0以外(準正常など)も返る。欠測は値が `null` になることがある(2026-09-19実測: 富士山の `sun10m` が `[null, 5]`)。**nullの要素は「この観測所では取れていない」と言い、推測で値を言わない。**
- 観測所によって持たない要素がある(積雪系など)。キー自体がない場合も「その要素は未観測」として扱う。

## エラー・失敗時の対応

- `curl` には必ず `-m 30` を付ける。
- **404**: map/時系列の時刻部分か観測所コードの誤り(2026-09-19に存在しない時刻・存在しない観測所コードで404を実測)。まず `latest_time.txt` を取り直してURLを組み立て直す。
- **空・欠測**: 値が `null` または要素キーがない場合は欠測・未観測。0や平年値で埋めない。
- **遅延**: `latest_time.txt` が現在時刻より古い場合は配信遅延。その時刻のデータであると明示して答え、再取得して「更新を待つ」ことはしない。

## 注意

- アメダスは**観測(実況)**。予報は `jma-weather`、雨雲の様子は `amagumo`、警報・地震・津波は `bosai-alert`、台風は `bosai-typhoon` を使う。
- 値は観測所の地点のもの。「東京」は大手町の観測所(コード44132)で、都内全域を代表しない。
- 観測所コードは地域番号+観測所番号の5桁(例: 44132)。気象庁の予報区等で使う6桁コードとは別物。

## English summary

Reads the latest AMeDAS observations (temperature, precipitation, wind, humidity, pressure, sunshine) for about 1,300 stations across Japan from JMA's public disaster-information JSON. No API key or login. Flow: read `latest_time.txt` for the current observation time, fetch `map/<YYYYMMDDHHMMSS>.json` (all stations, keyed by station code), and resolve station names/coordinates via `const/amedastable.json`. A per-station 10-minute time series is available at `point/<code>/<YYYYMMDD_HH>.json` (HH in 3-hour blocks). Values are `[value, quality flag]` pairs; missing values come back as `null` or absent keys and must be reported as missing, never guessed. Always quote the observation time from `latest_time.txt` with the answer, since delivery can lag real time by tens of minutes. All endpoints verified live on 2026-09-19; unknown timestamps and unknown station codes return 404. Use jma-weather for forecasts, amagumo for rain radar, bosai-alert for warnings and earthquakes.
