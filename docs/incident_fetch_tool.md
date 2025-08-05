# Incident Data Retrieval Tool

This document describes the `get_incident_by_number` tool for fetching incident data from ServiceNow's incident table based on ticket ID.

## Overview

The `get_incident_by_number` tool allows you to retrieve detailed information about a specific incident from your ServiceNow instance using the incident number (ticket ID). This tool is particularly useful for:

- Looking up incident details for support cases
- Retrieving incident status and assignment information
- Getting incident history and metadata
- Integrating incident data into external systems

## Tool Details

### Function Name
`get_incident_by_number`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `incident_number` | string | Yes | The incident number/ticket ID to fetch (e.g., "INC0010001") |

### Response Format

The tool returns a JSON response with the following structure:

```json
{
  "success": true,
  "message": "Incident INC0010001 found",
  "incident": {
    "sys_id": "a1b2c3d4e5f6789012345678901234567890abcd",
    "number": "INC0010001",
    "short_description": "Unable to access email",
    "description": "User reports that they cannot access their corporate email...",
    "state": "In Progress",
    "priority": "3 - Moderate",
    "assigned_to": "John Doe",
    "category": "Software",
    "subcategory": "Email",
    "created_on": "2025-01-15 09:30:00",
    "updated_on": "2025-01-15 14:22:00"
  }
}
```

### Error Response

If the incident is not found or an error occurs:

```json
{
  "success": false,
  "message": "Incident not found: INC0010001"
}
```

## Usage Examples

### MCP Tool Call

```json
{
  "tool": "get_incident_by_number",
  "parameters": {
    "incident_number": "INC0010001"
  }
}
```

### Python Code Example

```python
from servicenow_mcp.tools.incident_tools import get_incident_by_number, GetIncidentByNumberParams

# Create parameters
params = GetIncidentByNumberParams(incident_number="INC0010001")

# Call the tool
result = get_incident_by_number(config, auth_manager, params)

# Process results
if result["success"]:
    incident = result["incident"]
    print(f"Incident: {incident['number']}")
    print(f"Description: {incident['short_description']}")
    print(f"Status: {incident['state']}")
else:
    print(f"Error: {result['message']}")
```

## ServiceNow API Details

### Endpoint
- **URL**: `https://<instance>.service-now.com/api/now/table/incident`
- **Method**: GET
- **Query**: `sysparm_query=number=<incident_number>`

### Required Permissions
- `incident` table read access
- Valid ServiceNow user credentials

### API Parameters Used
- `sysparm_query`: Filters incidents by number
- `sysparm_limit`: Limits results to 1 incident
- `sysparm_display_value`: Returns human-readable values
- `sysparm_exclude_reference_link`: Excludes reference links for cleaner output

## Tool Package Configuration

This tool is included in the following tool packages:

- **service_desk**: Essential tools for service desk operations
- **full**: Complete set of all available tools

To use this tool, ensure your MCP server is configured with one of these packages:

```bash
export MCP_TOOL_PACKAGE=service_desk
# or
export MCP_TOOL_PACKAGE=full
```

## Common Use Cases

### 1. Support Case Lookup
Quickly retrieve incident details when handling support requests:
```
User: "Can you check the status of ticket INC0010001?"
Tool Call: get_incident_by_number(incident_number="INC0010001")
```

### 2. Incident Status Monitoring
Check current status and assignment of incidents:
```python
# Monitor multiple incidents
incident_numbers = ["INC0010001", "INC0010002", "INC0010003"]
for number in incident_numbers:
    result = get_incident_by_number(config, auth_manager, 
                                   GetIncidentByNumberParams(incident_number=number))
    if result["success"]:
        incident = result["incident"]
        print(f"{number}: {incident['state']} - {incident['assigned_to']}")
```

### 3. Integration with External Systems
Extract incident data for reporting or external system integration:
```python
def sync_incident_to_external_system(incident_number):
    result = get_incident_by_number(config, auth_manager, 
                                   GetIncidentByNumberParams(incident_number=incident_number))
    if result["success"]:
        incident_data = result["incident"]
        # Send to external system
        external_api.create_or_update_ticket(incident_data)
```

## Error Handling

The tool handles several error scenarios:

1. **Incident Not Found**: Returns success=false with appropriate message
2. **Network Errors**: Catches requests exceptions and returns error details
3. **Authentication Errors**: Handled by the auth_manager
4. **Invalid Parameters**: Validated by Pydantic model

## Related Tools

- `list_incidents`: List multiple incidents with filtering
- `create_incident`: Create new incidents
- `update_incident`: Modify existing incidents
- `add_comment`: Add comments to incidents
- `resolve_incident`: Resolve incidents

## Demo Script

Run the included demo script to test the functionality:

```bash
cd examples
python incident_fetch_demo.py
```

Make sure to set your ServiceNow credentials:
```bash
export SERVICENOW_USERNAME=your_username
export SERVICENOW_PASSWORD=your_password
```
