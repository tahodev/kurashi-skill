# japan-holidays ガイド

内閣府の公式CSVから祝日・連休を調べるスキル。APIキー・ログイン不要。

## データ

- URL: `https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`
- 文字コード: Shift_JIS (`curl -s ... | iconv -f SHIFT_JIS -t UTF-8` で変換)
- 形式: `日付,名称` (1行目はヘッダー)。振替休日・国民の休日も行として収録。
- 収録範囲: 1955年〜翌年分程度

## 使い方の例

「今年の連休を教えて」と聞かれたら:

1. CSVを取得してUTF-8に変換
2. 対象年の全日付について「土日 or CSV掲載日」を判定
3. 連続する休みの区間を3日以上で抽出
4. 区間の日付・日数・含まれる祝日名を一覧にする

## つまずきポイント

- **文字化け**: UTF-8変換を忘れると名称が化ける。
- **将来年がない**: CSV未収録の年は、祝日法のルール(振替休日・国民の休日)で計算する必要がある。ルールは `japan-holidays/SKILL.md` を参照。
- **元ページ**: 制度の確認は内閣府のページ https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html
