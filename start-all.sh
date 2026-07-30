#!/usr/bin/env bash
# Thin wrapper — real starter is cross-platform Node script.
set -euo pipefail
cd "$(dirname "$0")"
exec node scripts/start-all.mjs "$@"
