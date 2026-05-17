#!/usr/bin/env bash
set -euo pipefail
if find . -name '*.rej' | grep -q .; then
  echo 'Found .rej files'; exit 1
fi
if rg -n '^(<<<<<<<|=======|>>>>>>>)' . --glob '!scripts/check-copier-conflicts.sh'; then
  echo 'Found conflict markers'; exit 1
fi
echo 'No copier conflict artifacts found.'
