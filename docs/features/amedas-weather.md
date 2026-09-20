# amedas-weather ガイド

気象庁のアメダス最新観測値を調べるスキル。正本は [amedas-weather/SKILL.md](../../amedas-weather/SKILL.md)。

- `latest_time.txt` で最新観測時刻(JST、10分間隔)を取得
- `/bosai/amedas/data/map/<YYYYMMDDHHMMSS>.json` で全国約1,300観測所の気温・湿度・風・降水量などを一括取得
- `/bosai/amedas/const/amedastable.json` で観測所名・位置を解決(`amedastation.json` というファイル名は存在しない)
- 要素は観測所のタイプで異なる(気圧は type A など一部のみ)
- 予報は jma-weather、雨雲の短時間予測は amagumo と使い分ける
