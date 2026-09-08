# bosai-alert ガイド

気象庁の防災情報を公開JSONから取得するスキル。APIキー・ログイン不要。

## エンドポイント一覧

| 用途 | URL |
| --- | --- |
| 地震一覧(最新) | `https://www.jma.go.jp/bosai/quake/data/list.json` |
| 地震の詳細 | `https://www.jma.go.jp/bosai/quake/data/{一覧のjsonフィールド}` |
| 警報・注意報 | `https://www.jma.go.jp/bosai/warning/data/warning/{officesコード}.json` |
| 津波情報一覧 | `https://www.jma.go.jp/bosai/tsunami/data/list.json` |
| エリア定義 | `https://www.jma.go.jp/bosai/common/const/area.json` |

## 使い方の例

「さっきの地震、震度どのくらい?」と聞かれたら:

1. `list.json` を取得し、先頭(最新)のイベントを見る
2. `maxi`(最大震度)、`anm`(震源地)、`mag`、`at`(発生時刻)を答える
3. 地域ごとの震度が必要なら `json` フィールドの詳細を取得し、`Body.Intensity.Observation` を読む

## つまずきポイント

- **詳細URLはフィールドから取る**: 詳細JSONのファイル名は一覧の `json` フィールドに入っている。自分でURLを組み立てない。
- **震度の表記**: `5-` / `6+` のような表記はそのまま「5弱」「6強」と読む。
- **緊急時の案内**: 避難判断には必ず公式発表を確認するよう添える。
