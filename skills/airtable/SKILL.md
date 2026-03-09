---
name: airtable
description: "MCP skill for airtable. Provides 8 tools: ping, list_bases, search_bases, list_tables_for_base, get_table_schema, list_records_for_table, create_records_for_table, update_records_for_table"
---

# airtable

MCP skill for airtable. Provides 8 tools: ping, list_bases, search_bases, list_tables_for_base, get_table_schema, list_records_for_table, create_records_for_table, update_records_for_table

## Authentication

This MCP server uses **OAuth** authentication.
The OAuth flow is handled automatically by the MCP client. Tokens are persisted
to `~/.mcp-skill/airtable/oauth-tokens/` so subsequent runs reuse the
same credentials without re-authenticating.

```python
app = AirtableApp()  # uses default OAuth flow
```

To bring your own OAuth provider, pass it via the `auth` argument:

```python
app = AirtableApp(auth=my_oauth_provider)
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
from airtable.app import AirtableApp
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from airtable.app import AirtableApp

async def main():
    app = AirtableApp()
    result = await app.ping()
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from airtable.app import AirtableApp

async def main():
    app = AirtableApp()
    result = await app.ping()
    print(result)

asyncio.run(main())
"
```

## Available Tools

### ping

Ping the MCP server to check if it is running

**Example:**
```python
result = await app.ping()
```

### list_bases

Lists all bases that you have access to in your Airtable account.
Use this to get the baseId of the base you want to use.
Favorited and recently viewed bases are generally more relevant.

**Example:**
```python
result = await app.list_bases()
```

### search_bases

Searches for bases by name.
This is useful when you need to find a specific base quickly by a partial name-based match.
Returns bases sorted by their relevance score, as well as a recommended base ID and a hint on whether
we need to ask the user to explicitly select the base they want to use.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| searchQuery | `str` | Yes | The query to search for bases by name.
The search is case-insensitive and works with partial matches.
Examples: "projects", "issues", "customers" |

**Example:**
```python
result = await app.search_bases(searchQuery="example")
```

### list_tables_for_base

Gets the summary of a specific base. This includes the schemas of all tables in the
base, including field name and type.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| baseId | `str` | Yes | The ID of the base to get the summary of.
Must start with "app" and is 14 characters long.
Example: "appZfrNIUEip5MazD".
Do not substitute user-facing names for baseId.
To get baseId, use the search_bases or list_bases tool. |

**Example:**
```python
result = await app.list_tables_for_base(baseId="example")
```

### get_table_schema

Gets the detailed schema information for specified tables and fields in a base.
This returns the field ID, type, and config for the specified fields of the specified tables.
Example: get schema for two fields in a table:
{"baseId": "appZfrNIUEip5MazD", "tables": [{"tableId": "tblGlReoTNWfYnXIG", "fieldIds": ["fld8WsrpLHHevsnW8", "fldgD18XtsueoiguT"]}]}

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| baseId | `str` | Yes | The ID of the base containing the tables.
Must start with "app" and is 14 characters long.
Example: "appZfrNIUEip5MazD".
Do not substitute user-facing names for baseId.
To get baseId, use the search_bases or list_bases tool. |
| tables | `list[Any]` | Yes | An array of table IDs and corresponding field IDs to get schema information for.
Must start with "tbl" and is 14 characters long.
Example: "tblGlReoTNWfYnXIG".
Do not substitute user-facing names for tableId.
To get tableId, use the list_tables_for_base tool.
Field IDs must start with "fld" and is 14 characters long.
Example: "fldGlRtkBNWfYnPOV".
Do not substitute user-facing names for IDs.
To get fieldId, use the list_tables_for_base tool. |

**Example:**
```python
result = await app.get_table_schema(baseId="example", tables="value")
```

### list_records_for_table

