# ROADMAP

30日間の公開開発チャレンジの Day 7-30 に向けたスキル候補の一覧。収録基準は [CONTRIBUTING.md](CONTRIBUTING.md) と同じ: **ログイン不要・課金不要**(無料即時発行のAPIキーは可)、**公式API・公開データのみ**、**照会・計算のみ**。

候補の採用条件:

1. 実際にコマンドを実行して動くことを確認してから採用する(実測なしでSKILL.mdを書かない)。
2. 失敗時の対応セクションを必ず付ける。
3. 外部データに基準日があるものは、基準日と公式の根拠URLを明記する。
4. 採用したら下の表を更新し、[CHANGELOG.md](CHANGELOG.md) に記録する。

## 候補一覧 (Day 7-30)

| # | 候補名 | できること | データソース | 認証 | 検証メモ |
| --- | --- | --- | --- | --- | --- |
| 1 | `amedas-weather` | アメダスの最新観測値(気温・降水量・風)の照会 | 気象庁 防災情報 JSON (`bosai/amedas`) | 不要 | 2026-09-11 `latest_time.txt` 実測200。時系列JSONの構造確認が次のステップ |
| 2 | `ndl-books` | 国立国会図書館サーチで書誌検索(ISBN・タイトル) | NDL Search API (SRU / OpenSearch) | 不要 | 公式仕様書あり。calil-books と棲み分け(蔵書ではなく書誌) |
| 3 | `estat-stats` | 政府統計(人口・経済など)の統計表検索とデータ取得 | e-Stat API | 無料appId(要登録) | calil-books方式のキー前提スキルとして扱う |
| 4 | `dataportal-search` | data.go.jp のオープンデータセット横断検索 | data.go.jp メタデータ取得API (CKAN互換) | 不要 | CKAN標準API。ヒットしたデータセットの形式はまちまちなので出力は検索まで |
| 5 | `zipcode-lookup` | 郵便番号⇔住所の照会 | 日本郵便 郵便番号データ(CSV) | 不要 | 公式CSVダウンロード。更新頻度(月次)の注記が必要 |
| 6 | `reinfolib-prices` | 不動産取引価格・地価公示の照会 | 国土交通省 不動産情報ライブラリ API | 無料キー(審査あり) | キー発行に承認が要るので即時性はcalil型より低い。取得手順をSKILL.mdに書く |
| 7 | `air-quality` | 大気汚染の常時監視データ(PM2.5など)の照会 | 環境省 そらまめ君 データダウンロード | 不要 | CSVダウンロード型。リアルタイムAPIではない点を明記 |
| 8 | `odpt-transit` | 鉄道・バスの時刻表・運行情報の照会 | 公共交通オープンデータセンター (ODPT) API | 無料キー(要登録) | 対象事業者が限定される点を明記 |
| 9 | `bosai-typhoon` | 台風の現況・進路予報の照会 | 気象庁 防災情報 JSON (`bosai/typhoon`) | 不要 | 台風非発生時は一覧が404になることを2026-09-11実測。空=平時の扱いを失敗時対応に明記 |
| 10 | `hazard-map` | 洪水・土砂災害などのハザード情報の照会 | 国土数値情報 / ハザードマップポータル | 不要 | データ形式の実測から。タイル配信は利用規約の確認が先 |
| 11 | `shelter-lookup` | 指定避難所・避難場所の検索 | 国土数値情報 避難所データ | 不要 | ダウンロード型。位置検索の計算部分が中心になる見込み |
| 12 | `address-normalize` | 住所文字列の正規化・緯度経度の付与 | デジタル庁 アドレス・ベース・レジストリ (ABR) | 不要 | 配布形態(カタログデータ/ツール)の実測から採用判断 |
| 13 | `withholding-tax` | 源泉徴収税額の目安計算 | 国税庁 公表の税額表 | 不要 | furusato-nozei方式の純計算スキル。基準日・根拠URLが必須 |

上記以外のアイデアは issue テンプレート「スキル追加の提案」から。採用・不採用の判断はこのファイルに記録する。

---

## Roadmap (English summary)

Candidate backlog for Days 7-30 of the 30-day build-in-public challenge. Every candidate follows the repo's inclusion rules: no login or paid key (free instant API keys are OK), official APIs or public datasets only, read-only lookups and calculations. A candidate is adopted only after its commands are tested for real, and every adoption is recorded here and in the changelog.
