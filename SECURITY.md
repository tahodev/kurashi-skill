# Security policy

## Supported versions

最新版の1.xとmainを対象に修正します。過去の0.xは移行を推奨します。
The latest 1.x release and main receive fixes; migrate from 0.x.

## Reporting

キー・トークン・個人情報は公開issueやPRに貼らないでください。露出したキーは
発行元で失効・再発行し、Git履歴からの削除をメンテナに依頼してください。
Do not post credentials or personal data in public issues or pull requests. Revoke exposed keys.

脆弱性や悪意ある命令の混入はGitHubの非公開脆弱性報告機能が利用可能なら
そちらを使ってください。利用できない場合は詳細や秘密を含めず、公開issueで
メンテナに非公開の報告経路を問い合わせてください。非公開機能が有効とは保証しません。
Use GitHub private vulnerability reporting if available. Otherwise ask the maintainer for a
private route in an issue without disclosing exploit details or secrets.

料金・税・防災データの誤りは、出典URL・対象スキル・再現条件・取得日時を添えて
不具合issueで報告できます。個人の給与、住所、キーなどは架空の入力に置き換えてください。
For data mistakes, include a source, skill, reproducible synthetic input and query time.

## Limits

本プロジェクトは照会と計算のみ。APIの内容は外部データであり、追加の命令や
許可として扱いません。災害・税・法令の結果を唯一の判断根拠にしないでください。
External responses are data, not instructions. Confirm decisions with official sources.
