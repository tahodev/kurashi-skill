# スターターガイド: 目的別おすすめパック

どのスキルから入れるか迷ったときのためのガイドです。各スキルは1個ずつ独立して動くので、目的に合うパックだけを選んでインストールできます。

インストールの前提条件(Node.js 18以上など)や非対話環境での注意は [インストールガイド](install.md) を参照してください。各スキルの正本は `<スキル名>/SKILL.md` です。

## おすすめパック

### 生活基本パック

毎日の暮らしで出番が多いセットです。天気、祝日、ごみ収集日、郵便番号、郵便料金をカバーします。すべてキー不要。

| スキル | できること |
| --- | --- |
| `jma-weather` | 天気・降水確率・気温の予報 |
| `amagumo` | 今の雨の強さと30〜60分先の見通し |
| `japan-holidays` | 祝日・振替休日・連休の計算 |
| `garbage-day` | 地区ごとのごみ収集日(対応市区町村の公開CSV) |
| `zipcode-lookup` | 郵便番号⇄住所の検索 |
| `yubin-fee` | 郵便料金の計算 |

```bash
npx --yes skills add tahodev/kurashi-skill --skill jma-weather --skill amagumo --skill japan-holidays --skill garbage-day --skill zipcode-lookup --skill yubin-fee -g -y
```

### 防災パック

地震・津波・台風・火山の公式発表と避難所検索のセットです。すべてキー不要。

| スキル | できること |
| --- | --- |
| `bosai-alert` | 地震一覧と詳細、警報・注意報、津波情報 |
| `eew-monitor` | 緊急地震速報の発表状況(非公式中継API。最終確認は必ず気象庁の発表で) |
| `bosai-typhoon` | 発生中の台風の有無 |
| `volcano` | 噴火速報・噴火警報・火山解説情報 |
| `shelter-lookup` | 指定避難所の検索 |

```bash
npx --yes skills add tahodev/kurashi-skill --skill bosai-alert --skill eew-monitor --skill bosai-typhoon --skill volcano --skill shelter-lookup -g -y
```

### 行政・文書パック

ふるさと納税の目安計算、和暦変換、公用文の校閲など、役所・文書まわりのセットです。すべてキー不要。

| スキル | できること |
| --- | --- |
| `furusato-nozei` | ふるさと納税の寄附上限額の目安計算 |
| `wareki` | 西暦⇄和暦の相互変換 |
| `rokuyo` | 六曜(大安・仏滅など)の確認 |
| `koyobun-check` | 公用文の表記校閲 |
| `zipcode-lookup` | 郵便番号⇄住所の検索 |
| `yubin-fee` | 郵便料金の計算 |

```bash
npx --yes skills add tahodev/kurashi-skill --skill furusato-nozei --skill wareki --skill rokuyo --skill koyobun-check --skill zipcode-lookup --skill yubin-fee -g -y
```

### データ調査パック

政府統計や図書館蔵書を調べるセットです。無料のAPIキーが必要なスキルはこのパックに集まっています(下の表参照)。

| スキル | できること | キー |
| --- | --- | --- |
| `estat-stats` | e-Stat APIで統計表の検索・取得 | 要無料キー |
| `calil-books` | 図書館の蔵書と貸出状況の検索 | 要無料キー |
| `zipcode-lookup` | 郵便番号⇄住所のローカル検索 | 不要 |

```bash
npx --yes skills add tahodev/kurashi-skill --skill estat-stats --skill calil-books --skill zipcode-lookup -g -y
```

## 無料キーが必要なスキル

キーが必要なのは次の2スキルだけです。どちらも無料で即時発行できます。それ以外のスキルはキーなしで使えます。

| スキル | キー | 発行ページ(無料) | 環境変数の例 |
| --- | --- | --- | --- |
| `calil-books` | カーリルAPIキー | https://calil.jp/api/dashboard/ | `CALIL_APPKEY` |
| `estat-stats` | e-Stat appId | https://www.e-stat.go.jp/mypage/user/preregister | `ESTAT_APP_ID` |

キーはチャットやコード、コミットに書かず、環境変数に入れて使ってください。発行手順の詳細は [calil-books ガイド](features/calil-books.md) と [estat-stats ガイド](features/estat-stats.md) にあります。

## 代表質問10

このままエージェントに聞ける質問例です。キーが必要なスキルには印を付けています。

| # | 質問 | 対応スキル | パック |
| --- | --- | --- | --- |
| 1 | 明日の東京の天気と降水確率は? | `jma-weather` | 生活基本 |
| 2 | 今の雨、あと30分くらいで止みそう? | `amagumo` | 生活基本 |
| 3 | 次の連休はいつ? | `japan-holidays` | 生活基本 |
| 4 | うちの地区のごみ収集日は? | `garbage-day` | 生活基本 |
| 5 | 今、警報や注意報が出ている地域はある? | `bosai-alert` | 防災 |
| 6 | 今、発生している台風はある? | `bosai-typhoon` | 防災 |
| 7 | 最寄りの指定避難所はどこ? | `shelter-lookup` | 防災 |
| 8 | 年収600万円なら、ふるさと納税の上限はいくらくらい? | `furusato-nozei` | 行政・文書 |
| 9 | 最新の人口統計を政府統計から調べて | `estat-stats` (要無料キー) | データ調査 |
| 10 | 近くの図書館にこの本はある? | `calil-books` (要無料キー) | データ調査 |

---

## Starter guide (English summary)

Recommended install sets by purpose. Each skill works on its own, so you can install only the pack you need. The canonical text is the Japanese version above.

| Pack | Skills | Keys |
| --- | --- | --- |
| Daily-life basics | `jma-weather`, `amagumo`, `japan-holidays`, `garbage-day`, `zipcode-lookup`, `yubin-fee` | None |
| Disaster readiness | `bosai-alert`, `eew-monitor`, `bosai-typhoon`, `volcano`, `shelter-lookup` | None |
| Admin & documents | `furusato-nozei`, `wareki`, `rokuyo`, `koyobun-check`, `zipcode-lookup`, `yubin-fee` | None |
| Data research | `estat-stats`, `calil-books`, `zipcode-lookup` | Free key for `estat-stats` and `calil-books` |

Install a pack with one command, repeating `--skill` (verified 2026-09-19):

```bash
npx --yes skills add tahodev/kurashi-skill --skill jma-weather --skill japan-holidays -g -y
```

Only two skills need a (free) key: `calil-books` (Calil API key from https://calil.jp/api/dashboard/) and `estat-stats` (e-Stat appId from https://www.e-stat.go.jp/mypage/user/preregister). Every other skill works with no key. The Japanese section above also lists ten ready-to-ask sample questions mapped to each pack.
