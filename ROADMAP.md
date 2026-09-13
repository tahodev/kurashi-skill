# ROADMAP

30日間の公開開発チャレンジの Day 7-30 の計画。収録基準は [CONTRIBUTING.md](CONTRIBUTING.md) と同じ: **ログイン不要・課金不要**(無料即時発行のAPIキーは可)、**公式API・公開データのみ**、**照会・計算のみ**。

採用の条件:

1. 実際にコマンドを実行して動くことを確認してから採用する(実測なしでSKILL.mdを書かない)。
2. 失敗時の対応セクションを必ず付ける。
3. 外部データに基準日があるものは、基準日と公式の根拠URLを明記する。
4. 採用したら下の表を更新し、[CHANGELOG.md](CHANGELOG.md) に記録する。

## 採用スケジュール (Day 7-30) — 2026-09-11 決定

Day 1 の Qiita 記事で公表した案(以下「A案」)と、検証済み候補一覧(「B案」)をマージした結果。A案の週構成(週頭の振り返り、Day 29 の v1.0.0、Day 30 の総括)を骨格に、重複する候補は実測済みの名前・データソースに統一し、B案の検証済み候補を組み込んだ。Week 3 が防災寄りなのは、9月(防災の日・台風シーズン・残暑)に合わせた意図的な構成。

| Day | スキル | 内容 | データソース | 認証 | 検証メモ |
| --- | --- | --- | --- | --- | --- |
| 7 | (振り返り) | Week 2 の振り返り記事 | - | - | スキル追加なし |
| 8 | `wareki` | 西暦⇔和暦(令和・平成など)の変換 | 純計算 | 不要 | 元号の改元日は静的データとして保持 |
| 9 | `rokuyo` | 六曜(大安・仏滅など)の算出 | 純計算 | 不要 | 旧暦換算が必要。計算の根拠を明記 |
| 10 | `zipcode-lookup` | 郵便番号⇔住所の照会 | 日本郵便 郵便番号データ(CSV) | 不要 | 公式CSV(utf_ken_all)の存在を2026-09-11確認。**月次更新**(追加・廃止の差分あり)の注記が必要 |
| 11 | `yubin-fee` | 郵便料金の目安計算 | 日本郵便 公表の料金表 | 不要 | 料金表は静的データとして保持し、基準日と根拠URLを明記 |
| 12 | `amagumo` | 雨雲の動き(降水ナウキャスト)の照会 | 気象庁 防災情報 JSON | 不要 | jma-weather(予報)とは観測/ナウキャストで棲み分け |
| 13 | `bosai-typhoon` | 台風の現況・進路予報の照会 | 気象庁 防災情報 JSON (`bosai/typhoon`) | 不要 | **台風非発生時は一覧が404になる**ことを2026-09-11実測。空=平時の扱いを失敗時対応に明記 |
| 14 | (振り返り) | Week 3 の振り返り記事 | - | - | スキル追加なし |
| 15 | `volcano` | 火山の噴火警報・活動情報の照会 | 気象庁 防災情報 JSON | 不要 | bosai-alert と同系のJSON。対象火山の一覧を明記 |
| 16 | `shelter-lookup` | 指定避難所・避難場所の検索 | 国土数値情報 避難所データ | 不要 | ダウンロード型。位置検索の距離計算部分が中心になる見込み |
| 17 | `river-level` | 河川の水位・氾濫注意情報の照会 | 国土交通省 川の防災情報 | 不要 | **curl 直接アクセスは403。ブラウザ相当の User-Agent ヘッダが必要**(2026-09-11実測)。公式サイトの公開情報であり、ヘッダ付与のみで回避策は使わない |
| 18 | `air-quality` | 大気汚染の常時監視データ(PM2.5など)の照会 | 環境省 そらまめ君 データダウンロード | 不要 | CSVダウンロード型。リアルタイムAPIではない点を明記 |
| 19 | `heatstroke` | 暑さ指数(WBGT)・熱中症警戒情報の照会 | 環境省 暑さ指数予報等 | 不要 | 9月の残暑に季節的に合致。予報/実況の区別を明記 |
| 20 | `address-normalize` | 住所文字列の正規化・緯度経度の付与 | デジタル庁 アドレス・ベース・レジストリ (ABR) | 不要 | 配布形態(カタログデータ/ツール)の実測から採用判断 |
| 21 | (振り返り) | Week 4 の振り返り記事 | - | - | スキル追加なし |
| 22 | `odpt-transit` | 鉄道・バスの時刻表・運行情報の照会 | 公共交通オープンデータセンター (ODPT) API | 無料キー(要登録) | 対象事業者が限定される点を明記。乗換案内のスクレイピングではなく公式APIの経路 |
| 23 | `ndl-books` | 国立国会図書館サーチで書誌検索(ISBN・タイトル) | NDL Search API (SRU / OpenSearch) | 不要 | 公式仕様書あり。calil-books と棲み分け(蔵書ではなく書誌) |
| 24 | `aozora` | 青空文庫の作品検索 | 青空文庫 カタログCSV | 不要 | 公式APIはなく公開CSVカタログを利用。更新頻度の注記が必要 |
| 25 | `kokkai` | 国会会議録の検索 | 国会会議録検索システム API | 不要 | 2026-09-11実測で応答確認(パラメータ必須、認証不要) |
| 26 | `egov-laws` | 法令条文の検索・照会 | e-Gov 法令API v2 | 不要 | v1 は廃止済み。v2 のエンドポイントを使う |
| 27 | `withholding-tax` | 源泉徴収税額の目安計算 | 国税庁 公表の税額表 | 不要 | furusato-nozei方式の純計算スキル。基準日・根拠URLが必須 |
| 28 | ~~`garbage-day`~~ (採用済み) | ごみ収集日の照会 | 5374形式の公開CSV | 不要 | **2026-09-13に前倒し採用**。下の「追加採用」参照。Day 28 の記事枠は振り返りか差し替え候補から選ぶ |
| 29 | (v1.0.0) | 全スキルの最終点検と v1.0.0 リリース | - | - | git tag と GitHub Release を同バージョンで作成 |
| 30 | (総括) | 30日間の総括記事 | - | - | スキル追加なし |

