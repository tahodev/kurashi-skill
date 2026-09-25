#!/usr/bin/env python3
"""SKILL.md の「実測日」が古くなっていないか検査する。

実測日から STALE_AFTER_DAYS(既定90日)を過ぎたスキルは失敗扱い。
スケジュール実行時は health-check.yml の issue 自動起票で再実測のリマインドになる。
実測日ヘッダがないスキル(静的データスキル等)は data_as_of ポリシー側の対象なので警告のみ。
"""
from datetime import date
from pathlib import Path
import re, sys

STALE_AFTER_DAYS = 90
HEADER_RE = re.compile(r'実測日[:：]\s*(\d{4}-\d{2}-\d{2})')

root = Path(__file__).resolve().parents[1]
today = date.today()
stale, missing = [], []
for path in sorted(root.glob('*/SKILL.md')):
    m = HEADER_RE.search(path.read_text(encoding='utf-8'))
    if not m:
        missing.append(path.parent.name)
        continue
    d = date.fromisoformat(m.group(1))
    age = (today - d).days
    status = 'OK  ' if age <= STALE_AFTER_DAYS else 'STALE'
    print(f'{status} {path.parent.name}: 実測日 {d} ({age}日前)')
    if age > STALE_AFTER_DAYS:
        stale.append((path.parent.name, d, age))

if missing:
    print('INFO  実測日ヘッダなし(data_as_ofポリシー側で管理): ' + ', '.join(missing))
if stale:
    print(f'{len(stale)}件のスキルが実測から{STALE_AFTER_DAYS}日超過。再実測してSKILL.mdの実測日を更新してください: '
          + ', '.join(f'{n}({d})' for n, d, _ in stale))
    sys.exit(1)
print(f'全スキルの実測日が{STALE_AFTER_DAYS}日以内')
