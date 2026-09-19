# amedas-weather ガイド

気象庁アメダスの最新観測値(気温・降水量・風・湿度など)を全国約1,300か所の観測所から取得するスキル。APIキー・ログイン不要(2026-09-19全エンドポイント実測)。

**正本は [`amedas-weather/SKILL.md`](../../amedas-weather/SKILL.md)。** コマンド、フィールドの読み方、品質フラグ、失敗時の対応はすべてそちらを参照。

- データ: 気象庁防災情報サイトのアメダスJSON(latest_time.txt / map / point / amedastable)
- できること: 「今の気温は?」「今雨は降ってる?」を観測所の実測値と観測時刻つきで答える
- 注意: 観測(実況)であり予報ではない。予報は jma-weather、雨雲は amagumo
