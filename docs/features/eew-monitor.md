# eew-monitor ガイド

緊急地震速報(EEW)の発表状況と直近の地震・津波情報を、キー不要の公開API(wolfx / P2P地震情報)から取得するスキル。

**正本は [`eew-monitor/SKILL.md`](../../eew-monitor/SKILL.md)。** フィールドの意味、「発表中かどうか」の判断、強震モニタの扱い、失敗時の対応はすべてそちらを参照。

- データ: wolfx `api.wolfx.jp/jma_eew.json`、P2P地震情報 API v2 `api.p2pquake.net/v2/`(いずれも気象庁電文の非公式中継)
- ひとことメモ: 平時は wolfx が「最後のEEWの最終報」を返す。`Issue.Status` が `通常` なら発表中ではない
- 確定情報は `bosai-alert`(気象庁公式)、緊急時の判断は気象庁・自治体の公式発表で
