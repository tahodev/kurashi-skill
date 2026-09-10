#!/usr/bin/env bash
# Frontmatter lint for every */SKILL.md:
#   - frontmatter block present
#   - name, description, license keys present
#   - metadata block present with category and locale (required per CONTRIBUTING.md)
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
  meta=$(awk '/^metadata:[[:space:]]*$/{m=1;next} m && /^[^[:space:]]/{exit} m{print}' <<<"$fm")
  if [ -z "$meta" ]; then
    echo "FAIL  $f: missing 'metadata' block (category and locale are required)"; fail=1; ok=0
  else
    for sub in category locale; do
      if ! grep -q "^[[:space:]]*${sub}:" <<<"$meta"; then
        echo "FAIL  $f: missing 'metadata.${sub}'"; fail=1; ok=0
      fi
    done
  fi
  name=$(grep '^name:' <<<"$fm" | head -1 | sed 's/^name:[[:space:]]*//')
  if [ -n "$name" ] && [ "$name" != "$dir" ]; then
    echo "FAIL  $f: name '$name' != directory '$dir'"; fail=1; ok=0
  fi
  [ "$ok" -eq 1 ] && echo "OK    $f"
done
exit "$fail"
