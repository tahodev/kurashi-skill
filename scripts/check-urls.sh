#!/usr/bin/env bash
# Extract http(s) URLs from each skill's SKILL.md, README.md and docs/**/*.md,
# and verify they respond.
# Skipped:
#   - Templated URLs (containing { } or ${...}): they need real parameters
#     such as an API key and cannot be checked anonymously.
#   - URLs in EXCLUDE_URLS below: dated one-off examples that expire by design
#     (e.g. a single JMA earthquake JSON). Keep them in the docs as concrete
#     historical examples, but never fail CI on them. When you add one, mark
#     it clearly as a historical example in the doc too.
set -u
fail=0

EXCLUDE_URLS=(
  # JMA individual earthquake JSONs are removed after a few days; kept in
  # bosai-alert/SKILL.md as a worked example of the `json` field.
  'https://www.jma.go.jp/bosai/quake/data/20260908234330_20260908234052_VXSE5k_1.json'
  # Typhoon list.json returns 404 when no typhoon is active - that is the
  # normal quiet-time state, documented in bosai-typhoon/SKILL.md.
  'https://www.jma.go.jp/bosai/typhoon/data/list.json'
)

mapfile -t urls < <(grep -hoE 'https?://[^ )"`<]+' -- */SKILL.md README.md docs/*.md docs/features/*.md \
  | sed 's/[.,;]*$//' | sort -u)
for url in "${urls[@]}"; do
  case "$url" in
    *'{'*|*'}'*) echo "SKIP  $url (templated)"; continue ;;
  esac
  skip=0
  for ex in "${EXCLUDE_URLS[@]}"; do
    if [ "$url" = "$ex" ]; then
      echo "SKIP  $url (dated example, EXCLUDE_URLS)"; skip=1; break
    fi
  done
  [ "$skip" -eq 1 ] && continue
  code=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 \
    -A 'kurashi-skill-url-check' "$url")
  case "$code" in
    2*|3*) echo "OK    $code $url" ;;
    *)     echo "FAIL  $code $url"; fail=1 ;;
  esac
done

# Informational (never fails CI): the KEN_ALL zip behind the templated URL in
# zipcode-lookup/SKILL.md is skipped above, and Japan Post serves 404 for it
# from datacenter IPs (documented 2026-09-11/12). Surface the current state so
# a real outage is distinguishable from the known IP restriction.
page=$(curl -s -L --max-time 20 -A 'kurashi-skill-url-check' \
  'https://www.post.japanpost.jp/zipcode/dl/utf-zip.html' || true)
href=$(grep -oE 'utf/zip/utf_ken_all\.zip' <<<"$page" | head -1)
if [ -z "$href" ]; then
  echo "INFO  KEN_ALL zip link not found on download page (page structure changed?)"
else
  zcode=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 \
    -A 'kurashi-skill-url-check' "https://www.post.japanpost.jp/zipcode/dl/${href}")
  echo "INFO  KEN_ALL zip (${href}): HTTP ${zcode} (404 from datacenter IPs is the known restriction)"
fi
exit "$fail"
