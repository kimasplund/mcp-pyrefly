#!/usr/bin/env python3
"""Simple test script for MCP Pyrefly server."""

import asyncio
import json
from src.mcp_pyrefly.server import check_code, track_identifier, check_consistency, suggest_fix
from src.mcp_pyrefly.server import CodeCheckRequest, IdentifierTrackRequest, ConsistencyCheckRequest


async def test_basic_functionality():
    """Test basic server functionality."""
    print("Testing MCP Pyrefly Server...\n")
    
    # Test 1: Check valid code
    print("1. Testing valid code:")
    valid_code = '''
def get_user_data(user_id: str) -> dict:
    """Get user data by ID."""
    return {"id": user_id, "name": "Test User"}
'''
    
    result = await check_code(CodeCheckRequest(code=valid_code, filename="test.py"), context=None)
    print(f"   Success: {result.success}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Warnings: {len(result.warnings)}")
    print()
    
    # Test 2: Check code with type error
    print("2. Testing code with type error:")
    error_code = '''
def get_user_data(user_id: str) -> dict:
    return {"id": user_id, "name": "Test User"}

# Type error: passing int instead of str
result = get_user_data(123)
'''
    
    result = await check_code(CodeCheckRequest(code=error_code, filename="test.py"), context=None)
    print(f"   Success: {result.success}")
    print(f"   Errors: {len(result.errors)}")
    if result.errors:
        print(f"   First error: {result.errors[0].get('message', 'N/A')}")
    if result.suggestions:
        print("   Suggestions:")
        for i, suggestion in enumerate(result.suggestions[:3]):
            print(f"     - {suggestion}")
    print()
    
    # Test 3: Check naming consistency
    print("3. Testing naming consistency:")
    
    # First, track the original function
    await track_identifier(IdentifierTrackRequest(
        name="get_user_data",
        type="function",
        signature="(user_id: str) -> dict"
    ), context=None)
    
    # Now check inconsistent code
    inconsistent_code = '''
# Using different naming convention
data = getUserData("123")  # Should be get_user_data
'''
    
    result = await check_code(CodeCheckRequest(code=inconsistent_code, filename="test2.py"), context=None)
    print(f"   Success: {result.success}")
    print(f"   Consistency issues: {len(result.consistency_issues)}")
    if result.consistency_issues:
        issue = result.consistency_issues[0]
        print(f"   Issue: {issue.get('issue', 'N/A')}")
        print(f"   Suggestion: Use '{issue.get('suggestion', 'N/A')}' instead")
    print()
    
    # Test 4: Check consistency directly
    print("4. Testing direct consistency check:")
    consistency = await check_consistency(
        ConsistencyCheckRequest(identifier="getUserData"),
        context=None
    )
    print(f"   Consistent: {consistency.get('consistent', 'N/A')}")
    if not consistency.get('consistent'):
        print(f"   Issue: {consistency.get('issue', 'N/A')}")
        print(f"   Suggestion: {consistency.get('suggestion', 'N/A')}")
    print()
    
    # Test 5: Get fix suggestions
    print("5. Testing fix suggestions:")
    fix_result = await suggest_fix(
        error_message="NameError: name 'getUserData' is not defined",
        context=None
    )
    print(f"   Has suggestions: {fix_result.get('has_suggestions', False)}")
    if fix_result.get('suggestions'):
        print("   Suggestions:")
        for suggestion in fix_result.get('suggestions', [])[:2]:
            print(f"     - {suggestion}")
    print()
    
    print("Tests completed!")


if __name__ == "__main__":
    asyncio.run(test_basic_functionality())