#!/usr/bin/env bash
# Install the Founder pack into a DeepSeek Harness profile.
#
#   ./install.sh                 # install into the default profile (~/.dsh)
#   ./install.sh --profile work  # install into ~/.dsh/profiles/work
#   ./install.sh --uninstall     # remove it again
#
# The pack installs as plain skill directories. DSH's skill-filesystem provider
# discovers <name>/SKILL.md under $DSH_HOME/skills, so no plugin, build step or
# network access is required.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HERE/skills"
PROFILE=""
UNINSTALL=0

while [ $# -gt 0 ]; do
  case "$1" in
    --profile) PROFILE="${2:?--profile needs a name}"; shift 2 ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

if [ -n "$PROFILE" ]; then
  ROOT="${DSH_HOME:-$HOME/.dsh}/profiles/$PROFILE"
else
  ROOT="${DSH_HOME:-$HOME/.dsh}"
fi
TARGET="$ROOT/skills"

if [ ! -d "$SKILLS_DIR" ]; then
  echo "error: $SKILLS_DIR not found; run install.sh from the package root" >&2
  exit 1
fi

names=()
for d in "$SKILLS_DIR"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  names+=("$(basename "$d")")
done

if [ "${#names[@]}" -eq 0 ]; then
  echo "error: no skill folders with a SKILL.md found in $SKILLS_DIR" >&2
  exit 1
fi

if [ "$UNINSTALL" -eq 1 ]; then
  for n in "${names[@]}"; do
    if [ -e "$TARGET/$n" ]; then
      rm -rf "$TARGET/$n"
      echo "removed $TARGET/$n"
    fi
  done
  echo "uninstalled $((${#names[@]})) skills from $TARGET"
  exit 0
fi

mkdir -p "$TARGET"
installed=0
skipped=0
for n in "${names[@]}"; do
  if [ -e "$TARGET/$n" ]; then
    echo "kept existing $TARGET/$n (not overwritten)"
    skipped=$((skipped + 1))
    continue
  fi
  cp -R "$SKILLS_DIR/$n" "$TARGET/$n"
  find "$TARGET/$n" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
  find "$TARGET/$n" -name '*.pyc' -delete 2>/dev/null || true
  echo "installed $TARGET/$n"
  installed=$((installed + 1))
done

echo
echo "installed $installed skill(s) into $TARGET${skipped:+, $skipped already present}"
echo
echo "Next: start DSH and ask it to test a business idea, for example"
echo "  \"test this idea: a mobile dog-wash service in Lisbon\""
echo "The founder skill chains the whole pack. Ask for 20 buyers (Quick) or 100 (Full)."
