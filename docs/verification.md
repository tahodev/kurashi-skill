# 検証範囲 / Verification

27スキル。10のPython helperには67単体テスト、コア18スキルには固定fixtureの
スモークテストがある。両者は重複し、27+18の機能を意味しない。
`koyobun-check`は知識チェックリストで実行テストの対象外。

## 何を検証するか

- frontmatter/YAML/Markdown(既存のHTML見出し・長文・裸の出典URLは明示的に許容)、相対リンクと見出し、スキル一覧とPagesの一致
- 静的データの再検証期限と、既知の改定日の効力終了
- 文書コードブロックの文法、一部の自己完結するオフライン例
- helperのfixtureパース・絞り込み・エラー処理
- 公開URLのHTTP/形式。動的URLは実データで補い、曖昧な到達を成功扱いしない
- ゆうパック東京発49料金を公式表と比較するlive probe

固定fixtureが通っても現在のAPIが同じとは限らない。URLの200は計算・防災判断の
正しさを証明しない。WARN/SKIPは未検証として明示する。

## ローカル再現

```bash
npm ci --ignore-scripts
python3 -m pip install -r requirements-dev.txt
bash scripts/lint-skills.sh
npm run lint:markdown
python3 scripts/check-yaml-links.py
python3 scripts/check-docs-drift.py
python3 scripts/check-static-data.py
python3 scripts/check-measured-date.py
python3 scripts/check-code-blocks.py
python3 tests/test-core-skills.py
python3 -m unittest discover -s tests/checks
for d in */tests; do python3 -m unittest discover -s "$d" || exit 1; done
python3 scripts/check-urls.py
```

`valid_through`は再検証期限(30日前から失敗)。既知の改定日は `effective_until`
(その日以降は無効、30日前から更新を要求)にも記録する。期限だけを延ばさず、
公式表とfixtureを更新する。静的スキル以外は実測日が必要。

## インストール実測

2026-10-13、隔離した新規プロジェクトで `npx skills add` のlocal path/`--copy`/Codex指定を実行。10helperすべてにSKILL.mdとlookup.pyが同梱された。グローバルの既存設定は変更していない。

## Pages

mainの`site/`が正本。`scripts/build-pages.py`でREADMEから一覧を生成し、
Pages workflowでartifactをアップロード・配信する。GitHub PagesのSourceを
GitHub Actionsに切り替える必要がある。旧gh-pagesは履歴として残し、二重編集しない。

## English

Fixtures, live URL checks and real scenario verification are different layers. Green CI
is not a guarantee that every scenario or source is current. The Pages workflow requires
GitHub Actions to be selected as the repository's Pages publishing source.
