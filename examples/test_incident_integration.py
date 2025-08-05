#!/usr/bin/env python3
"""
Integration test for the get_incident_by_number tool.

This script tests the integration of the get_incident_by_number tool
within the MCP framework to ensure it's properly registered and callable.
"""

import os
import sys
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from servicenow_mcp.utils.tool_utils import get_tool_definitions
from servicenow_mcp.tools.knowledge_base import (
    create_category as create_kb_category_tool,
    list_categories as list_kb_categories_tool,
)


def test_tool_registration():
    """Test that the get_incident_by_number tool is properly registered."""
    print("🔧 Testing Tool Registration")
    print("=" * 40)
    
    # Get tool definitions
    tool_definitions = get_tool_definitions(create_kb_category_tool, list_kb_categories_tool)
    
    # Check if our tool is registered
    tool_name = "get_incident_by_number"
    if tool_name in tool_definitions:
        print(f"✅ Tool '{tool_name}' is registered")
        
        # Get tool definition details
        impl_func, params_model, return_annotation, description, serialization = tool_definitions[tool_name]
        
        print(f"   Description: {description}")
        print(f"   Parameters Model: {params_model.__name__}")
        print(f"   Return Type: {return_annotation}")
        print(f"   Serialization: {serialization}")
        
        # Test parameter schema generation
        try:
            schema = params_model.model_json_schema()
            print(f"   ✅ Parameter schema generated successfully")
            print(f"      Required fields: {schema.get('required', [])}")
            
            # Pretty print the schema for verification
            print("\n📋 Parameter Schema:")
            print(json.dumps(schema, indent=2))
            
        except Exception as e:
            print(f"   ❌ Error generating parameter schema: {e}")
            return False
        
        return True
    else:
        print(f"❌ Tool '{tool_name}' is NOT registered")
        print(f"   Available tools: {list(tool_definitions.keys())}")
        return False


def test_tool_package_inclusion():
    """Test that the tool is included in the expected packages."""
    print("\n📦 Testing Tool Package Inclusion")
    print("=" * 40)
    
    import yaml
    
    # Load the tool packages configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'tool_packages.yaml')
    
    try:
        with open(config_path, 'r') as f:
            packages = yaml.safe_load(f)
        
        tool_name = "get_incident_by_number"
        found_in_packages = []
        
        for package_name, tools in packages.items():
            if tool_name in tools:
                found_in_packages.append(package_name)
        
        if found_in_packages:
            print(f"✅ Tool '{tool_name}' found in packages: {found_in_packages}")
            return True
        else:
            print(f"❌ Tool '{tool_name}' not found in any package")
            return False
            
    except Exception as e:
        print(f"❌ Error loading package configuration: {e}")
        return False


def test_parameter_validation():
    """Test parameter validation for the tool."""
    print("\n🔍 Testing Parameter Validation")
    print("=" * 40)
    
    from servicenow_mcp.tools.incident_tools import GetIncidentByNumberParams
    
    # Test valid parameters
    try:
        valid_params = GetIncidentByNumberParams(incident_number="INC0010001")
        print(f"✅ Valid parameters accepted: {valid_params.incident_number}")
    except Exception as e:
        print(f"❌ Error with valid parameters: {e}")
        return False
    
    # Test invalid parameters (missing required field)
    try:
        invalid_params = GetIncidentByNumberParams()
        print(f"❌ Invalid parameters should have been rejected")
        return False
    except Exception as e:
        print(f"✅ Invalid parameters correctly rejected: {type(e).__name__}")
    
    # Test parameter types
    try:
        # Test with non-string incident number
        invalid_type_params = GetIncidentByNumberParams(incident_number=12345)
        print(f"   Incident number as integer: {invalid_type_params.incident_number} (converted to string)")
    except Exception as e:
        print(f"   Type conversion error: {e}")
    
    return True


def main():
    """Run all integration tests."""
    print("🚀 ServiceNow MCP Tool Integration Test")
    print("=" * 50)
    print("Testing get_incident_by_number tool integration\n")
    
    tests = [
        test_tool_registration,
        test_tool_package_inclusion,
        test_parameter_validation,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    print("📊 Test Summary")
    print("=" * 20)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} tests passed!")
        print("\n🎉 The get_incident_by_number tool is properly integrated and ready to use.")
    else:
        print(f"❌ {passed}/{total} tests passed")
        print("\n⚠️  Some integration issues were found. Please review the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
