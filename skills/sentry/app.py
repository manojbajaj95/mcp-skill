"""Application for interacting with Sentry via MCP."""
from typing import Any
from fastmcp import Client
from mcp_skill.auth import OAuth
import json

class SentryApp:
    """
    Application for interacting with Sentry via MCP.
    Provides tools to interact with tools: whoami, find_organizations, find_teams, find_projects, find_releases and 8 more.
    """

    def __init__(self, url: str = "https://mcp.sentry.dev/mcp", auth=None) -> None:
        self.url = url
        self._oauth_auth = auth

    def _get_client(self) -> Client:
        oauth = self._oauth_auth or OAuth()
        return Client(self.url, auth=oauth)

    async def whoami(self) -> dict[str, Any]:
        """
        Identify the authenticated user in Sentry.

Use this tool when you need to:
- Get the user's name and email address.

        Returns:
            Tool execution result

        Tags:
            whoami
        """
        async with self._get_client() as client:
            call_args = {}
            result = await client.call_tool("whoami", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def find_organizations(self, query: str | None = None) -> dict[str, Any]:
        """
        Find organizations that the user has access to in Sentry.

Use this tool when you need to:
- View organizations in Sentry
- Find an organization's slug to aid other tool requests
- Search for specific organizations by name or slug

Returns up to 25 results. If you hit this limit, use the query parameter to narrow down results.

        Args:
            query: Search query to filter results by name or slug. Use this to narrow down results when there are many items.

        Returns:
            Tool execution result

        Tags:
            find, organizations
        """
        async with self._get_client() as client:
            call_args = {}
            if query is not None:
                call_args["query"] = query
            result = await client.call_tool("find_organizations", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def find_teams(self, organizationSlug: str, query: str | None = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
        Find teams in an organization in Sentry.

Use this tool when you need to:
- View teams in a Sentry organization
- Find a team's slug and numeric ID to aid other tool requests
- Search for specific teams by name or slug

Returns up to 25 results. If you hit this limit, use the query parameter to narrow down results.

        Args:
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            query: Search query to filter results by name or slug. Use this to narrow down results when there are many items.
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            find, teams
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["organizationSlug"] = organizationSlug
            if query is not None:
                call_args["query"] = query
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("find_teams", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def find_projects(self, organizationSlug: str, query: str | None = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
        Find projects in Sentry.

Use this tool when you need to:
- View projects in a Sentry organization
- Find a project's slug to aid other tool requests
- Search for specific projects by name or slug

Returns up to 25 results. If you hit this limit, use the query parameter to narrow down results.

        Args:
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            query: Search query to filter results by name or slug. Use this to narrow down results when there are many items.
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            find, projects
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["organizationSlug"] = organizationSlug
            if query is not None:
                call_args["query"] = query
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("find_projects", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def find_releases(self, organizationSlug: str, projectSlug: str | None = None, query: str | None = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
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

        Args:
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            projectSlug: The project's slug. This will default to all projects you have access to. It is encouraged to specify this when possible.
            query: Search for versions which contain the provided string.
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            find, releases
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["organizationSlug"] = organizationSlug
            if projectSlug is not None:
                call_args["projectSlug"] = projectSlug
            if query is not None:
                call_args["query"] = query
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("find_releases", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_issue_details(self, eventId: str = None, issueId: str = None, issueUrl: str = None, organizationSlug: str = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
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

        Args:
            eventId: The ID of the event.
            issueId: The Issue ID. e.g. `PROJECT-1Z43`
            issueUrl: The URL of the issue. e.g. https://my-organization.sentry.io/issues/PROJECT-1Z43
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            issue, details
        """
        async with self._get_client() as client:
            call_args = {}
            if eventId is not None:
                call_args["eventId"] = eventId
            if issueId is not None:
                call_args["issueId"] = issueId
            if issueUrl is not None:
                call_args["issueUrl"] = issueUrl
            if organizationSlug is not None:
                call_args["organizationSlug"] = organizationSlug
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("get_issue_details", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_issue_tag_values(self, tagKey: str, issueId: str = None, issueUrl: str = None, organizationSlug: str = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
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

        Args:
            tagKey: The tag key to get values for (e.g., 'url', 'browser', 'environment', 'release').
            issueId: The Issue ID. e.g. `PROJECT-1Z43`
            issueUrl: The URL of the issue. e.g. https://my-organization.sentry.io/issues/PROJECT-1Z43
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            issue, tag, values
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["tagKey"] = tagKey
            if issueId is not None:
                call_args["issueId"] = issueId
            if issueUrl is not None:
                call_args["issueUrl"] = issueUrl
            if organizationSlug is not None:
                call_args["organizationSlug"] = organizationSlug
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("get_issue_tag_values", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_trace_details(self, organizationSlug: str, traceId: str, regionUrl: str | None = None) -> dict[str, Any]:
        """
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

        Args:
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            traceId: The trace ID. e.g. `a4d1aae7216b47ff8117cf4e09ce9d0a`
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            trace, details
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["organizationSlug"] = organizationSlug
            call_args["traceId"] = traceId
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("get_trace_details", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_event_attachment(self, eventId: str, organizationSlug: str, projectSlug: str, attachmentId: str | None = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
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

        Args:
            eventId: The ID of the event.
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            projectSlug: The project's slug. You can find a list of existing projects in an organization using the `find_projects()` tool.
            attachmentId: The ID of the attachment to download.
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            event, attachment
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["eventId"] = eventId
            call_args["organizationSlug"] = organizationSlug
            call_args["projectSlug"] = projectSlug
            if attachmentId is not None:
                call_args["attachmentId"] = attachmentId
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("get_event_attachment", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def search_events(self, naturalLanguageQuery: str, organizationSlug: str, includeExplanation: bool = None, limit: float = None, projectSlug: str | None = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
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

        Args:
            naturalLanguageQuery: Natural language description of what you want to search for
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            includeExplanation: Include explanation of how the query was translated
            limit: Maximum number of results to return
            projectSlug: The project's slug. You can find a list of existing projects in an organization using the `find_projects()` tool.
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            search, events
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["naturalLanguageQuery"] = naturalLanguageQuery
            call_args["organizationSlug"] = organizationSlug
            if includeExplanation is not None:
                call_args["includeExplanation"] = includeExplanation
            if limit is not None:
                call_args["limit"] = limit
            if projectSlug is not None:
                call_args["projectSlug"] = projectSlug
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("search_events", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def analyze_issue_with_seer(self, instruction: str = None, issueId: str = None, issueUrl: str = None, organizationSlug: str = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
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

        Args:
            instruction: Optional custom instruction for the AI analysis
            issueId: The Issue ID. e.g. `PROJECT-1Z43`
            issueUrl: The URL of the issue. e.g. https://my-organization.sentry.io/issues/PROJECT-1Z43
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            analyze, issue, with, seer
        """
        async with self._get_client() as client:
            call_args = {}
            if instruction is not None:
                call_args["instruction"] = instruction
            if issueId is not None:
                call_args["issueId"] = issueId
            if issueUrl is not None:
                call_args["issueUrl"] = issueUrl
            if organizationSlug is not None:
                call_args["organizationSlug"] = organizationSlug
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("analyze_issue_with_seer", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def search_issues(self, naturalLanguageQuery: str, organizationSlug: str, includeExplanation: bool = None, limit: float = None, projectSlugOrId: str | None = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
        Search for grouped issues/problems in Sentry - returns a LIST of issues, NOT counts or aggregations.

Uses AI to translate natural language queries into Sentry issue search syntax.
Returns grouped issues with metadata like title, status, and user count.

USE THIS TOOL WHEN USERS WANT:
- A LIST of issues: 'show me issues', 'what problems do we have'
- Filtered issue lists: 'unresolved issues', 'critical bugs'
- Issues by impact: 'errors affecting more than 100 users'
- Issues by assignment: 'issues assigned to me'
- User feedback: 'show me user feedback', 'feedback from last week'

DO NOT USE FOR COUNTS/AGGREGATIONS:
- 'how many errors' → use search_events
- 'count of issues' → use search_events
- 'total number of errors today' → use search_events
- 'sum/average/statistics' → use search_events

ALSO DO NOT USE FOR:
- Individual error events with timestamps → use search_events
- Details about a specific issue ID → use get_issue_details

REMEMBER: This tool returns a LIST of issues, not counts or statistics!

<examples>
search_issues(organizationSlug='my-org', naturalLanguageQuery='critical bugs from last week')
search_issues(organizationSlug='my-org', naturalLanguageQuery='unhandled errors affecting 100+ users')
search_issues(organizationSlug='my-org', naturalLanguageQuery='issues assigned to me')
search_issues(organizationSlug='my-org', naturalLanguageQuery='user feedback from production')
</examples>

<hints>
- If the user passes a parameter in the form of name/otherName, it's likely in the format of <organizationSlug>/<projectSlugOrId>.
- Parse org/project notation directly without calling find_organizations or find_projects.
- The projectSlugOrId parameter accepts both project slugs (e.g., 'my-project') and numeric IDs (e.g., '123456').
</hints>

        Args:
            naturalLanguageQuery: Natural language description of issues to search for
            organizationSlug: The organization's slug. You can find a existing list of organizations you have access to using the `find_organizations()` tool.
            includeExplanation: Include explanation of how the query was translated
            limit: Maximum number of issues to return
            projectSlugOrId: The project's slug or numeric ID (optional)
            regionUrl: The region URL for the organization you're querying, if known. For Sentry's Cloud Service (sentry.io), this is typically the region-specific URL like 'https://us.sentry.io'. For self-hosted Sentry installations, this parameter is usually not needed and should be omitted. You can find the correct regionUrl from the organization details using the `find_organizations()` tool.

        Returns:
            Tool execution result

        Tags:
            search, issues
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["naturalLanguageQuery"] = naturalLanguageQuery
            call_args["organizationSlug"] = organizationSlug
            if includeExplanation is not None:
                call_args["includeExplanation"] = includeExplanation
            if limit is not None:
                call_args["limit"] = limit
            if projectSlugOrId is not None:
                call_args["projectSlugOrId"] = projectSlugOrId
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("search_issues", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def search_issue_events(self, naturalLanguageQuery: str, includeExplanation: bool = None, issueId: str = None, issueUrl: str = None, limit: float = None, organizationSlug: str | None = None, projectSlug: str | None = None, regionUrl: str | None = None) -> dict[str, Any]:
        """
        Search and filter events within a specific issue using natural language queries.

Use this to filter events by time, environment, release, user, trace ID, or other tags. The tool automatically constrains results to the specified issue.

For cross-issue searches use search_issues, for single event details use get_issue_details.

<examples>
search_issue_events(issueId='MCP-41', organizationSlug='my-org', naturalLanguageQuery='from last hour')
search_issue_events(issueUrl='https://sentry.io/.../issues/123/', naturalLanguageQuery='production with release v1.0')
</examples>

        Args:
            naturalLanguageQuery: Natural language description of what events you want to find within this issue. Examples: 'from last hour', 'production with release v1.0', 'affecting user alice@example.com', 'with trace ID abc123'
            includeExplanation: Include explanation of how the natural language query was translated to Sentry syntax
            issueId: Issue ID (e.g., 'MCP-41', 'PROJECT-123'). Requires organizationSlug. Alternatively, use issueUrl.
            issueUrl: Full Sentry issue URL (e.g., 'https://sentry.io/organizations/my-org/issues/123/'). Includes both organization and issue ID.
            limit: Maximum number of events to return (1-100, default: 50)
            organizationSlug: Organization slug. Required when using issueId. Not needed when using issueUrl.
            projectSlug: Project slug for better tag discovery. Optional - helps find project-specific tags.
            regionUrl: Sentry region URL. Optional - defaults to main region.

        Returns:
            Tool execution result

        Tags:
            search, issue, events
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["naturalLanguageQuery"] = naturalLanguageQuery
            if includeExplanation is not None:
                call_args["includeExplanation"] = includeExplanation
            if issueId is not None:
                call_args["issueId"] = issueId
            if issueUrl is not None:
                call_args["issueUrl"] = issueUrl
            if limit is not None:
                call_args["limit"] = limit
            if organizationSlug is not None:
                call_args["organizationSlug"] = organizationSlug
            if projectSlug is not None:
                call_args["projectSlug"] = projectSlug
            if regionUrl is not None:
                call_args["regionUrl"] = regionUrl
            result = await client.call_tool("search_issue_events", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    def list_tools(self):
        return [self.whoami, self.find_organizations, self.find_teams, self.find_projects, self.find_releases, self.get_issue_details, self.get_issue_tag_values, self.get_trace_details, self.get_event_attachment, self.search_events, self.analyze_issue_with_seer, self.search_issues, self.search_issue_events]
