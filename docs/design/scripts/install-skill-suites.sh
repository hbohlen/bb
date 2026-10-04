#!/usr/bin/env bash
# Install the mattpocock skill suite into a bb dev instance.
#
# `bb skill install` writes into the instance's own data dir, so pointing
# BB_DATA_DIR at the fork's dev instance keeps these installs out of the
# production ~/.bb data dir. Skills already present are skipped rather than
# reinstalled, so the script is safe to rerun.
#
# Usage:
#   BB_INSTANCE=bb-vendor-bb-f6b7ebc4daeb ./install-skill-suites.sh
#
# BB_INSTANCE is the dev instance directory name under ~/.bb-dev. The server
# port and this name both derive from a hash of the repo root, so they change if
# the checkout moves or is renamed. Read the current values from the dev server
# log, which prints "Instance" and "Server listening" on startup.
#
# NOTE: BB_SERVER_URL is deliberately NOT inherited from the environment. The
# fork's API runs on a different port from the app, and picking up a stale
# BB_SERVER_URL from an interactive shell silently installs into production.

set -uo pipefail

INSTANCE="${BB_INSTANCE:-bb-vendor-bb-f6b7ebc4daeb}"
DATA_DIR="$HOME/.bb-dev/$INSTANCE"
SERVER_PORT="${BB_SERVER_PORT:-19580}"

export BB_SERVER_URL="http://127.0.0.1:$SERVER_PORT"
export BB_DATA_DIR="$DATA_DIR"
export BB_SERVER_MANAGED=0

if [[ ! -f "$DATA_DIR/bb.db" ]]; then
  echo "No bb.db in $DATA_DIR. Is the dev server running?" >&2
  exit 1
fi

PROJECT_ID="$(bb project list --json 2>/dev/null | python3 -c '
import json, sys
d = json.load(sys.stdin)
items = d if isinstance(d, list) else d.get("projects", [])
print(items[0]["id"] if items else "")
')"

if [[ -z "$PROJECT_ID" ]]; then
  echo "Could not resolve a project on $BB_SERVER_URL. Set BB_PROJECT_ID." >&2
  exit 1
fi
export BB_PROJECT_ID="$PROJECT_ID"

echo "Instance : $BB_SERVER_URL"
echo "Data dir : $BB_DATA_DIR"
echo "Project  : $BB_PROJECT_ID"
echo

# Built from `bb skill search mattpocock --json`, then pruned against the real
# repository inventory. The registry index lists 53 results but is stale: it
# still advertises `review`, `batch-grill-me` and `resolving-merge-conflicts`,
# which the repository no longer ships. When an install fails, bb prints the
# authoritative list — currently 37 skills — so that output is the source of
# truth, not the search index.
#
# bb skill install can exit nonzero on success, so each install is confirmed by
# reading the file back off disk.
SUITES=(
  mattpocock/skills/ask-matt
  mattpocock/skills/code-review
  mattpocock/skills/codebase-design
  mattpocock/skills/diagnosing-bugs
  mattpocock/skills/domain-modeling
  mattpocock/skills/git-guardrails-claude-code
  mattpocock/skills/grill-me
  mattpocock/skills/grill-with-docs
  mattpocock/skills/grilling
  mattpocock/skills/handoff
  mattpocock/skills/implement
  mattpocock/skills/implement-spec
  mattpocock/skills/improve-codebase-architecture
  mattpocock/skills/loop-me
  mattpocock/skills/pr
  mattpocock/skills/prototype
  mattpocock/skills/research
  mattpocock/skills/retro
  mattpocock/skills/setup-matt-pocock-skills
  mattpocock/skills/setup-pre-commit
  mattpocock/skills/tdd
  mattpocock/skills/teach
  mattpocock/skills/to-spec
  mattpocock/skills/to-tickets
  mattpocock/skills/triage
  mattpocock/skills/wayfinder
  mattpocock/skills/wizard
  # The remaining 10 from the repository inventory bb printed on a failed
  # install. These do not surface in `bb skill search mattpocock`, so building
  # the list from search alone silently misses them.
  mattpocock/skills/claude-handoff
  mattpocock/skills/migrate-to-shoehorn
  mattpocock/skills/scaffold-exercises
  mattpocock/skills/setup-ts-deep-modules
  mattpocock/skills/to-questionnaire
  mattpocock/skills/wait-what
  mattpocock/skills/writing-beats
  mattpocock/skills/writing-for-agents
  mattpocock/skills/writing-fragments
  mattpocock/skills/writing-shape
)

for skill in "${SUITES[@]}"; do
  name="${skill##*/}"
  if [[ -f "$DATA_DIR/skills/$name/SKILL.md" ]]; then
    echo "  skip    $name"
    continue
  fi
  bb skill install "$skill" >/dev/null 2>&1
  if [[ -f "$DATA_DIR/skills/$name/SKILL.md" ]]; then
    echo "  ok      $name"
  else
    echo "  FAILED  $name  ($skill)"
  fi
done

echo
printf 'installed: %s skills in %s\n' "$(ls -1 "$DATA_DIR/skills" | wc -l | tr -d ' ')" "$DATA_DIR/skills"