Lists records queried from an Airtable table.
Do not assume baseId and tableId. Obtain these from search_bases → list_tables_for_base.
Do not attempt to pass filterByFormula. Look carefully at the filters parameter.
Pre-requisite: If filtering on select/multiSelect fields, you must call get_table_schema first to get the choice IDs.
Aim to provide at least 6 relevant fields via the 'fieldIds' parameter.
Note: Select and multiSelect field values are returned as objects (e.g., {"id": "sel...", "name": "Option", "color": "blue"}) or arrays of such objects. When writing these values back via create_records_for_table or update_records_for_table, use the plain string name (e.g., "Option") instead of the object.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| baseId | `str` | Yes | The ID of the base containing the table.
Must start with "app" and is 14 characters long.
Example: "appZfrNIUEip5MazD".
Do not substitute user-facing names for baseId.
To get baseId, use the search_bases or list_bases tool. |
| tableId | `str` | Yes | The ID of the table to list records from.
Must start with "tbl" and is 14 characters long.
Example: "tblGlReoTNWfYnXIG".
Do not substitute user-facing names for tableId.
To get tableId, use the list_tables_for_base tool. |
| fieldIds | `list[str]` | No | Only data for fields whose IDs are in this list will be included in the result.
Pass in only the fields most useful for the user to see.
If not provided, all fields will be included in the result.
Field IDs must start with "fld" and is 14 characters long.
Example: "fldGlRtkBNWfYnPOV".
Do not substitute user-facing names for IDs.
To get fieldId, use the list_tables_for_base tool. |
| pageSize | `float` | No | The maximum number of records to return in the response.
The server may respond with fewer records than this value when the total set has fewer records than this value.
Defaults to 3000. |
| cursor | `str` | No | The cursor to start from. To begin from the first record, do not include a cursor.
For a subsequent paginated request, include the nextCursor from the previous response. |
| sort | `list[Any]` | No | A list of sort objects that specifies how the records will be ordered.
Each sort object must have a fieldId key specifying the ID of the field to sort on, and an optional direction key that is either "asc" or "desc".
The default direction is "asc".
Records are sorted by the first sort object first, then by the second sort object for records that have the same value for the first sort, and so on.
Example sort by a single field in descending order: [{"fieldId": "fld9x4rqyBSCLzsJM", "direction": "desc"}]
Example sort by two fields, first ascending then descending: [{"fieldId": "fld9x4rqyBSCLzsJM", "direction": "asc"}, {"fieldId": "fldulcCPDVz87Bmnw", "direction": "desc"}] |
| recordIds | `list[str]` | No | An array of record IDs to filter by. Only records with these IDs will be returned.
Must start with "rec" and is 14 characters long.
Example: "recZOTa3BDHxlJNzf".
Do not substitute user-facing names for IDs
To get recordId, use the list_records_for_table tool or display_records_for_table tools. |
| filters | `dict[str, Any]` | No | Describes the filters to apply to the records using a structured format.
Example filter where the value of the field with ID "fld8WsrpLHHevsnW8" is "orange" or the value of the field with ID "fldulcCPDVz87Bmnw" is greater than 5:
{"operator": "or", "operands": [{"operator": "=", "operands": ["fld8WsrpLHHevsnW8", "orange"]}, {"operator": ">", "operands": ["fldulcCPDVz87Bmnw", 5]}]}
Example filter where the value of the collaborator field with ID "fldCRi9oz2vRLcIWr" can be any user in a group with ID "ugpDUVUnftA7H9bG8" and the value of the field with ID "fldgD18XtsueoiguT" equals select option with ID "selha8nGNAT5ATR7P":
{"operator": "and", "operands": [{"operator": "hasAnyOf", "operands": ["fldCRi9oz2vRLcIWr", "ugpDUVUnftA7H9bG8"], "operatorOptions": {"matchGroupsByMembership": true}}, {"operator": "=", "operands": ["fldgD18XtsueoiguT", "selha8nGNAT5ATR7P"]}]}
Example filter for records where a date field is within the past week:
{"operands": [{"operator": "isWithin", "operands": ["fldABC12345678x", {"mode": "pastWeek", "timeZone": "America/New_York"}]}]}
Example filter for records where a field is not empty:
{"operands": [{"operator": "isNotEmpty", "operands": ["fldABC12345678x"]}]} |

