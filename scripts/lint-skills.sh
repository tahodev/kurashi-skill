#!/usr/bin/env bash
# Frontmatter lint for every */SKILL.md:
#   - frontmatter block present
#   - name, description, license keys present
#   - name matches the directory name
set -u
fail=0
for f in */SKILL.md; do
  dir=$(dirname "$f")
  fm=$(awk 'NR==1 && /^---$/ {inside=1; next} inside && /^---$/ {exit} inside {print}' "$f")
  if [ -z "$fm" ]; then echo "FAIL  $f: no frontmatter"; fail=1; continue; fi
  ok=1
  for key in name description license; do
    if ! grep -q "^${key}:" <<<"$fm"; then
      echo "FAIL  $f: missing '$key'"; fail=1; ok=0
    fi
  done
  name=$(grep '^name:' <<<"$fm" | head -1 | sed 's/^name:[[:space:]]*//')
  if [ -n "$name" ] && [ "$name" != "$dir" ]; then
    echo "FAIL  $f: name '$name' != directory '$dir'"; fail=1; ok=0
  fi
  [ "$ok" -eq 1 ] && echo "OK    $f"
done
exit "$fail"
