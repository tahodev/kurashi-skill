#!/usr/bin/env python3
from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
skills=sorted(p.parent.name for p in root.glob('*/SKILL.md'))
guides=sorted(p.stem for p in (root/'docs/features').glob('*.md'))
readme=(root/'README.md').read_text(encoding='utf-8')
listed=sorted(set(re.findall(r'docs/features/([a-z0-9-]+)\.md', readme)))
failed=False
for label, actual in [('docs/features', guides), ('README feature table', listed)]:
    missing=sorted(set(skills)-set(actual)); extra=sorted(set(actual)-set(skills))
    if missing or extra:
        print(f'FAIL  {label} drift: missing={missing} extra={extra}'); failed=True
    else:
        print(f'OK    {label}: {len(actual)} skills')
# Check explicit repository-wide totals in README and docs. Counts attached to an
# individual install command (for example "1スキル") are intentionally excluded.
patterns=[
    r'(?:現在は|現在|全)\s*(\d+)\s*スキル',
    r'(?:currently (?:contains|has)|all)\s*(\d+)\s*skills',
]
for path in [root/'README.md', *root.glob('docs/**/*.md')]:
    text=path.read_text(encoding='utf-8')
    for pat in patterns:
        for m in re.finditer(pat, text, re.I):
            if int(m.group(1)) != len(skills):
                print(f'FAIL  {path.relative_to(root)} current skill count says {m.group(1)}; filesystem has {len(skills)}'); failed=True
print(f'OK    canonical skill count: {len(skills)}')
sys.exit(1 if failed else 0)
