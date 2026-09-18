---
name: shelter-lookup
description: 国土地理院の指定緊急避難場所・指定避難所データ(全国、市町村が指定した公式データ)をダウンロードして避難所を検索する。避難所、避難場所、ハザード時の逃げ場、災害種別ごとの避難場所の質問に対応。APIキー・ログイン不要。ハザードマップの範囲判定や浸水深の計算は対象外。
license: MIT
metadata:
  category: disaster
  locale: ja-JP
---

# shelter-lookup

国土地理院の「避難所等データダウンロードサイト」が公開する、市町村長指定の指定緊急避難場所・指定避難所データをダウンロードして検索するスキル。APIキー・ログイン不要。国土数値情報の避難施設データ(P20)は2012年度版で古いため使わない(後述)。

**実測日: 2026-09-19。以下のURL・構造・行数はすべて当日の実測で確認。**

## ダウンロード元

公開ページ: https://hinanmap.gsi.go.jp/hinanjocp/hinanbasho/koukaidate.html (国土地理院 指定緊急避難場所・指定避難所データ)

全国データは2系統ある(いずれもUTF-8 BOMつきCSV。GeoJSON版も同階層の `geoJSON/` にある)。

| データ | URL | 実測サイズ |
| --- | --- | --- |
| 指定避難所 | `https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/csv/mergeFromCity_1.csv` | 約11.7MB |
| 指定緊急避難場所(災害種別フラグつき) | `https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/csv/mergeFromCity_2.csv` | 約17.0MB |

```bash
curl -sm 120 -O https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/csv/mergeFromCity_2.csv
```

## CSVの読み方

### 指定避難所(mergeFromCity_1.csv)

列: `NO,共通ID,都道府県名及び市町村名,施設・場所名,住所,指定緊急避難場所との住所同一,その他市町村長が必要と認める事項,受入対象者,緯度,経度,備考`

### 指定緊急避難場所(mergeFromCity_2.csv)

列: `NO,共通ID,都道府県名及び市町村名,施設・場所名,住所,洪水,崖崩れ、土石流及び地滑り,高潮,地震,津波,大規模な火事,内水氾濫,火山現象,指定避難所との住所同一,緯度,経度,備考`

災害種別の列は `1` が「その災害の避難場所として指定されている」、空欄は対象外。**災害種別を必ず確認する**: 洪水の避難場所が津波の避難場所とは限らない。

### 検索例

```bash
# 住所・施設名の部分一致 (ヘッダ行を落とす)
grep '千代田区' mergeFromCity_2.csv | head -5
# 津波指定のある施設だけ (津波列は9列目)
awk -F, '$9==1' mergeFromCity_2.csv | head -5
```

### データの新しさを確認する

市町村ごとのデータ更新日は公開ページと同じサーバの一覧CSVで分かる。

```bash
curl -s https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/publicHistoryCSV/publicHistoryListData.csv | head -5
```

`市町村コード,市町村名,初回公開日,データ更新日` の形式。2026-09-19実測では 2026-09-10 更新の自治体があった。**回答には「この市町村のデータは○年○月更新」と更新日を添える。**

## エラー・失敗時の対応

- **市町村ごとの個別ファイルは404**: `csv/<市町村コード>.csv` のような個別ファイルは2026-09-19実測で404(公開ページはブラウザ内でZIPを組み立てる方式)。直リンクを推測で書かず、全国ファイルをダウンロードしてgrepする。
- **文字化け**: ファイルはUTF-8(BOMつき)。化けたらShift_JIS系の別データ(国土数値情報など)を掴んでいる可能性が高い。
- **国土数値情報 P20(避難施設データ)に注意**: 検索で先に出てくるが最新版は2012年度版(2013年作製)で、現在の指定状況を反映しない。避難所の検索には使わず、必ず国土地理院の上記データを使う。2026-09-19に P20-12_31_GML.zip (鳥取県) をダウンロードして内容が2013年作製であることを実測確認。

## 注意

- 指定緊急避難場所は災害種別ごとの指定。**場所の名前だけでなく、何の災害に対する指定かを必ず併記する。**
- 指定の主体は市町村長。データの更新日は国土地理院DBの更新日であり、市町村長の指定日とは異なる(公開ページの注記)。
- 緯度経度の測地系は公開ページ・メタデータに従う。距離計算に使う場合は測地系を確認する。
- 避難の判断自体(今避難すべきか)はこのスキルの対象外。気象庁の警報等は bosai-alert、自治体の避難情報は公式発表を案内する。

## English summary

Downloads and searches Japan's official designated emergency evacuation site and shelter lists published by the Geospatial Information Authority of Japan (GSI). Two nationwide CSVs (UTF-8 with BOM): mergeFromCity_1.csv (designated shelters, ~11.7MB) and mergeFromCity_2.csv (designated emergency evacuation sites with per-hazard flags for flood, landslide, storm surge, earthquake, tsunami, fire, inland flooding, volcanic activity, ~17.0MB). GeoJSON versions exist under geoJSON/. Per-municipality update dates are in publicHistoryCSV/publicHistoryListData.csv. No API key or login. Verified live on 2026-09-19. Do NOT use the older Kokudo Suchi Joho P20 dataset (2012 edition, confirmed stale); always state which hazard a site is designated for and the municipality's data update date.
