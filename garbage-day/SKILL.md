---
name: garbage-day
description: 5374(ゴミナシ)形式の公開データで自治体のごみ収集日を調べる。ごみの日、収集日、燃えるごみ、資源ごみの曜日に対応。対象外の自治体や最新の収集カレンダーの確証が必要な場合は、自治体の公式案内を案内する。
license: MIT
metadata:
  category: living
  locale: ja-JP
---

# garbage-day

5374.jp 形式(Code for Kanazawa発のオープンソース)で公開されている自治体のごみ収集日データを読み、地区・ごみの種類ごとの収集曜日を答えるスキル。APIキー・ログイン不要。

> **データの性質**: 5374のデータはシビックテックのボランティアが自治体の公表情報をもとにCSV化したもので、自治体公式の配信ではない。収集日は変更されることがあるため、引っ越し直後や祝日・年末年始の確認など確実性が必要な場面では、自治体の公式案内もあわせて確認するよう案内する。

## 5374形式のデータ構造

各地域の5374サイトは `data/` ディレクトリのCSV5本で動く(2026-09-13に codeforkanazawa-org/5374 の LOCALIZE.md と実データで確認):

- `area_days.csv`: **本体**。地区名、センター名、3列目以降にごみのカテゴリ(燃やすごみ、資源など)ごとの収集曜日
- `target.csv`: カテゴリ別の品目一覧(「この品物は何ごみ?」を引く表)
- `description.csv`: カテゴリの説明(袋の指定など)
- `center.csv`: 収集センターの休止期間(年末年始など)
- `remarks.csv`: 注意事項

### 収集曜日の書式(area_days.csv)

- `月 木` … 毎週月曜と木曜(半角スペース区切り)
- `月1` … 毎月第1月曜。`水2 水4` なら第2・第4水曜
- `20140301 20140325` … 不定期な日付の直接指定(YYYYMMDD)

実例(金沢市の `area_days.csv` 先頭、2026-09-13実測):

```csv
校下・地区,センター,燃やすごみ,燃やさないごみ,資源,あきびん
浅野川,東部管理センター,月 木,水4,火1 火3 火5,水2
```

## 公開データがある自治体(2026-09-13実測で到達確認)

GitHub上の raw CSV を直接読める。ブランチ名は自治体で異なる。

```bash
# 金沢市 (Code for Kanazawa 本家)
curl -s https://raw.githubusercontent.com/codeforkanazawa-org/5374/kanazawa/data/area_days.csv

# 美唄市(北海道)
curl -s https://raw.githubusercontent.com/govtech-bibai/5374-bibai/master/data/area_days.csv

# 松前町(北海道)
curl -s https://raw.githubusercontent.com/matsumaetown/5374/master/data/area_days.csv

# 笠間市(茨城県)
curl -s https://raw.githubusercontent.com/cfkasama/5374/master/data/area_days.csv

# 上砂川町(北海道)
curl -s https://raw.githubusercontent.com/Kamisunagawa-town/5374/master/data/area_days.csv

# 大分市
curl -s https://raw.githubusercontent.com/codeforoita/5374/gh-pages/data/area_days.csv
```

使い方の例:

```bash
# 金沢市で「浅野川」地区の収集日を引く
curl -s https://raw.githubusercontent.com/codeforkanazawa-org/5374/kanazawa/data/area_days.csv | grep '^浅野川,'
# -> 浅野川,東部管理センター,月 木,水4,火1 火3 火5,水2
#    = 燃やすごみ: 毎週月・木、燃やさないごみ: 第4水曜、資源: 第1・3・5火曜、あきびん: 第2水曜
```

地区名が分からない場合は、まず1列目の一覧を出して候補を見せる。

```bash
curl -s https://raw.githubusercontent.com/codeforkanazawa-org/5374/kanazawa/data/area_days.csv | cut -d, -f1
```

## 対象の自治体がない場合

5374の展開はボランティア次第で、主要都市を含めカバーされていない自治体が多い。対象データが見つからない場合は推測で答えず、次を案内する:

1. 自治体の公式サイトの「ごみ収集日」「収集カレンダー」ページ(地区名+「ごみ収集日」での検索)
2. 自治体のオープンデータカタログや data.go.jp での「ごみ 収集日」検索
3. 5374公式サイト ( http://5374.jp/ ) にある展開済み地域の案内。HTTPSは証明書が未設定で使えないため(2026-09-13実測、`*.github.com` の証明書が返りホスト名不一致)、httpでのアクセスになる

## 注意

- CSVの文字コードは自治体版により異なる。金沢市・美唄市はUTF-8(2026-09-13実測)だが、文字化けしたら `iconv -f SHIFT_JIS -t UTF-8` で変換する。
- ヘッダ行(カテゴリ名)は自治体で違う。答える前に必ず1行目を読んで列の意味を確認する。
- センター休止期間(center.csv)は更新が古いままのことがある(金沢市版は2022/2023年の日付が残っていた)。年末年始の質問には公式案内を優先する。
- 祝日の収集の有無は自治体のルール次第で、5374の曜日データだけでは分からない。公式案内を確認するよう添える。

## エラー・失敗時の対応

- **タイムアウトを付ける**: `curl -sm 30` のように必ず制限時間を付ける。
- **HTTP 404**: ブランチ名(kanazawa/master/gh-pages)かファイルパスの違いが主な原因。GitHubのリポジトリページで `data/` の有無を確認する。リポジトリ自体が消えている場合は、その自治体版は運用終了の可能性があるため公式案内に切り替える。
- **地区名が見つからない**: 丁目や字の表記ゆれ(「浅野川」と「浅野川町」など)を疑い、1列目の一覧から部分一致で候補を示す。それでもなければデータにない地区として、公式案内を案内する。推測で曜日を答えない。
- **HTTP 5xx / タイムアウト**: 1〜2回だけ再試行。直らなければGitHub側の障害の可能性として、自治体公式サイトの確認を案内する。

## English summary

Looks up municipal garbage collection days from 5374.jp-format open datasets (the Code for Kanazawa open-source model): one `area_days.csv` per city maps each district to weekly/nth-weekday collection days per garbage category. Verified live sources (2026-09-13): Kanazawa, Bibai, Matsumae, Kasama, Kamisunagawa and Oita on GitHub raw. The CSVs are volunteer-maintained, not official city feeds - for anything that must be certain (moving, holidays, year-end), point the user to the city's official garbage calendar. If a city has no 5374 dataset or a district is not found, say so and redirect to official sources instead of guessing.
