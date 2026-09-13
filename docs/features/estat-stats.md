# estat-stats ガイド

e-Stat(政府統計の総合窓口)API v3 で統計表の検索・メタ情報・データ取得を行うスキル。無料のappIdが必要。

**正本は [`estat-stats/SKILL.md`](../../estat-stats/SKILL.md)。** 3つのAPIの手順、ページング、エラー時の対応はすべてそちらを参照。

- データ: e-Stat API v3 `api.e-stat.go.jp/rest/3.0/app/json/`(getStatsList / getMetaInfo / getStatsData)
- ひとことメモ: 認証エラーでもHTTP 200が返る。成否は応答JSONの `RESULT.STATUS`(0=成功)で見る
- 取得データの利用には出典(クレジット)の明記が必要
