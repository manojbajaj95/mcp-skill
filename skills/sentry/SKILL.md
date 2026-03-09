---
name: sentry
description: "MCP skill for sentry. Provides 13 tools: whoami, find_organizations, find_teams, find_projects, find_releases, get_issue_details, get_issue_tag_values, get_trace_details, get_event_attachment, search_events, analyze_issue_with_seer, search_issues, search_issue_events"
---

# sentry

MCP skill for sentry. Provides 13 tools: whoami, find_organizations, find_teams, find_projects, find_releases, get_issue_details, get_issue_tag_values, get_trace_details, get_event_attachment, search_events, analyze_issue_with_seer, search_issues, search_issue_events

## Authentication

This MCP server uses **OAuth** authentication.
The OAuth flow is handled automatically by the MCP client. Tokens are persisted
to `~/.mcp-skill/sentry/oauth-tokens/` so subsequent runs reuse the
same credentials without re-authenticating.

```python
app = SentryApp()  # uses default OAuth flow
```

To bring your own OAuth provider, pass it via the `auth` argument:

```python
app = SentryApp(auth=my_oauth_provider)
```

## Dependencies

This skill requires the following Python packages:

- `mcp-skill`

Install with uv:

```bash
uv pip install mcp-skill
```

Or with pip:

```bash
pip install mcp-skill
```

## How to Run

**Important:** Add `.agents/skills` to your Python path so imports resolve correctly:

```python
import sys
sys.path.insert(0, ".agents/skills")
from sentry.app import SentryApp
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from sentry.app import SentryApp

async def main():
    app = SentryApp()
    result = await app.whoami()
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from sentry.app import SentryApp

async def main():
    app = SentryApp()
    result = await app.whoami()
    print(result)

asyncio.run(main())
"
```

## Available Tools

### whoami

Identify the authenticated user in Sentry.

Use this tool when you need to:
- Get the user's name and email address.

**Example:**
```python
result = await app.whoami()
```

### find_organizations

Find organizations that the user has access to in Sentry.

Use this tool when you need to:
- View organizations in Sentry
- Find an organization's slug to aid other tool requests
- Search for specific organizations by name or slug

Returns up to 25 results. If you hit this limit, use the query parameter to narrow down results.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | `str | None` | No | Search query to filter results by name or slug. Use this to narrow down results when there are many items. |

**Example:**
```python
result = await app.find_organizations(query="example")
```

### find_teams

Find teams in an organization in Sentry.

Use this tool when you need to:
- View teams in a Sentry organization
- Find a team's slug and numeric ID to aid other tool requests
- Search for specific teams by name or slug

Returns up to 25 results. If you hit this limit, use the query parameter to narrow down results.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organizationSlug | `str` | Yes | The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool. |
| regionUrl | `str | None` | No | The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool. |
| query | `str | None` | No | Search query to filter results by name or slug. Use this to narrow down results when there are many items. |

**Example:**
```python
result = await app.find_teams(organizationSlug="example", regionUrl="example", query="example")
```

### find_projects

Find projects in Sentry.

Use this tool when you need to:
- View projects in a Sentry organization
- Find a project's slug to aid other tool requests
- Search for specific projects by name or slug

Returns up to 25 results. If you hit this limit, use the query parameter to narrow down results.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organizationSlug | `str` | Yes | The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool. |
| regionUrl | `str | None` | No | The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool. |
| query | `str | None` | No | Search query to filter results by name or slug. Use this to narrow down results when there are many items. |

**Example:**
```python
result = await app.find_projects(organizationSlug="example", regionUrl="example", query="example")
```

### find_releases

Find releases in Sentry.

Use this tool when you need to:
- Find recent releases in a Sentry organization
- Find the most recent version released of a specific project
- Determine when a release was deployed to an environment

<examples>
### Find the most recent releases in the 'my-organization' organization

```
find_releases(organizationSlug='my-organization')
```

### Find releases matching '2ce6a27' in the 'my-organization' organization

```
find_releases(organizationSlug='my-organization', query='2ce6a27')
```
</examples>

<hints>
- If the user passes a parameter in the form of name/otherName, its likely in the format of <organizationSlug>/<projectSlug>.
</hints>

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organizationSlug | `str` | Yes | The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool. |
| regionUrl | `str | None` | No | The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool. |
| projectSlug | `str | None` | No | The project's slug. This will default to all projects you have access to. It is encouraged to specify this when possible. |
| query | `str | None` | No | Search for versions which contain the provided string. |

**Example:**
```python
result = await app.find_releases(organizationSlug="example", regionUrl="example", projectSlug="example")
```

### get_issue_details

Get detailed information about a specific Sentry issue by ID.

USE THIS TOOL WHEN USERS:
- Provide a specific issue ID (e.g., 'CLOUDFLARE-MCP-41', 'PROJECT-123')
- Ask to 'explain [ISSUE-ID]', 'tell me about [ISSUE-ID]'
- Want details/stacktrace/analysis for a known issue
- Provide a Sentry issue URL

