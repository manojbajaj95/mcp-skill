#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_SKILLS="$SCRIPT_DIR/.agents/skills"
OUTPUT_DIR="$SCRIPT_DIR/skills"

run() {
  local name="$1"; shift
  echo ">>> Generating: $name"
  uv run mcp-skill create "$@" --non-interactive --force
  echo "<<< Done: $name"
  echo ""
}

# No auth
run context7      --url https://mcp.context7.com/mcp       --auth none  --name context7       --app-name Context7
run pubmed        --url https://pubmed.mcp.claude.com/mcp  --auth none  --name pubmed         --app-name Pubmed

# OAuth
run airtable      --url https://mcp.airtable.com/mcp        --auth oauth --name airtable       --app-name Airtable
run canva         --url https://mcp.canva.com/mcp            --auth oauth --name canva          --app-name Canva
run clickup       --url https://mcp.clickup.com/mcp          --auth oauth --name clickup        --app-name Clickup
run linear        --url https://mcp.linear.app/mcp           --auth oauth --name linear         --app-name Linear
run notion        --url https://mcp.notion.com/mcp           --auth oauth --name notion         --app-name Notion
run parallel_search --url https://search-mcp.parallel.ai/mcp --auth oauth --name parallel_search --app-name Parallelsearch
run sentry        --url https://mcp.sentry.dev/mcp           --auth oauth --name sentry         --app-name Sentry

# Move generated skills to skills/ folder
echo ">>> Moving skills from $AGENTS_SKILLS to $OUTPUT_DIR"
for skill_dir in "$AGENTS_SKILLS"/*/; do
  skill_name="$(basename "$skill_dir")"
  dest="$OUTPUT_DIR/$skill_name"
  rm -rf "$dest"
  mv "$skill_dir" "$dest"
  echo "    Moved: $skill_name"
done

echo ""
echo "Done. Skills available in: $OUTPUT_DIR"
