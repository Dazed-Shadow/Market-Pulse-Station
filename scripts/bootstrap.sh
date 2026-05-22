#!/usr/bin/env bash
# Bootstrap the Market Pulse Station repo.
# Inits git, makes the first commit locally, and PRINTS the GitHub steps.
# It will NOT create a GitHub repo or push for you — that's yours to run.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -d .git ]; then
  echo "✓ git already initialized"
else
  git init -q
  echo "✓ git initialized"
fi

# Safety check: secrets.py must never be staged.
if git ls-files --error-unmatch firmware/secrets.py >/dev/null 2>&1; then
  echo "✗ firmware/secrets.py is tracked — aborting. Remove it from git first."
  exit 1
fi

git add .
if git diff --cached --quiet; then
  echo "✓ nothing new to commit"
else
  git commit -q -m "Initial scaffold: roadmap, CLAUDE.md, Notion setup, firmware skeleton"
  echo "✓ first commit created"
fi

cat <<'NEXT'

────────────────────────────────────────────────────────
Next steps (run these yourself — they touch your account):

  1. Create an EMPTY repo on GitHub named: market-pulse-station
     (no README/license — this repo already has them)

  2. Wire the remote and push:
       git remote add origin git@github.com:<your-username>/market-pulse-station.git
       git branch -M main
       git push -u origin main

  3. In CLAUDE.md, fill the two placeholders:
       - Notion landing-page URL
       - confirmed display driver chip (ILI9341 or ST7796)
────────────────────────────────────────────────────────
NEXT