## 追加採用 (2026-09-13)

スケジュール外・バックログから4スキルを採用し実装した。

| スキル | 内容 | データソース | 認証 | 由来 |
| --- | --- | --- | --- | --- |
| `eew-monitor` | 緊急地震速報(EEW)の発表状況と直近の地震・津波情報 | wolfx (api.wolfx.jp) / P2P地震情報 API v2 (いずれも気象庁電文の非公式中継) | 不要 | 新規。bosai-alert(気象庁公式の確定情報)との棲み分けを明記 |
| `estat-stats` | 政府統計の統計表検索・データ取得 | e-Stat API v3 | 無料appId(要登録) | バックログから採用 |
| `garbage-day` | ごみ収集日の照会 | 5374形式の公開CSV(金沢・美唄・松前・笠間・上砂川・大分を2026-09-13実測) | 不要 | Day 28 から前倒し |
| `koyobun-check` | 公用文の表記校閲 | 文化審議会建議「公用文作成の考え方」(令和4年。知識スキル、APIなし) | 不要 | 新規 |

## 不採用 (2026-09-11 決定)

| 候補名 | 不採用の理由 |
| --- | --- |
| `station-finder` | `odpt-transit` が上位互換(駅検索・時刻表・運行情報をまとめてカバー)のため統合 |
| `nenkin` | `furusato-nozei` と計算スキルとしてのパターンが重複。フリーランスの読者には `withholding-tax` のほうが実用的と判断 |

## バックログ (差し替え候補)

採用スケジュールに空きが出た場合や、採用候補が実測で使えなかった場合の差し替え枠。

| 候補名 | 内容 | 保留の理由 |
| --- | --- | --- |
| `reinfolib-prices` | 不動産取引価格・地価公示の照会(国土交通省 不動産情報ライブラリ API) | **キー発行に審査があり即時性が低い**。キーは事前に申請しておき、発行され次第いずれかの Day と差し替えて投入する。住まいテーマとして強力な次期候補 |
| ~~`estat-stats`~~ (採用済み) | 政府統計の統計表検索(e-Stat API、無料appId) | **2026-09-13に採用**。calil-books方式のキー前提スキルとして実装。下の「追加採用」参照 |
| `dataportal-search` | data.go.jp のデータセット横断検索(CKAN互換API) | メタ的なスキル。estat-stats と同じく性格がデータ基盤寄り |
| `amedas-weather` | アメダス最新観測値の照会(気象庁 防災情報 JSON) | Day 2 の jma-weather とテーマが近い(観測 vs 予報の違いはある)。Week 2 の拡張候補。2026-09-11 `latest_time.txt` 実測200 |
| `hazard-map` | 洪水・土砂災害などのハザード情報の照会(国土数値情報/ハザードマップポータル) | **タイル配信の利用規約確認が先**。規約上問題なければ採用可 |

上記以外のアイデアは issue テンプレート「スキル追加の提案」から。採用・不採用の判断はこのファイルに記録する。

---

## Roadmap (English summary)

Adopted schedule for Days 7-30 of the 30-day build-in-public challenge, decided 2026-09-11 by merging the plan announced in the Day 1 Qiita article with the verified candidate list. Every skill follows the repo's inclusion rules: no login or paid key (free instant API keys are OK), official APIs or public datasets only, read-only lookups and calculations. A skill ships only after its commands are tested for real, and every adoption is recorded here and in the changelog.

- **Week 2** (Day 8-13): `wareki`, `rokuyo`, `zipcode-lookup`, `yubin-fee`, `amagumo`, `bosai-typhoon` (Day 7: reflection)
- **Week 3** (Day 15-20): `volcano`, `shelter-lookup`, `river-level`, `air-quality`, `heatstroke`, `address-normalize` (Day 14: reflection). Disaster-heavy by design: September is typhoon season in Japan
- **Week 4** (Day 22-28): `odpt-transit`, `ndl-books`, `aozora`, `kokkai`, `egov-laws`, `withholding-tax`, `garbage-day` (Day 21: reflection, Day 29: v1.0.0 release, Day 30: wrap-up)
- **Rejected**: `station-finder` (superseded by `odpt-transit`), `nenkin` (calculation pattern duplicates `furusato-nozei`)
- **Backlog**: `reinfolib-prices` (waiting on API key review; apply in advance and swap in once issued), `estat-stats`, `dataportal-search`, `amedas-weather`, `hazard-map` (tile terms of use must be checked first)