DO NOT USE for:
- General searching or listing issues (use search_issues)

TRIGGER PATTERNS:
- 'Explain ISSUE-123' → use get_issue_details
- 'Tell me about PROJECT-456' → use get_issue_details
- 'What happened in [issue URL]' → use get_issue_details

<examples>
### With Sentry URL (recommended - simplest approach)
```
get_issue_details(issueUrl='https://sentry.sentry.io/issues/6916805731/?project=4509062593708032&query=is%3Aunresolved')
```

### With issue ID and organization
```
get_issue_details(organizationSlug='my-organization', issueId='CLOUDFLARE-MCP-41')
```

### With event ID and organization
```
get_issue_details(organizationSlug='my-organization', eventId='c49541c747cb4d8aa3efb70ca5aba243')
```
</examples>

<hints>
- **IMPORTANT**: If user provides a Sentry URL, pass the ENTIRE URL to issueUrl parameter unchanged
- When using issueUrl, all other parameters are automatically extracted - don't provide them separately
- If using issueId (not URL), then organizationSlug is required
</hints>

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organizationSlug | `str` | No | The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool. |
| regionUrl | `str | None` | No | The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool. |
| issueId | `str` | No | The Issue ID. e.g. `PROJECT-1Z43` |
| eventId | `str` | No | The ID of the event. |
| issueUrl | `str` | No | The URL of the issue. e.g. https://my-organization.sentry.io/issues/PROJECT-1Z43 |

**Example:**
```python
result = await app.get_issue_details(organizationSlug="example", regionUrl="example", issueId="example")
```

### get_issue_tag_values

Get tag value distribution for a specific Sentry issue.

Use this tool when you need to:
- Understand how an issue is distributed across different tag values
- Get aggregate counts of unique tag values (e.g., 'how many unique URLs are affected')
- Analyze which browsers, environments, or URLs are most impacted by an issue
- View the tag distributions page data programmatically

Common tag keys:
- `url`: Request URLs affected by the issue
- `browser`: Browser types and versions
- `browser.name`: Browser names only
- `os`: Operating systems
- `environment`: Deployment environments (production, staging, etc.)
- `release`: Software releases
- `device`: Device types
- `user`: Affected users

<examples>
### Get URL distribution for an issue
```
get_issue_tag_values(organizationSlug='my-organization', issueId='PROJECT-123', tagKey='url')
```

### Get browser distribution using issue URL
```
get_issue_tag_values(issueUrl='https://sentry.io/issues/PROJECT-123/', tagKey='browser')
```

### Get environment distribution
```
get_issue_tag_values(organizationSlug='my-organization', issueId='PROJECT-123', tagKey='environment')
```
</examples>

<hints>
- If user provides a Sentry URL, pass the ENTIRE URL to issueUrl parameter unchanged
- Common tag keys: url, browser, browser.name, os, environment, release, device, user
- Tag keys are case-sensitive
</hints>

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organizationSlug | `str` | No | The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool. |
| regionUrl | `str | None` | No | The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool. |
| issueId | `str` | No | The Issue ID. e.g. `PROJECT-1Z43` |
| issueUrl | `str` | No | The URL of the issue. e.g. https://my-organization.sentry.io/issues/PROJECT-1Z43 |
| tagKey | `str` | Yes | The tag key to get values for (e.g., 'url', 'browser', 'environment', 'release'). |

**Example:**
```python
result = await app.get_issue_tag_values(organizationSlug="example", regionUrl="example", issueId="example")
```

### get_trace_details

Get detailed information about a specific Sentry trace by ID.

USE THIS TOOL WHEN USERS:
- Provide a specific trace ID (e.g., 'a4d1aae7216b47ff8117cf4e09ce9d0a')
- Ask to 'show me trace [TRACE-ID]', 'explain trace [TRACE-ID]'
- Want high-level overview and link to view trace details in Sentry
- Need trace statistics and span breakdown

DO NOT USE for:
- General searching for traces (use search_events with trace queries)
- Individual span details (this shows trace overview)

TRIGGER PATTERNS:
- 'Show me trace abc123' → use get_trace_details
- 'Explain trace a4d1aae7216b47ff8117cf4e09ce9d0a' → use get_trace_details
- 'What is trace [trace-id]' → use get_trace_details

<examples>
### Get trace overview
```
get_trace_details(organizationSlug='my-organization', traceId='a4d1aae7216b47ff8117cf4e09ce9d0a')
```
</examples>

<hints>
- Trace IDs are 32-character hexadecimal strings
</hints>

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organizationSlug | `str` | Yes | The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool. |
| regionUrl | `str | None` | No | The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool. |
| traceId | `str` | Yes | The trace ID. e.g. `a4d1aae7216b47ff8117cf4e09ce9d0a` |

