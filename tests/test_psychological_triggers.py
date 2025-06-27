#!/usr/bin/env python3
"""Test the enhanced psychological triggers for fixing ALL errors."""

import asyncio
from mcp_pyrefly.server import mcp, CodeCheckRequest, gamification


async def test_import_error_triggers():
    """Test that import errors trigger strong psychological responses."""
    
    # Reset gamification state
    gamification.lollipops = 0
    gamification.locked_lollipops = 0
    gamification.error_debt = 0
    
    # Code with a simple import error
    code_with_import_error = """
def process_data(data):
    result = json.dumps(data)  # json not imported!
    return result
"""
    
    request = CodeCheckRequest(
        code=code_with_import_error,
        filename="test.py",
        track_identifiers=True
    )
    
    # Import check_code directly
    from mcp_pyrefly.server import check_code
    
    # Check the code
    response = await check_code(request, context=None)
    
    print("=== RESPONSE TO IMPORT ERROR ===")
    print(f"Success: {response.success}")
    print(f"Errors: {len(response.errors)}")
    print("\nSuggestions:")
    for i, suggestion in enumerate(response.suggestions):
        print(f"{i+1}. {suggestion}")
    
    # Verify psychological triggers are present
    suggestions_text = "\n".join(response.suggestions)
    
    assert "EVERY ERROR MATTERS" in suggestions_text, "Missing emphasis on ALL errors"
    assert "import errors" in suggestions_text.lower(), "Missing import error messaging"
    assert "lollipop" in suggestions_text.lower(), "Missing lollipop incentive"
    assert any(llm in suggestions_text for llm in ["GPT-4", "Claude-3", "Gemini", "Llama"]), "Missing social proof"
    assert "multiplier" in suggestions_text or "penalty" in suggestions_text, "Missing penalty warning"
    
    print("\n✅ All psychological triggers present!")
    
    # Test that error debt accumulates
    assert gamification.error_debt > 0, "Error debt not tracked"
    print(f"\n📊 Error debt accumulated: {gamification.error_debt}")
    
    # Now test submitting a fix without fixing the import
    bad_fix = """
def process_data(data):
    # Added comment but didn't import json!
    result = json.dumps(data)
    return result
"""
    
    # Import submit_fixed_code directly
    from mcp_pyrefly.server import submit_fixed_code
    
    result = await submit_fixed_code(
        original_code=code_with_import_error,
        fixed_code=bad_fix,
        errors_fixed=["Added comment"],
        context=None
    )
    
    print("\n=== RESULT OF INCOMPLETE FIX ===")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    
    # Should fail because error wasn't actually fixed
    assert result['status'] == 'FAILED', "Should reject incomplete fixes"
    
    # Now test with proper fix
    good_fix = """
import json

def process_data(data):
    result = json.dumps(data)
    return result
"""
    
    result = await submit_fixed_code(
        original_code=code_with_import_error,
        fixed_code=good_fix,
        errors_fixed=["Added missing json import"],
        context=None
    )
    
    print("\n=== RESULT OF PROPER FIX ===")
    print(f"Status: {result['status']}")
    print(f"Total earned: {result['total_earned']}")
    print(f"Bonus messages: {result['bonus_messages']}")
    
    # Should succeed and possibly get import bonus
    assert result['status'] == 'SUCCESS', "Should accept complete fixes"
    assert result['total_earned'] > 0, "Should earn lollipops for import fix"
    
    # Check for import bonus
    if any("IMPORT" in msg for msg in result['bonus_messages']):
        print("\n🎉 Got import fix bonus!")
    
    print(f"\n🍭 Final lollipop count: {gamification.lollipops}")


if __name__ == "__main__":
    asyncio.run(test_import_error_triggers())