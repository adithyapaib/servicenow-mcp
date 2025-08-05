#!/usr/bin/env python3
"""
Simple test to verify the get_incident_by_number tool functionality
without requiring the full MCP environment.
"""

import os
import sys
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_import_and_basic_functionality():
    """Test importing the tool and its basic functionality."""
    print("🔧 Testing Tool Import and Basic Functionality")
    print("=" * 50)
    
    try:
        # Test imports
        from servicenow_mcp.tools.incident_tools import (
            get_incident_by_number, 
            GetIncidentByNumberParams
        )
        print("✅ Successfully imported get_incident_by_number and GetIncidentByNumberParams")
        
        # Test parameter model
        params = GetIncidentByNumberParams(incident_number="INC0010001")
        print(f"✅ Parameter model works: {params.incident_number}")
        
        # Test parameter validation
        try:
            invalid_params = GetIncidentByNumberParams()
            print("❌ Should have failed with missing required parameter")
            return False
        except Exception:
            print("✅ Parameter validation works (correctly rejected missing parameter)")
        
        # Test parameter schema
        schema = GetIncidentByNumberParams.model_json_schema()
        print("✅ Parameter schema generation works")
        print(f"   Required fields: {schema.get('required', [])}")
        
        # Show the schema
        print("\n📋 Parameter Schema:")
        print(json.dumps(schema, indent=2))
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_function_signature():
    """Test the function signature and documentation."""
    print("\n📝 Testing Function Signature and Documentation")
    print("=" * 50)
    
    try:
        from servicenow_mcp.tools.incident_tools import get_incident_by_number
        import inspect
        
        # Get function signature
        sig = inspect.signature(get_incident_by_number)
        print(f"✅ Function signature: {sig}")
        
        # Get docstring
        doc = get_incident_by_number.__doc__
        if doc:
            print("✅ Function has documentation:")
            print(f"   {doc.strip()}")
        else:
            print("⚠️  Function has no documentation")
        
        # Check parameter names
        param_names = list(sig.parameters.keys())
        expected_params = ['config', 'auth_manager', 'params']
        
        if param_names == expected_params:
            print(f"✅ Function parameters match expected: {param_names}")
        else:
            print(f"❌ Unexpected parameters. Expected: {expected_params}, Got: {param_names}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing function signature: {e}")
        return False


def test_tool_package_config():
    """Test that the tool is properly configured in packages."""
    print("\n📦 Testing Tool Package Configuration")
    print("=" * 50)
    
    try:
        import yaml
        
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'tool_packages.yaml')
        
        with open(config_path, 'r') as f:
            packages = yaml.safe_load(f)
        
        tool_name = "get_incident_by_number"
        found_in_packages = []
        
        for package_name, tools in packages.items():
            if isinstance(tools, list) and tool_name in tools:
                found_in_packages.append(package_name)
        
        if found_in_packages:
            print(f"✅ Tool '{tool_name}' found in packages: {found_in_packages}")
            
            # Verify it's in the expected packages
            expected_packages = ['service_desk', 'full']
            missing_packages = [pkg for pkg in expected_packages if pkg not in found_in_packages]
            
            if missing_packages:
                print(f"⚠️  Tool missing from expected packages: {missing_packages}")
            else:
                print(f"✅ Tool found in all expected packages")
            
            return True
        else:
            print(f"❌ Tool '{tool_name}' not found in any package")
            print(f"   Available packages: {list(packages.keys())}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking package configuration: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 ServiceNow MCP Tool Simple Test")
    print("Testing get_incident_by_number tool without full MCP environment\n")
    
    tests = [
        test_import_and_basic_functionality,
        test_function_signature,
        test_tool_package_config,
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
        print("\n🎉 The get_incident_by_number tool is properly configured and ready to use.")
        print("\nNext steps:")
        print("1. Install dependencies: uv sync")
        print("2. Set up ServiceNow credentials")
        print("3. Test with live ServiceNow instance using incident_fetch_demo.py")
    else:
        print(f"❌ {passed}/{total} tests passed")
        print("\n⚠️  Some issues were found. Please review the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
