# Changelog

このファイルは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) の形式にしたがう。バージョン付けは [SemVer](https://semver.org/lang/ja/) ベース。

## 更新ルール(メンテナ向け)

- **スキルを追加・削除したとき**: 対象バージョンの `Added` / `Removed` にスキル名と概要を1行で記録する。
- **スキルが使うエンドポイント・データソース・計算式を変えたとき**: `Changed` に新旧のURLや式を記録する。外部データの仕様変更への追従もここ。
- **税率・祝日CSVなど外部データの「時点」が変わったとき**: 該当スキル内の基準日注記とあわせて `Changed` に記録する。
- CHANGELOG を更新したら、リリース時に git tag と GitHub Release を同じバージョンで切る(現状は手動)。

## [Unreleased]

### Added
- 各SKILL.mdに失敗時の対応セクション(HTTPエラー、空配列とエラーの区別、ポーリング上限、文字コード変換の代替手段、タイムアウト、ユーザーへの伝え方)を追加
- CONTRIBUTING.md、issueテンプレート、AGENTS.md を追加

### Changed
- furusato-nozei: 給与所得控除・基礎控除を令和7年分以降の現行値に更新し、各税率表に基準日(2026年9月時点)と国税庁・総務省の公式URLを明記

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
