# jma-weather ガイド

気象庁の公開JSONから天気・降水確率・気温の予報を取得するスキル。APIキー・ログイン不要。

**正本は [`jma-weather/SKILL.md`](../../jma-weather/SKILL.md)。** エリアコードの調べ方、JSONの構造、天気コード、エラー時の対応まですべてそちらにまとまっている。このガイドは概要のみ。

- データ: 気象庁 `www.jma.go.jp/bosai/forecast/` の公開JSON (UTF-8)
- できること: 「明日の東京の天気は?」のような予報照会。発表時刻(`reportDatetime`)つきで答える
