#!/usr/bin/env python3
"""Parse YAML and validate local Markdown files plus GitHub-style heading anchors."""
from pathlib import Path
from urllib.parse import unquote
import re, sys
import yaml
ROOT = Path(__file__).resolve().parents[1]


def anchors(text):
    counts, result = {}, set()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        value = heading.lower().replace(' ', '-')
        value = ''.join(c for c in value if c.isalnum() or c in '-_')
        suffix = counts.get(value, 0)
        counts[value] = suffix + 1
        result.add(value + (f'-{suffix}' if suffix else ''))
    return result


def main():
    errors, yaml_count, links = [], 0, 0
    paths = [*ROOT.glob('*/SKILL.md'), *ROOT.glob('.github/**/*.yml'), *ROOT.glob('.github/**/*.yaml')]
    for path in paths:
        text = path.read_text()
        if path.suffix == '.md':
            match = re.match(r'\A---\n(.*?)\n---', text, re.S)
            if not match:
                errors.append(f'{path.relative_to(ROOT)}: missing frontmatter')
                continue
            text = match.group(1)
        try:
            value = yaml.safe_load(text)
            if not isinstance(value, dict):
                raise ValueError('expected mapping')
            yaml_count += 1
        except (yaml.YAMLError, ValueError) as exc:
            errors.append(f'{path.relative_to(ROOT)}: YAML {exc}')
    for path in [ROOT/'README.md', ROOT/'CONTRIBUTING.md', ROOT/'AGENTS.md', ROOT/'ROADMAP.md', ROOT/'CHANGELOG.md', ROOT/'SECURITY.md', *ROOT.glob('*/SKILL.md'), *ROOT.glob('docs/**/*.md'), *ROOT.glob('.github/**/*.md')]:
        text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)', text):
            if re.match(r'^[a-z][a-z0-9+.-]*:', target, re.I):
                continue
            relative, _, fragment = unquote(target).partition('#')
            dest = path.parent / relative if relative else path
            links += 1
            if not dest.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing local link {target}')
            elif fragment and dest.suffix == '.md' and fragment not in anchors(dest.read_text()):
                errors.append(f'{path.relative_to(ROOT)}: missing anchor {target}')
    for error in errors:
        print(f'FAIL {error}')
    print(f'Checked {yaml_count} YAML documents and {links} local links/anchors')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
