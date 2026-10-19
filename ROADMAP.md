# ROADMAP

更新日: 2026-10-13。30日連載は2026-10-10に完了、27スキルを収録。
過去の計画・差し替え理由は [30日計画アーカイブ](docs/archive/roadmap-30-days.md) に保存。
開発ログの区分はREADME、Qiitaの記事番号は連載側で管理する。

## 完了 / Shipped

- 27スキルの一覧と正本への入口は [README](README.md) を参照。
- `air-quality`: CSV速報値と公式JSONの月次履歴に対応。
- `heatstroke`: API v1の予測・実況。旧CSVは使用しない。
- `address-normalize`: 都道府県・市区町村・町字の分解。番地・号の正規化とジオコーディングは対象外。
- `kokkai`・`egov-laws`・`withholding-tax`・`gsi-geocode`: 実装・fixtureテスト済み。
- v1.0.1リリース済み(2026-10-13)。ゆうパック料金表の再検証・実測日比較のJST基準化など10月の修正を収録。

## 現在の優先順位 / Maintenance first

1. 料金・税表の既知の改定日を期限に結び、古い値で回答しない。
2. URL到達、レスポンス形式、データ内容、実際の文書手順を分けて検証する。
3. README・SKILL.md・ガイド・Pagesを同期し、検証していない機能を宣伝しない。

## 次期候補 / Uncommitted candidates

| 候補 | 状態 | 再開・採用条件 |
| --- | --- | --- |
| `odpt-transit` | 保留 | 利用者が公式の無料キーを登録・取得し、対象事業者と条件を実測できた場合のみ。登録代行やスクレイピングはしない |
| `reinfolib-prices` | 保留 | 審査付きAPIキー取得後、公式仕様・利用条件・応答を実測 |
| `dataportal-search` | 未検証 | 現在の公式データポータルとAPIの提供状況を確認してから判断 |
| `hazard-map` | 未検証 | タイルの利用規約と必要な照会方法を確認してから判断 |

日付や実装を約束する表ではない。未確認の候補はSKILL.mdを出さない。

## 不採用・代替 / Rejected or replaced

- `river-level`: 有償提供または定期収集自粛の条件が収録基準と合わず不採用。`amedas-weather`を代替採用済み。
- `station-finder`: ODPT候補と重複するため別スキルとしては不採用。ODPT自体は未採用。
- `nenkin`: 当初の計算テーマからは不採用。将来の判断は新しい提案で行う。

## English summary

The 30-post series is complete. All 27 shipped skills are listed in README.
The original schedule is archived, not a list of pending implementation tasks.
Maintenance prioritizes known data changes, meaningful API checks and synchronized docs.
ODPT and real-estate APIs need user-obtained keys and verified terms; portal search and
hazard tiles remain unverified. No delivery dates are promised.
