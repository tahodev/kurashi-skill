---
name: bosai-alert
description: 気象庁の防災情報(地震速報・詳細、気象警報・注意報、津波情報)を公開JSONから取得する。APIキー・ログイン不要。
license: MIT
metadata:
  category: disaster
  locale: ja-JP
---

# bosai-alert

気象庁の防災情報を公開JSONから取得するスキル。地震の速報と詳細、地域ごとの警報・注意報、津波情報をカバーする。APIキー不要。

## 地震情報

### 最新の地震一覧

```bash
curl -s https://www.jma.go.jp/bosai/quake/data/list.json
```

直近の地震イベントの配列。主なフィールド:

- `at`: 発生時刻 (ISO 8601)
- `anm`: 震源地名 (`en_anm` は英語表記)
- `mag`: マグニチュード
- `maxi`: 最大震度 (例: "3", "5-", "6+")
- `ttl`: 情報の種類 (震源・震度情報 など)
- `json`: 詳細JSONのファイル名(下記)

### 地震の詳細

一覧の `json` フィールドをそのまま使う。

```bash
curl -s https://www.jma.go.jp/bosai/quake/data/20260908234330_20260908234052_VXSE5k_1.json
```

構造: `Control` (発表情報) と `Body` (震源、震度観測点のリストなど)。`Body.Intensity.Observation` に地域ごとの震度が入る。

## 気象警報・注意報

```bash
curl -s https://www.jma.go.jp/bosai/warning/data/warning/130000.json
```

`130000` は `offices` コード (気象庁エリア定義 `https://www.jma.go.jp/bosai/common/const/area.json` を参照)。

- `headlineText`: 見出し文
- `areaTypes[].areas[].warnings`: 地域ごとの警報・注意報。`code` と `status` (発表/継続/解除) を持つ。

## 津波情報

```bash
curl -s https://www.jma.go.jp/bosai/tsunami/data/list.json
```

発表中の津波情報一覧。空配列 `[]` なら現在発表なし。

## 注意

- 緊急時はこのスキルの結果だけで判断せず、気象庁・自治体の公式発表を確認するよう案内する。
- データは発表のたびに更新される。引用時は発表時刻を一緒に伝える。
- 短時間に連続リクエストしない。
