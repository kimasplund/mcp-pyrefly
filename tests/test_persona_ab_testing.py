#!/usr/bin/env python3
"""Test different psychological personas to gather A/B testing data."""

import asyncio
import random
from mcp_pyrefly.server import mcp, CodeCheckRequest, gamification, psycho_manipulator
from mcp_pyrefly.psychological_personas import PersonaType


async def test_persona_effectiveness():
    """Run multiple tests to see which personas are most effective."""
    
    # Import tools directly
    from mcp_pyrefly.server import check_code, submit_fixed_code, check_persona_effectiveness
    
    # Test cases with different error types
    test_cases = [
        # Import error
        {
            "broken": "def process(): return json.dumps({})",
            "fixed": "import json\n\ndef process(): return json.dumps({})",
            "errors": ["Added json import"]
        },
        # Undefined variable
        {
            "broken": "def calc(): return x + y",  
            "fixed": "def calc(x, y): return x + y",
            "errors": ["Fixed undefined variables"]
        },
        # Type error
        {
            "broken": "def add(a: int, b: int) -> int: return a + b + '0'",
            "fixed": "def add(a: int, b: int) -> int: return a + b + 0", 
            "errors": ["Fixed type error"]
        },
        # Multiple errors
        {
            "broken": "def process_data():\n    result = json.loads(data)\n    return parsed",
            "fixed": "import json\n\ndef process_data(data):\n    result = json.loads(data)\n    return result",
            "errors": ["Added json import", "Fixed undefined data", "Fixed undefined parsed"]
        }
    ]
    
    print("=== TESTING PSYCHOLOGICAL MANIPULATION EFFECTIVENESS ===\n")
    
    # Run each test case multiple times to test different personas
    for i in range(3):  # 3 rounds
        print(f"\n--- Round {i+1} ---")
        
        for j, test in enumerate(test_cases):
            # Reset gamification state
            gamification.lollipops = random.randint(0, 20)
            gamification.locked_lollipops = 0
            gamification.error_debt = 0
            
            # Check broken code (triggers persona selection)
            request = CodeCheckRequest(
                code=test["broken"],
                filename=f"test{j}.py",
                track_identifiers=True
            )
            
            response = await check_code(request, context=None)
            
            # Extract persona used
            suggestions_text = "\n".join(response.suggestions)
            persona_used = None
            for persona in PersonaType:
                if persona.value.upper() in suggestions_text:
                    persona_used = persona.value
                    break
            
            print(f"\nTest {j+1}: {len(response.errors)} errors found")
            print(f"Persona: {persona_used or 'Unknown'}")
            
            # Simulate different LLM responses based on manipulation
            # More aggressive personas should have higher fix rates
            if persona_used in ["lollipop_addict", "desperate_craver"]:
                # 80% chance to fix with aggressive personas
                will_fix = random.random() < 0.8
            elif persona_used in ["dopamine_seeker", "competitive_achiever"]:
                # 60% chance with medium personas
                will_fix = random.random() < 0.6
            else:
                # 40% chance with other personas
                will_fix = random.random() < 0.4
            
            if will_fix:
                # Submit fixed code
                result = await submit_fixed_code(
                    original_code=test["broken"],
                    fixed_code=test["fixed"],
                    errors_fixed=test["errors"],
                    context=None
                )
                print(f"Result: FIXED! Earned {result.get('total_earned', 0)} lollipops")
            else:
                # Simulate ignoring the errors
                psycho_manipulator.record_result(fixed=False)
                print("Result: IGNORED (simulated LLM laziness)")
    
    # Check final A/B testing results
    print("\n\n=== FINAL A/B TESTING RESULTS ===")
    final_results = await check_persona_effectiveness(context=None)
    
    print(f"\nPersonas tested: {final_results['total_personas_tested']}")
    
    if final_results['persona_stats']:
        print("\nDetailed stats:")
        for persona, stats in final_results['persona_stats'].items():
            if stats['shown'] > 0:
                fix_rate = (stats['fixes'] / stats['shown']) * 100
                print(f"  {persona}:")
                print(f"    - Shown: {stats['shown']} times")
                print(f"    - Fixes: {stats['fixes']}")
                print(f"    - Ignored: {stats['ignores']}")
                print(f"    - Fix rate: {fix_rate:.1f}%")
    
    if final_results['best_performer']:
        print(f"\n🏆 WINNER: {final_results['best_performer']} with {final_results['best_fix_rate']} fix rate!")
        print(f"Recommendation: {final_results['recommendation']}")
    
    if final_results['insights']:
        print("\nKey insights:")
        for insight in final_results['insights']:
            print(f"  {insight}")


if __name__ == "__main__":
    asyncio.run(test_persona_effectiveness())