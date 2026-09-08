# インストールガイド

## 前提条件

- Node.js 18 以上 (`npx` が使えること)
- `npx skills add` に対応したコーディングエージェント (Claude Code、Codex、OpenCode など)

## インストール

```bash
# すべてのスキルをグローバルにインストール
npx --yes skills add tahodev/kurashi-skill --all -g

# 特定のスキルだけインストール
npx --yes skills add tahodev/kurashi-skill --skill jma-weather -g
npx --yes skills add tahodev/kurashi-skill --skill bosai-alert -g
npx --yes skills add tahodev/kurashi-skill --skill japan-holidays -g
npx --yes skills add tahodev/kurashi-skill --skill furusato-nozei -g
npx --yes skills add tahodev/kurashi-skill --skill calil-books -g
```

`-g` を外すと、カレントのプロジェクトだけにインストールされます。

## スキルの構成

各スキルはリポジトリ直下のディレクトリにある `SKILL.md` 1ファイルだけで動きます。追加のランタイムやプロキシサーバーは不要です。照会はすべて `curl` など一般的なHTTPクライアントで完結します。

```
kurashi-skill/
  jma-weather/SKILL.md
  bosai-alert/SKILL.md
  japan-holidays/SKILL.md
  furusato-nozei/SKILL.md
  calil-books/SKILL.md
  docs/
    install.md
    features/<skill>.md   # スキルごとの詳細ガイド
```

## アンインストール

`npx skills add` でインストールしたスキルは、エージェントのスキルディレクトリから該当ディレクトリを削除すれば取り除けます。

## データの出どころと注意

- 気象庁の公開JSON (`www.jma.go.jp/bosai/...`) — APIキー不要
- 内閣府 国民の祝日・休日CSV (`www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`) — キー不要
- カーリル図書館API (`api.calil.jp`) — 無料のAPIキーが必要 ([calil-books ガイド](features/calil-books.md) 参照)

各サービスの利用規約に従って使ってください。短時間に大量のリクエストを送らないでください。
