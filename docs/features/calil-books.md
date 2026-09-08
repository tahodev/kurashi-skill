# calil-books ガイド

カーリル図書館APIで図書館の蔵書と貸出状況を検索するスキル。無料のAPIキーが必要。

## 準備

https://calil.jp/api/dashboard/ でアカウントを作ってAPIキーを発行する(無料)。キーは環境変数に入れ、チャットやコミットに書かない。

## エンドポイント一覧

| 用途 | URL |
| --- | --- |
| 図書館検索 | `https://api.calil.jp/library?appkey={キー}&pref={都道府県}&format=json` |
| 蔵書照会 | `https://api.calil.jp/check?appkey={キー}&isbn={ISBN}&systemid={ID}&format=json` |
| ポーリング | `https://api.calil.jp/check?appkey={キー}&session={セッション}&format=json` |

## 使い方の例

「この本、近くの図書館で借りられる?」と聞かれたら:

1. `library` で対象地域の図書館を検索し、`systemid` を得る
2. `check` にISBNと `systemid` を渡す
3. `continue: 1` なら `session` で2秒以上あけて再取得(`continue: 0` まで)
4. `libkey` ごとの状態(貸出可 / 貸出中 / 蔵書なし ...)を答える。`reserveurl` があれば一緒に伝える

## つまずきポイント

- **ポーリング必須**: 初回で結果が揃わないのが普通。`session` 再取得では `isbn`・`systemid` を付けない。
- **再取得の間隔**: 2秒未満で連打しない。
- **利用規約**: https://calil.jp/doc/api.html 。データの長期キャッシュは規約上できない。
