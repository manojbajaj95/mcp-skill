#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_SKILLS="$SCRIPT_DIR/.agents/skills"
OUTPUT_DIR="$SCRIPT_DIR/skills"

run() {
  local name="$1"
  local url="$2"
  local auth="$3"
  local app_name="$4"

  echo ">>> Generating: $name"
  uv run mcp-skill create \
    --url "$url" \
    --auth "$auth" \
    --name "$name" \
    --app-name "$app_name" \
    --non-interactive \
    --force
  echo "<<< Done: $name"
  echo ""
}

copy_generated_skill() {
  local name="$1"
  local src="$AGENTS_SKILLS/$name"
  local dest="$OUTPUT_DIR/$name"

  if [[ ! -d "$src" ]]; then
    echo "Error: expected generated skill directory '$src' was not created." >&2
    exit 1
  fi

  rm -rf "$dest"
  cp -R "$src" "$dest"
  echo "    Copied: $name"
}

skills=(
  "airtable|https://mcp.airtable.com/mcp|oauth|Airtable"
  "canva|https://mcp.canva.com/mcp|oauth|Canva"
  "clickup|https://mcp.clickup.com/mcp|oauth|Clickup"
  "context7|https://mcp.context7.com/mcp|none|Context7"
  "linear|https://mcp.linear.app/mcp|oauth|Linear"
  "notion|https://mcp.notion.com/mcp|oauth|Notion"
  "parallel_search|https://search-mcp.parallel.ai/mcp|oauth|Parallelsearch"
  "pubmed|https://pubmed.mcp.claude.com/mcp|none|Pubmed"
  "sentry|https://mcp.sentry.dev/mcp|oauth|Sentry"
)

for skill in "${skills[@]}"; do
  IFS="|" read -r name url auth app_name <<< "$skill"
  run "$name" "$url" "$auth" "$app_name"
done

echo ">>> Copying regenerated app skills to $OUTPUT_DIR"
for skill in "${skills[@]}"; do
  IFS="|" read -r name _ <<< "$skill"
  copy_generated_skill "$name"
done

echo ""
echo "Done. Regenerated app skills are available in: $OUTPUT_DIR"
