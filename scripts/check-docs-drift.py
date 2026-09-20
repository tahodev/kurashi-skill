#!/usr/bin/env python3
"""Fail when the canonical skill directories and their documentation drift apart."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
skills = sorted(p.parent.name for p in root.glob("*/SKILL.md"))
skill_set = set(skills)
failed = False


def compare(label: str, documented: list[str]) -> None:
    global failed
    actual = set(documented)
    missing = sorted(skill_set - actual)
    extra = sorted(actual - skill_set)
    duplicates = sorted(name for name in actual if documented.count(name) > 1)
    if missing or extra or duplicates:
        print(
            f"FAIL  {label} drift: missing={missing} extra={extra} "
            f"duplicates={duplicates}"
        )
        failed = True
    else:
        print(f"OK    {label}: {len(documented)} skills")


guides = sorted(p.stem for p in (root / "docs/features").glob("*.md"))
compare("docs/features", guides)

readme = (root / "README.md").read_text(encoding="utf-8")
# Check the Japanese and English feature tables independently. A combined set can
# hide a missing row in one language when the other language still has it.
english_marker = "## English"
japanese_readme, english_readme = readme.split(english_marker, 1)
feature_link = r"docs/features/([a-z0-9-]+)\.md"
compare("README Japanese feature table", re.findall(feature_link, japanese_readme))
compare("README English feature table", re.findall(feature_link, english_readme))

install = (root / "docs/install.md").read_text(encoding="utf-8")
install_tree = re.findall(r"^  ([a-z0-9-]+)/SKILL\.md\b", install, re.MULTILINE)
compare("docs/install.md repository tree", install_tree)

# Every live skill must be recorded in the changelog. This deliberately checks
# presence rather than parsing release headings so Unreleased entries also count.
changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
changelog_names = [name for name in skills if re.search(rf"`?{re.escape(name)}`?", changelog)]
missing_changelog = sorted(skill_set - set(changelog_names))
if missing_changelog:
    print(f"FAIL  CHANGELOG.md missing skills: {missing_changelog}")
    failed = True
else:
    print(f"OK    CHANGELOG.md mentions all {len(skills)} skills")

# Check explicit repository-wide totals in README and docs. Counts attached to an
# individual install command (for example "1スキル") are intentionally excluded.
patterns = [
    r"(?:現在の収録数:|現在は|現在|全)\s*\*{0,2}(\d+)\s*スキル",
    r"(?:current collection:|currently (?:contains|has)|all)\s*\*{0,2}(\d+)\s*skills",
]
for path in [root / "README.md", *root.glob("docs/**/*.md")]:
    text = path.read_text(encoding="utf-8")
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            if int(match.group(1)) != len(skills):
                print(
                    f"FAIL  {path.relative_to(root)} current skill count says "
                    f"{match.group(1)}; filesystem has {len(skills)}"
                )
                failed = True

print(f"OK    canonical skill count: {len(skills)}")
sys.exit(1 if failed else 0)
