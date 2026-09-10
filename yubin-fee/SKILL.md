---
name: yubin-fee
description: 日本郵便の郵便料金(定形・定形外・ミニレター・レターパック・スマートレター・はがき)を重量とサイズから調べる。切手代、郵便料金、何円の切手、送料の質問に対応。料金表はスキル内蔵(基準日明記)でAPIキー・ログイン不要。ゆうパック・ゆうメール・国際郵便・速達書留などのオプション料金は対象外。
license: MIT
metadata:
  category: postal
  locale: ja-JP
---

# yubin-fee

日本郵便の基本的な郵便料金を重量・サイズから調べるスキル。料金表を内蔵するので計算だけで答えられる。

**基準日: 2024-10-01の改定料金。2026-09-11に公式ページで現行であることを確認。**
根拠URL: 手紙(第一種) https://www.post.japanpost.jp/send/domestic/charge/list/one_two.html ／ はがき https://www.post.japanpost.jp/service/send/domestic/mail/postcard/

## 料金表

### 定形郵便物(長辺14〜23.5cm × 短辺9〜12cm、厚さ1cm以内、50g以内)

| 重量 | 料金 |
| --- | --- |
| 50g以内 | 110円 |

### 定形外郵便物(規格内: 長辺34cm・短辺25cm・厚さ3cm・1kg以内 ／ 規格外: 長辺60cm以内、長辺+短辺+厚さ90cm以内、4kg以内)

| 重量 | 規格内 | 規格外 |
| --- | --- | --- |
| 50g以内 | 140円 | 260円 |
| 100g以内 | 180円 | 290円 |
| 150g以内 | 270円 | 390円 |
| 250g以内 | 320円 | 450円 |
| 500g以内 | 510円 | 660円 |
| 1kg以内 | 750円 | 920円 |
| 2kg以内 | (対象外) | 1,350円 |
| 4kg以内 | (対象外) | 1,750円 |

### その他の定番

| 種類 | 料金 | 条件 |
| --- | --- | --- |
| 通常はがき | 85円 | 全国一律(2026-09-11に公式ページで確認) |
| ミニレター(郵便書簡) | 85円 | 厚さ1cm・25gまで |
| レターパックライト | 430円 | 厚さ3cm・4kgまで |
| レターパックプラス | 600円 | 4kgまで(厚さ制限なし) |
| スマートレター | 210円 | 25×17cm・厚さ2cm・1kgまで |

## 基本の流れ

1. ユーザーが送りたいものの種類(手紙/はがき/荷物に近いもの)を聞くか推定する。
2. サイズと重量から区分(定形/定形外の規格内・規格外)を決める。重量もサイズも条件を満たす必要がある(例: 30gでも厚さ1cm超なら定形外)。
3. 表から料金を返す。判断に使った区分・重量帯を一緒に伝える。

## エラー・失敗時の対応

- このスキルはネットワークを使わない。
- **区分が判定できない(サイズ不明など)**: 推測で料金を出さず、足りない条件(重量・厚さ)を聞き返す。条件が違えば料金は倍近く変わる。
- **表にないもの(ゆうパック、ゆうメール、国際郵便、速達・書留・本人限定などのオプション)**: 対象外と明示し、公式の料金ページ(https://www.post.japanpost.jp/send/domestic/charge/list/one_two.html)を案内する。

## 注意

- 料金は改定される。直近では2024-10-01に手紙・はがきが改定(定形郵便は50g以内110円の一律に統一)、2025-11-01にゆうメール運賃が改定されている。さらに2026-10-01にはゆうパック・ゆうパケット・クリックポストの運賃改定が予定されている(日本郵便のお知らせ: https://www.post.japanpost.jp/newsrelease/pressrelease/26283434137.html )。表の料金を答えるときは「2026-09-11時点の料金」と基準日を必ず添える。改定の可能性がある話題(来年の予定など)では、公式ページの確認を促す。
- 切手の組み合わせ(何円切手を何枚)を聞かれたら、不足のない組み合わせを計算してよい。料金そのものを勝手に安く見せる組み方(過不足のある貼り方)は提案しない。

## English summary

Looks up Japan Post's basic domestic postage (letters, postcards, mini-letters, Letter Pack, Smart Letter) from weight and size using a built-in fee table. No network access needed. Fees are the 2024-10-01 revision (standard letters are a flat 110 yen up to 50g), re-verified against Japan Post's official pages on 2026-09-11; always state that basis date when answering. Out of scope: Yu-Pack, Yu-Mail, international mail, and options like express or registered mail - point users to the official fee page for those. If weight or size is unknown, ask instead of guessing - the fee can nearly double across categories.
