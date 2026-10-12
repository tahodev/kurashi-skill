#!/usr/bin/env python3
"""Generate the skill cards from the canonical README Japanese table."""
from pathlib import Path
import html, re
ROOT = Path(__file__).resolve().parents[1]
readme = (ROOT / 'README.md').read_text().split('## English')[0]
rows = re.findall(r'^\| ([^|]+) \| `([a-z0-9-]+)` \| ([^|]+) \| ([^|]+) \|', readme, re.M)
cards = []
for i, (title, name, description, login) in enumerate(rows):
    cards.append(f'<article class="skill{ " red" if i % 2 else ""}" data-skill="{name}"><div class="top"><div class="stamp">暮</div><div><h3>{name}</h3></div></div><p>{html.escape(description.strip())}</p><div class="meta"><span class="tag">{html.escape(login.strip())}</span><a href="https://github.com/tahodev/kurashi-skill/blob/main/{name}/SKILL.md">正本</a></div></article>')
assert len(rows) == len(list(ROOT.glob('*/SKILL.md'))), 'README skill table drift'
p = ROOT / 'site/index.html'
t = p.read_text()
t = re.sub(r'<!-- GENERATED_SKILLS_START -->.*?<!-- GENERATED_SKILLS_END -->', '<!-- GENERATED_SKILLS_START -->\n' + '\n'.join(cards) + '\n<!-- GENERATED_SKILLS_END -->', t, flags=re.S)
p.write_text(t)
print(f'Generated {len(cards)} cards')
