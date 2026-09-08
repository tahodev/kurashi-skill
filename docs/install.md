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
    features/<skill>.md   # スキルごとの概要ガイド(正本は各 SKILL.md)
```


## クリーン環境での検証結果 (2026-09-09 実測)

Node.js v22 / npm 10.9、空のHOME・空のnpmキャッシュで上記コマンドを実際に実行した結果。

### `--all -g` (全スキル)

- 5スキルすべてが `~/.agents/skills/<skill名>/SKILL.md` にインストールされる。
- Claude Code など各エージェントのディレクトリ (例: `~/.claude/skills/<skill名>/`) にも配置される。
- `Eve` と `PromptScript` の2ターゲットは「global skill installation非対応」でスキップされる。これはインストーラ側の仕様で、スキル自体の問題ではない。

### `--skill jma-weather -g` (1スキル)

- 対話環境ではどのエージェントに入れるかの選択プロンプトが出る。
- **非対話環境 (CI・SSHなどTTYなし) ではプロンプトがキャンセルされ、何もインストールされない。** その場合は `-y` を付ける (または `--agent <名前>` / `--agent '*'` でエージェントを指定する):

```bash
npx --yes skills add tahodev/kurashi-skill --skill jma-weather -g -y
```

- `-y` 付きで `~/.agents/skills/jma-weather/SKILL.md` などに正しく配置されることを確認済み。

### 確認方法

```bash
ls ~/.agents/skills/          # インストールされたスキル一覧
cat ~/.agents/skills/jma-weather/SKILL.md
```

## アンインストール

`npx skills add` でインストールしたスキルは、エージェントのスキルディレクトリから該当ディレクトリを削除すれば取り除けます。

## データの出どころと注意

- 気象庁の公開JSON (`www.jma.go.jp/bosai/...`) — APIキー不要
- 内閣府 国民の祝日・休日CSV (`www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`) — キー不要
- カーリル図書館API (`api.calil.jp`) — 無料のAPIキーが必要 ([calil-books ガイド](features/calil-books.md) 参照)

各サービスの利用規約に従って使ってください。短時間に大量のリクエストを送らないでください。