**Example:**
```python
result = await app.list_records_for_table(baseId="example", tableId="example", fieldIds="value")
```

### create_records_for_table

Creates new records in an Airtable table.
To get baseId and tableId, use the search_bases and list_tables_for_base tools first.
For select/multiSelect fields, provide the option name as a plain string (e.g., "In progress") or array of strings, not the object format returned by list_records_for_table.
Example: create a record with text, number, select, and multiSelect fields:
{"baseId": "appZfrNIUEip5MazD", "tableId": "tblGlReoTNWfYnXIG", "records": [{"fields": {"fldGlRtkBNWfYnPOV": "Launch meeting", "fldulcCPDVz87Bmnw": 42, "fld8WsrpLHHevsnW8": "In progress", "fldgD18XtsueoiguT": ["Urgent", "Q1"]}}]}

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| baseId | `str` | Yes | The ID of the base containing the table.
Must start with "app" and is 14 characters long.
Example: "appZfrNIUEip5MazD".
Do not substitute user-facing names for baseId.
To get baseId, use the search_bases or list_bases tool. |
| tableId | `str` | Yes | The ID of the table to create a record in.
Must start with "tbl" and is 14 characters long.
Example: "tblGlReoTNWfYnXIG".
Do not substitute user-facing names for tableId.
To get tableId, use the list_tables_for_base tool. |
| records | `list[Any]` | Yes | An array of record objects to create. Each record must have a "fields" property
containing the field values. You can create up to 10 records per request. |
| typecast | `bool` | No | Whether or not to perform best-effort automatic data conversion from string values.
Defaults to false to preserve data integrity. |

**Example:**
```python
result = await app.create_records_for_table(baseId="example", tableId="example", records="value")
```

### update_records_for_table

Updates records in an Airtable table.
The fields you specify will be updated, and all other fields will be left unchanged.
To get baseId and tableId, consider using the search_bases and list_tables_for_base tools first.
For select/multiSelect fields, provide the option name as a plain string (e.g., "In progress") or array of strings, not the object format returned by list_records_for_table.
Example: update a record's fields:
{"baseId": "appZfrNIUEip5MazD", "tableId": "tblGlReoTNWfYnXIG", "records": [{"id": "recZOTa3BDHxlJNzf", "fields": {"fldGlRtkBNWfYnPOV": "Updated name", "fld8WsrpLHHevsnW8": "Done"}}]}

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| baseId | `str` | Yes | The ID of the base containing the table.
Must start with "app" and is 14 characters long.
Example: "appZfrNIUEip5MazD".
Do not substitute user-facing names for baseId.
To get baseId, use the search_bases or list_bases tool. |
| tableId | `str` | Yes | The ID of the table to update records in.
Must start with "tbl" and is 14 characters long.
Example: "tblGlReoTNWfYnXIG".
Do not substitute user-facing names for tableId.
To get tableId, use the list_tables_for_base tool. |
| records | `list[Any]` | Yes | An array of record objects to update. Each record must have a "fields" property
containing the field values. You can update up to 10 records per request. |
| performUpsert | `dict[str, Any]` | No | Enables upsert behavior when set.
When upserting is enabled, the recordId parameter is optional.
Records that do not include a recordId will use the fields chosen by the fieldIdsToMergeOn parameter to match with existing records.
- If no matches are found, a new record will be created.
- If a match is found, that record will be updated.
- If multiple matches are found, the request will fail.
Records that include id will ignore fieldIdsToMergeOn and behave as normal updates.
If no record with the given id exists, the request will fail and will not create a new record |
| typecast | `bool` | No | Whether or not to perform best-effort automatic data conversion from string values.
Defaults to false to preserve data integrity. |

**Example:**
```python
result = await app.update_records_for_table(baseId="example", tableId="example", records="value")
```

