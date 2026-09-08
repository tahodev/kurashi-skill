# jma-weather ガイド

気象庁の公開JSONから天気予報を取得するスキル。APIキー・ログイン不要。

## 使い方の例

「明日の東京の天気は?」と聞かれたら:

1. `https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json` を取得
2. `timeSeries` の `timeDefines` から明日の枠を探す
3. 同じインデックスの `weathers` / `pops` / `temps` を読む
4. 発表時刻(`reportDatetime`)を添えて答える

## エンドポイント一覧

| 用途 | URL |
| --- | --- |
| エリア定義 | `https://www.jma.go.jp/bosai/common/const/area.json` |
| 予報(天気・降水確率・気温) | `https://www.jma.go.jp/bosai/forecast/data/forecast/{officesコード}.json` |
| 週間予報テキスト | `https://www.jma.go.jp/bosai/forecast/data/overview_week/{officesコード}.json` |
| 短期予報テキスト | `https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{officesコード}.json` |

詳しいJSONの構造と天気コードは `jma-weather/SKILL.md` を参照。

## つまずきポイント

- **気温が取れない枠がある**: 発表時刻によって `temps` に入るのは最低・最高だけ、ということが多い。枠の時刻と照合して「明日の最高気温」など意味を確認する。
- **エリアコードが分からない**: まず `area.json` を取得し、地名で検索して `offices` コードを見つける。
- **文字化けしない**: 気象庁のJSONはUTF-8。そのまま処理できる。
