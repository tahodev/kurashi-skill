---
name: zipcode-lookup
description: 日本郵便の公式データで郵便番号と住所を相互検索する。郵便番号、〒、住所から郵便番号、郵便番号から住所、町域の検索に対応。公式CSVをダウンロードしてローカル検索するのでAPIキー・ログイン不要。宛名印刷・配送・ゆうびんID変換は対象外。
license: MIT
metadata:
  category: address
  locale: ja-JP
---

# zipcode-lookup

日本郵便が公開する郵便番号データ(UTF-8版 KEN_ALL)をダウンロードして、郵便番号⇄住所をローカル検索するスキル。APIキー不要。約12万件の全データを手元に持つので、件数制限なく繰り返し検索できる。

## 基本の流れ

### 1. データをダウンロードする

ダウンロードページはここ(2026-09-11にページ構造を確認):

```bash
curl -sm 30 -L -o utf-zip.html https://www.post.japanpost.jp/zipcode/dl/utf-zip.html
```

ページ内の「全国一括」のリンク(2026-09-11時点で `utf/zip/utf_ken_all.zip`)を取り出してダウンロードする。

```bash
href=$(grep -oE 'utf/zip/utf_ken_all\.zip' utf-zip.html | head -1)
curl -sm 120 -L -o utf_ken_all.zip "https://www.post.japanpost.jp/zipcode/dl/${href}"
unzip -o utf_ken_all.zip   # KEN_ALL.CSV (UTF-8) が出てくる
```

**直リンクを推測で書かない。** 2026-09-11の実測では、データセンター系IPからのアクセスではzipの直リンクがすべて404を返し、ダウンロードページ自体は200だった。必ずページを経由して、そのとき記載されているリンクを使う。

差分だけ欲しい場合は、同じページに「更新データ(追加・廃止・変更)」の月次zipがある。

### 2. 検索する

```bash
# 郵便番号 → 住所 (ハイフンなし7桁で検索)
grep '^1000001,' KEN_ALL.CSV   # 千代田区千代田(皇居)

# 住所 → 郵便番号 (部分一致)
grep '千代田区丸の内' KEN_ALL.CSV
```

## 読み方(CSVの列)

1行15列。主要な列は: 1列目=全国地方公共団体コード、3列目=郵便番号(7桁)、7列目=都道府県名、8列目=市区町村名、9列目=町域名(4〜6列目はそれぞれのカナ表記)。

- 町域名が「以下に掲載がない場合」の行は、その市区町村で町域の記載がない地域すべてに対応する。
- 1つの郵便番号に複数行(複数町域)が対応することがある。最初の1行で打ち切らず、該当行をすべて返す。

## 更新サイクル

郵便番号データは月次で更新される(月末に当月分が公開)。検索のたびに取り直す必要はないが、「何月分のデータか」をユーザーに伝えられるように、ダウンロード日を控えておく。古いデータで廃止・変更された番号を案内しないよう、月1回程度は取り直す。

## エラー・失敗時の対応

- **zipが404/403/タイムアウト**: 推測したURLを叩いていないか確認し、ダウンロードページからリンクを取り直す。それでも駄目なら「日本郵便のサイトからデータを取得できなかった」と明示し、ページのURLを案内する。
- **住所が見つからない**: 町域名は郵便事業上の表記で、住居表示と異なることがある。丁目・番地を削って町域名の部分一致で探し直す。大字・小字はデータに含まれないことがある。
- **文字化け**: UTF-8版を使っている限り化けない。もし文字化けするならJIS版(`ken_all.zip`、Shift_JIS)を落としている可能性が高い。UTF-8版を取り直す。

## 注意

- 返す住所は郵便番号のための公式表記であり、住居表示・登記上の表記と一致しないことがある。「郵便番号データ上の表記」であることを必要に応じて伝える。
- データの基準日(何月分か)を添えて答える。

## English summary

Look up Japanese postal codes and addresses both ways using Japan Post's official KEN_ALL dataset (UTF-8 edition). No API key or login: download the national zip from the official download page and search locally. Never guess the zip's direct URL - datacenter IPs were served 404s for direct zip links on 2026-09-11 while the page itself returned 200; always extract the current link from the page. Data is updated monthly; tell the user which month's dataset you searched. Address spellings are Japan Post's postal notation, which can differ from residential addressing.
