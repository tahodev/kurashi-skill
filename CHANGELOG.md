# Changelog

このファイルは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) の形式にしたがう。バージョン付けは [SemVer](https://semver.org/lang/ja/) ベース。

## 更新ルール(メンテナ向け)

- **スキルを追加・削除したとき**: 対象バージョンの `Added` / `Removed` にスキル名と概要を1行で記録する。
- **スキルが使うエンドポイント・データソース・計算式を変えたとき**: `Changed` に新旧のURLや式を記録する。外部データの仕様変更への追従もここ。
- **税率・祝日CSVなど外部データの「時点」が変わったとき**: 該当スキル内の基準日注記とあわせて `Changed` に記録する。
- CHANGELOG を更新したら、リリース時に git tag と GitHub Release を同じバージョンで切る(現状は手動)。

## [Unreleased]

### Added
- 新スキル6個を追加(Day 8-13): `wareki`(和暦⇄西暦変換)、`rokuyo`(六曜計算、国立天文台暦要項ベースの旧暦テーブル内蔵)、`zipcode-lookup`(日本郵便KEN_ALLによる郵便番号検索)、`yubin-fee`(郵便料金表、2024-10-01改定を2026-09-11に確認)、`amagumo`(雨雲レーダータイル)、`bosai-typhoon`(台風情報の有無確認、非発生時404を平時として扱う)
- 各SKILL.mdに失敗時の対応セクション(HTTPエラー、空配列とエラーの区別、ポーリング上限、文字コード変換の代替手段、タイムアウト、ユーザーへの伝え方)を追加
- CONTRIBUTING.md、issueテンプレート、AGENTS.md を追加
- 各SKILL.mdに英語サマリーセクションを追加
- ヘルスチェックCI(`.github/workflows/health-check.yml`): SKILL.mdのURLチェック(`scripts/check-urls.sh`)・フロントマターリント(`scripts/lint-skills.sh`)・失敗時の自動issue起票
- 各スキルのdescriptionにルーティングキーワードと対象外スコープの境界を追加
- README に30日間の公開開発(build in public)チャレンジ節、シールエンブレムのヘッダーと紹介サイトへのリンク、CI・ライセンスバッジを追加。`.gitignore` を追加
- docs/install.md にクリーン環境でのインストール検証手順を追加
- ROADMAP.md を追加(30日チャレンジ Day 7-30 のスキル候補一覧)

### Changed
- ROADMAP.md に Day 7-30 の採用スケジュールを記録(Day 1 記事の案と検証済み候補一覧をマージして 2026-09-11 に決定)。不採用(`station-finder` / `nenkin`)とバックログ(`reinfolib-prices` / `estat-stats` / `dataportal-search` / `amedas-weather` / `hazard-map`)の判断理由も明記
- furusato-nozei: 給与所得控除・基礎控除を令和7年分以降の現行値に更新し、各税率表に基準日(2026年9月時点)と国税庁・総務省の公式URLを明記
- docs/features の各ガイドを要約に整理し、SKILL.md を正(カノニカル)とする方針を明記
- health-check を push / pull_request でも実行するように変更(失敗時の自動issue起票は schedule / 手動実行時のみ)
- lint-skills.sh: CONTRIBUTING.md で必須としている `metadata.category` / `metadata.locale` を必須項目として検査するように変更
- check-urls.sh: チェック対象を README.md と docs/**/*.md に拡大し、期限切れが前提の実例URLを除外する `EXCLUDE_URLS` の仕組みを追加

### Fixed
- bosai-alert: 日付入りの地震詳細JSONの実例URLが期限切れで404になりCIを壊す問題を、歴史的な例である注記とURLチェック除外で解消
- japan-holidays: curl フォールバックコマンドの重複した `-s` オプションを修正

## [0.1.0] - 2026-09-09

初回リリース。ログイン不要で安全に使える照会・計算系スキル5件を収録。

### Added
- `jma-weather` - 気象庁の公開JSONから天気予報(天気・降水確率・気温)を取得
- `bosai-alert` - 気象庁の防災情報(地震一覧と詳細、警報・注意報、津波情報)を取得
- `japan-holidays` - 内閣府の公式CSVから祝日・振替休日・国民の休日の照会と連休計算
- `furusato-nozei` - 給与収入や課税所得からふるさと納税の寄附上限額の目安を計算(API不要)
- `calil-books` - カーリル図書館APIで図書館の蔵書と貸出状況を検索(無料APIキー)

[Unreleased]: https://github.com/tahodev/kurashi-skill/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/tahodev/kurashi-skill/releases/tag/v0.1.0
