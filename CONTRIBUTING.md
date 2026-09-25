# コントリビューションガイド

kurashi-skill への貢献に興味を持ってくれてありがとうございます。スキルの追加提案、不具合報告、ドキュメントの改善、すべて歓迎です。

## スキルの採用基準

新しいスキルは、次の条件をすべて満たすものだけを収録します。

1. **ログイン不要・課金不要**: 利用者本人のアカウントや有料キーなしで使えること。無料で即発行できるAPIキー(calil-books方式)は可。
2. **公式API・公開データのみ**: 官公庁や事業者が公開する公式のAPI・データを使うこと。スクレイピング対策のあるサービス(メルカリ、SUUMO、乗換案内、食べログなど)は対象外。
   - 例外: `eew-monitor` は非公式リレー(wolfx JMA-API、P2P地震情報)を使う。EEWの公式の機械可読な配信経路が一般に開かれていないためで、スキル内で「非公式リレーであること」と「確認は気象庁の公式情報で」を明記する。例外は原則この1件のみ。
3. **照会・計算のみ**: 予約・購入・投稿など、外部の状態を変更する操作を含まないこと。

## 収録前の実測検証(必須)

- ドキュメントの記載ではなく、**実際にコマンドを実行して動いたものだけ**を収録する。SKILL.mdに書くcurlコマンドやURLは、投稿前にすべて実測する。
- 実測した日付と、失敗時の挙動(404、5xx、空のレスポンス)も確認し、「エラー・失敗時の対応」セクションに書く。
- 外部データに基準日があるもの(税率、料金表など)は、基準日と公式の根拠URLを本文に明記する。

## SKILL.md の形式

- スキルはリポジトリ直下に1ディレクトリ1スキルで置き、各ディレクトリに `SKILL.md` を置く(`npx skills add` 互換)。
- フロントマター: `name`, `description`, `license`, `metadata`(category, locale) を必須とする。既存スキルを参考にする。
- 本文は日本語を基本とし、以下の構成を目安にする:
  1. 何ができるか(1〜2文)
  2. 基本の流れ(コマンド例つき)
  3. レスポンスの読み方(API・データ取得型スキルの場合。純粋計算スキルでは計算の根拠を示す)
  4. エラー・失敗時の対応
  5. 注意事項(ユーザーに必ず伝えるべき前提)
- 補足がある場合は `docs/features/<スキル名>.md` にガイドを置き、READMEの表からリンクする。

## ヘルパースクリプト(lookup.py)

- 変換・絞り込みの手順が2つ以上、またはCSVのパースが必要なスキルは、手順を `<スキル名>/lookup.py` に切り出す(標準ライブラリのみ)。単純なcurl+grepで済むスキルはSKILL.md内のインライン例のまま。
- 引数の規約(既存スキルと合わせる):
  - 検索: `--keyword`(名称の部分一致) / `--pref`(都道府県コード) / `--station`(地点コード完全一致)
  - 位置: `--lat` / `--lon`(小数度。最寄り地点の検索に使う)
  - キャッシュ: `--cache-dir`(既定 `~/.cache/kurashi-skill/<スキル名>/`)、`--refresh` で再取得
- 新しいヘルパーには必ずテストを添える: `<スキル名>/tests/test_lookup.py` + `tests/fixtures/` の固定データで、パースと絞り込みの単体テストを書く(shelter-lookup、air-quality、heatstroke を参照)。

## 変更の記録

- スキルの追加・削除、エンドポイントやデータソース、計算式の変更は、必ず [CHANGELOG.md](CHANGELOG.md) に記録する(冒頭の更新ルール参照)。
- 税率・料金・暦表などを内蔵するスキルは、frontmatter の `metadata` に `data_as_of`、`valid_through`、`source_version` を3点セットで記録する。公式の終了日がない場合も、遅くとも1年後を再検証期限 (`valid_through`) にする。
- `valid_through` の30日前からCIは失敗する。更新時は公式一次資料を再確認し、日付・版と `fixtures/static-data.json` の核心行を一緒に更新する。期限だけを延ばさない。

## 不具合・提案

- 不具合は issue テンプレート「不具合報告」、スキルの追加提案は「スキル追加の提案」から issue を立ててください。
- プルリクエストも歓迎です。大きな変更は先に issue で相談してもらえると助かります。

---

## Contributing (English summary)

We welcome skill proposals, bug reports, and doc improvements. New skills must be (1) usable without a login or paid key, (2) built only on official APIs or public datasets, and (3) read-only (lookups and calculations, no state changes). Every command in a SKILL.md must be tested for real before merging, and each SKILL.md must include a failure-handling section. Record user-visible changes in [CHANGELOG.md](CHANGELOG.md).
