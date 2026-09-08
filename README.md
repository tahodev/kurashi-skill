# kurashi-skill

[![health-check](https://github.com/tahodev/kurashi-skill/actions/workflows/health-check.yml/badge.svg)](https://github.com/tahodev/kurashi-skill/actions/workflows/health-check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

日本での暮らしを手伝う、AIエージェント向けスキルコレクションです。
気象庁の公開データ、内閣府の祝日CSV、カーリル図書館APIなど、公式APIと公開データだけを使い、ログインなしで安全に使える照会系スキルを中心に集めています。

Claude Code、Codex、OpenCode など、`npx skills add` に対応したコーディングエージェントで使えます。

## できること

「ログイン」列は、利用者本人のアカウントやシークレットが必要かどうかだけを示します。

| できること | スキル名 | 説明 | ログイン | ドキュメント |
| --- | --- | --- | --- | --- |
| 日本の天気予報を調べる | `jma-weather` | 気象庁の公開JSONから天気・降水確率・気温の予報を取得 | 不要 | [jma-weather ガイド](docs/features/jma-weather.md) |
| 地震速報・気象警報を調べる | `bosai-alert` | 気象庁の防災情報(地震一覧と詳細、警報・注意報、津波情報)を取得 | 不要 | [bosai-alert ガイド](docs/features/bosai-alert.md) |
| 祝日・連休を調べる | `japan-holidays` | 内閣府の公式CSVから祝日・振替休日・国民の休日と連休を計算 | 不要 | [japan-holidays ガイド](docs/features/japan-holidays.md) |
| ふるさと納税の上限額を計算する | `furusato-nozei` | 給与収入や課税所得から寄附上限額の目安を計算(API不要) | 不要 | [furusato-nozei ガイド](docs/features/furusato-nozei.md) |
| 図書館の蔵書を検索する | `calil-books` | カーリル図書館APIで図書館の蔵書と貸出状況を検索 | APIキー(無料)が必要 | [calil-books ガイド](docs/features/calil-books.md) |

各スキルの**正本は `<スキル名>/SKILL.md`** です。`docs/features/` のガイドは概要版なので、詳細な手順・パラメータ・エラー対応は必ず SKILL.md を参照してください。

スコープについて:

- スクレイピング対策が強いサービス(メルカリ、SUUMO、乗換案内、食べログなど)は対象外です。
- 予約・購入・投稿など状態を変更する操作は扱いません。照会と計算だけです。
- 気象・防災情報は気象庁の発表データをそのまま取得します。最終的な判断には必ず公式発表を確認してください。

## インストール

```bash
# すべてのスキルをインストール
npx --yes skills add tahodev/kurashi-skill --all -g

# 特定のスキルだけインストール
npx --yes skills add tahodev/kurashi-skill --skill jma-weather -g
```

Node.js 18 以上と `npx` が必要です。詳しくは [インストールガイド](docs/install.md) を参照してください。

## 30日間の公開開発 (build in public) チャレンジ実施中

このリポジトリは、30日間の公開開発チャレンジとして育っています。1日1スキル、コミットがそのままQiitaの記事になる方式です。なお、制作パートナーのAIエージェント(Astra)のクオータが30日間持つかどうかが、実は最大のリスク要因だったりします。

| Day | 日付 | できごと |
| --- | --- | --- |
| 1 | 2026-09-09 | 宣言 & リポジトリ公開 (初期スキル5個) |

## English

**kurashi-skill** (暮らし, "kurashi" = everyday life) is a collection of AI-agent skills for daily life in Japan. It focuses on read-only lookups and calculations built only on official APIs and public datasets: no login walls, no scraping.

Works with any coding agent that supports `npx skills add` (Claude Code, Codex, OpenCode, ...).

### What you can do

| What you can do | Skill | Description | Login | Docs |
| --- | --- | --- | --- | --- |
| Look up weather forecasts in Japan | `jma-weather` | Weather, precipitation probability and temperature forecasts from the Japan Meteorological Agency's public JSON feeds | Not required | [jma-weather guide](docs/features/jma-weather.md) |
| Look up earthquake bulletins and weather warnings | `bosai-alert` | JMA disaster information: earthquake list and details, warnings/advisories, tsunami information | Not required | [bosai-alert guide](docs/features/bosai-alert.md) |
| Look up national holidays and long weekends | `japan-holidays` | Holiday, substitute-holiday and bridge-holiday calculation from the Cabinet Office's official CSV | Not required | [japan-holidays guide](docs/features/japan-holidays.md) |
| Estimate your furusato nozei donation cap | `furusato-nozei` | Pure-calculation estimate of the hometown-tax donation limit (no API needed) | Not required | [furusato-nozei guide](docs/features/furusato-nozei.md) |
| Search library holdings | `calil-books` | Library and book-availability search via the Calil API | Free API key required | [calil-books guide](docs/features/calil-books.md) |

The canonical source for each skill is its `<skill>/SKILL.md`. The guides under `docs/features/` are summaries only - always refer to SKILL.md for full procedures, parameters, and error handling.

Scope notes:

- Services with heavy anti-scraping (Mercari, SUUMO, transfer guides, Tabelog, ...) are out of scope.
- Nothing here changes state: no reservations, purchases, or posts. Lookups and calculations only.
- Weather and disaster data are JMA announcements as-is. Always confirm against official JMA bulletins before making decisions.

### Install

```bash
# Install every skill
npx --yes skills add tahodev/kurashi-skill --all -g

# Install a single skill
npx --yes skills add tahodev/kurashi-skill --skill jma-weather -g
```

Node.js 18+ and `npx` are required. See the [install guide](docs/install.md) for details.

### Building in public: a 30-day challenge

This repository is growing as a 30-day build-in-public challenge: one skill a day, with each commit doubling as a Qiita article. Frankly, the biggest risk factor is whether the quota of Astra - the AI agent co-authoring this series - survives all 30 days.

| Day | Date | What happened |
| --- | --- | --- |
| 1 | 2026-09-09 | Declaration & repository launch (initial 5 skills) |

## ライセンス / License

[MIT](LICENSE)
