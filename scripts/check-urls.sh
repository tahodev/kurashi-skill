#!/usr/bin/env bash
# Compatibility entry point: one response contract, no separate lenient checker.
set -euo pipefail
exec python3 "$(dirname "$0")/check-urls.py" "$@"
