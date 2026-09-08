#!/usr/bin/env bash
# Extract http(s) URLs from each skill's SKILL.md and verify they respond.
# Templated URLs (containing { } or ${...}) are skipped: they need real
# parameters such as an API key and cannot be checked anonymously.
set -u
fail=0
mapfile -t urls < <(grep -hoE 'https?://[^ )"`<]+' -- */SKILL.md \
  | sed 's/[.,;]*$//' | sort -u)
for url in "${urls[@]}"; do
  case "$url" in
    *'{'*|*'}'*) echo "SKIP  $url (templated)"; continue ;;
  esac
  code=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 \
    -A 'kurashi-skill-url-check' "$url")
  case "$code" in
    2*|3*) echo "OK    $code $url" ;;
    *)     echo "FAIL  $code $url"; fail=1 ;;
  esac
done
exit "$fail"