**Example:**
```python
result = await app.get_trace_details(organizationSlug="example", regionUrl="example", traceId="example")
```

### get_event_attachment

Download attachments from a Sentry event.

Use this tool when you need to:
- Download files attached to a specific event
- Access screenshots, log files, or other attachments uploaded with an error report
- Retrieve attachment metadata and download URLs

<examples>
### Download a specific attachment by ID

```
get_event_attachment(organizationSlug='my-organization', projectSlug='my-project', eventId='c49541c747cb4d8aa3efb70ca5aba243', attachmentId='12345')
```

### List all attachments for an event

```
get_event_attachment(organizationSlug='my-organization', projectSlug='my-project', eventId='c49541c747cb4d8aa3efb70ca5aba243')
```

</examples>

<hints>
- If `attachmentId` is provided, the specific attachment will be downloaded as an embedded resource
- If `attachmentId` is omitted, all attachments for the event will be listed with download information
- The `projectSlug` is required to identify which project the event belongs to
</hints>

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organizationSlug | `str` | Yes | The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool. |
| projectSlug | `str` | Yes | The project's slug. You can find a list of existing projects in an organization using the `find_projects()` tool. |
| eventId | `str` | Yes | The ID of the event. |
| attachmentId | `str | None` | No | The ID of the attachment to download. |
| regionUrl | `str | None` | No | The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool. |

**Example:**
```python
result = await app.get_event_attachment(organizationSlug="example", projectSlug="example", eventId="example")
```

### search_events

Search for events AND perform counts/aggregations - the ONLY tool for statistics and counts.

Supports TWO query types:
1. AGGREGATIONS (counts, sums, averages): 'how many errors', 'count of issues', 'total tokens'
2. Individual events with timestamps: 'show me error logs from last hour'

USE THIS FOR ALL COUNTS/STATISTICS:
- 'how many errors today' → returns count
- 'count of database failures' → returns count
- 'total number of issues' → returns count
- 'average response time' → returns avg()
- 'sum of tokens used' → returns sum()

ALSO USE FOR INDIVIDUAL EVENTS:
- 'error logs from last hour' → returns event list
- 'database errors with timestamps' → returns event list
- 'trace spans for slow API calls' → returns span list

Dataset Selection (AI automatically chooses):
- errors: Exception/crash events
- logs: Log entries
- spans: Performance data, AI/LLM calls, token usage

DO NOT USE for grouped issue lists → use search_issues

<examples>
search_events(organizationSlug='my-org', naturalLanguageQuery='how many errors today')
search_events(organizationSlug='my-org', naturalLanguageQuery='count of database failures this week')
search_events(organizationSlug='my-org', naturalLanguageQuery='total tokens used by model')
search_events(organizationSlug='my-org', naturalLanguageQuery='error logs from the last hour')
</examples>

<hints>
- If the user passes a parameter in the form of name/otherName, it's likely in the format of <organizationSlug>/<projectSlug>.
- Parse org/project notation directly without calling find_organizations or find_projects.
</hints>

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| organizationSlug | `str` | Yes | The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool. |
| naturalLanguageQuery | `str` | Yes | Natural language description of what you want to search for |
| projectSlug | `str | None` | No | The project's slug. You can find a list of existing projects in an organization using the `find_projects()` tool. |
| regionUrl | `str | None` | No | The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool. |
| limit | `float` | No | Maximum number of results to return |
| includeExplanation | `bool` | No | Include explanation of how the query was translated |

**Example:**
```python
result = await app.search_events(organizationSlug="example", naturalLanguageQuery="example", projectSlug="example")
```

### analyze_issue_with_seer

Use Seer to analyze production errors and get detailed root cause analysis with specific code fixes.

Use this tool when:
- The user explicitly asks for root cause analysis, Seer analysis, or help fixing/debugging an issue
- You are unable to accurately determine the root cause from the issue details alone

Do NOT call this tool as an automatic follow-up to get_issue_details.

What this tool provides:
- Root cause analysis with code-level explanations
- Specific file locations and line numbers where errors occur
- Concrete code fixes you can apply
- Step-by-step implementation guidance

This tool automatically:
1. Checks if analysis already exists (instant results)
2. Starts new AI analysis if needed (~2-5 minutes)
3. Returns complete fix recommendations

<examples>
### User: "Run Seer on this issue"

```
analyze_issue_with_seer(issueUrl='https://my-org.sentry.io/issues/PROJECT-1Z43')
```

### User: "Analyze this issue and suggest a fix"

```
analyze_issue_with_seer(organizationSlug='my-organization', issueId='ERROR-456')
```
</examples>

<hints>
- Only use when the user explicitly requests analysis or you cannot determine the root cause from issue details alone
- If the user provides an issueUrl, extract it and use that parameter alone
- The analysis includes actual code snippets and fixes, not just error descriptions
- Results are cached - subsequent calls return instantly
</hints>

*...additional tools omitted for brevity*
