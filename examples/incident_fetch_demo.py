#!/usr/bin/env python3
"""
ServiceNow MCP Incident Fetch Demo

This script demonstrates how to use the get_incident_by_number tool
to fetch incident data from ServiceNow's incident table based on ticket ID.

Usage:
    python incident_fetch_demo.py
"""

import os
import sys
import logging
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from servicenow_mcp.tools.incident_tools import get_incident_by_number, GetIncidentByNumberParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, AuthType, BasicAuthConfig
from servicenow_mcp.auth.auth_manager import AuthManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_fetch_incident():
    """
    Demonstrates fetching an incident by its number/ticket ID.
    
    This example shows how to:
    1. Set up the ServiceNow configuration
    2. Create authentication manager
    3. Use the get_incident_by_number tool to fetch incident data
    """
    
    print("🎫 ServiceNow Incident Fetch Demo")
    print("=" * 50)
    
    # Note: Replace these with your actual ServiceNow instance details
    instance_url = "https://netappengdevalt.service-now.com"
    
    # You can get these from environment variables or configuration
    username = os.getenv("SERVICENOW_USERNAME", "your_username")
    password = os.getenv("SERVICENOW_PASSWORD", "your_password")
    
    if username == "your_username" or password == "your_password":
        print("⚠️  Please set SERVICENOW_USERNAME and SERVICENOW_PASSWORD environment variables")
        print("   or update the script with your credentials.")
        return
    
    try:
        # Set up authentication configuration
        auth_config = AuthConfig(
            type=AuthType.BASIC,
            basic=BasicAuthConfig(username=username, password=password)
        )
        
        # Create server configuration
        config = ServerConfig(
            instance_url=instance_url,
            auth=auth_config,
            timeout=30
        )
        
        # Create authentication manager
        auth_manager = AuthManager(auth_config, instance_url)
        
        # Example incident numbers to fetch
        # Replace these with actual incident numbers from your ServiceNow instance
        incident_numbers = [
            "INC0010001",  # Replace with actual incident number
            "INC0010002",  # Replace with actual incident number
        ]
        
        print(f"🔍 Fetching incidents from: {instance_url}")
        print()
        
        for incident_number in incident_numbers:
            print(f"📋 Fetching incident: {incident_number}")
            
            # Create parameters for the tool
            params = GetIncidentByNumberParams(incident_number=incident_number)
            
            # Call the tool function
            result = get_incident_by_number(config, auth_manager, params)
            
            # Display results
            if result.get("success"):
                incident = result.get("incident", {})
                print(f"  ✅ Success: {result.get('message')}")
                print(f"     System ID: {incident.get('sys_id')}")
                print(f"     Number: {incident.get('number')}")
                print(f"     Short Description: {incident.get('short_description')}")
                print(f"     State: {incident.get('state')}")
                print(f"     Priority: {incident.get('priority')}")
                print(f"     Assigned To: {incident.get('assigned_to')}")
                print(f"     Category: {incident.get('category')}")
                print(f"     Created: {incident.get('created_on')}")
                print(f"     Updated: {incident.get('updated_on')}")
            else:
                print(f"  ❌ Failed: {result.get('message')}")
            
            print()
    
    except Exception as e:
        logger.error(f"Error during incident fetch demo: {e}")
        print(f"❌ Error: {e}")


def demo_tool_usage():
    """
    Shows how the tool can be used within the MCP framework.
    """
    print("\n🔧 MCP Tool Usage Example")
    print("=" * 50)
    
    example_request = {
        "tool": "get_incident_by_number",
        "parameters": {
            "incident_number": "INC0010001"
        }
    }
    
    print("Example MCP tool request:")
    print(f"  Tool: {example_request['tool']}")
    print(f"  Parameters: {example_request['parameters']}")
    print()
    
    print("This tool will:")
    print("  1. Query the ServiceNow incident table")
    print("  2. Search for the incident by number")
    print("  3. Return detailed incident information including:")
    print("     - System ID and incident number")
    print("     - Short description and full description")
    print("     - Current state and priority")
    print("     - Assigned user and category")
    print("     - Creation and update timestamps")
    print()
    
    print("API Endpoint used:")
    print("  GET https://netappengdevalt.service-now.com/api/now/table/incident")
    print("  Query: number=<incident_number>")


if __name__ == "__main__":
    print("🚀 Starting ServiceNow Incident Fetch Demo\n")
    
    # Demonstrate tool usage
    demo_tool_usage()
    
    # Run the actual demo (requires credentials)
    response = input("Do you want to run the live demo? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        demo_fetch_incident()
    else:
        print("Demo skipped. Set up your credentials and run again to test live functionality.")
    
    print("\n✨ Demo completed!")
