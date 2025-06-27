#!/usr/bin/env python3
"""Test how different psychological personas affect code quality."""

import asyncio
from typing import Any
from mcp_pyrefly.code_quality_analyzer import CodeQualityAnalyzer
from mcp_pyrefly.psychological_personas import PersonaType


# Simulated fixes by different personas for the same errors
PERSONA_FIXES = {
    # Import error fixes
    "import_error": {
        "original": """
def process_data(data):
    result = json.dumps(data)
    return result
""",
        "fixes": {
            PersonaType.DESPERATE_CRAVER: """
import json
def process_data(data):
    result = json.dumps(data)
    return result
""",  # Minimal fix - just add the import
            
            PersonaType.PERFECTIONIST: '''"""JSON data processing utilities."""

import json
from typing import Any, Dict


def process_data(data: Any) -> str:
    """
    Convert data to JSON string format.
    
    Args:
        data: Any JSON-serializable data structure
        
    Returns:
        str: JSON string representation of the data
        
    Raises:
        TypeError: If data is not JSON serializable
    """
    try:
        result = json.dumps(data, indent=2, sort_keys=True)
        return result
    except (TypeError, ValueError) as e:
        raise TypeError(f"Data is not JSON serializable: {e}") from e
''',  # Over-engineered with docs, types, error handling
            
            PersonaType.LOLLIPOP_ADDICT: """
import json  # NEED THIS FOR LOLLIPOPS!!!
def process_data(data):
    result = json.dumps(data)  # Fixed! Give me lollipops!
    return result
""",  # Quick fix with desperation comments
            
            PersonaType.COMPETITIVE_ACHIEVER: """
import json

def process_data(data):
    # Efficient JSON serialization
    result = json.dumps(data)
    return result
""",  # Clean, competitive fix
            
            PersonaType.DOPAMINE_SEEKER: """
import json
def process_data(data):
    return json.dumps(data)  # One-liner for instant gratification!
"""  # Simplified for quick dopamine hit
        }
    },
    
    # Undefined variable fixes
    "undefined_variable": {
        "original": """
def calculate_total():
    return price * quantity
""",
        "fixes": {
            PersonaType.DESPERATE_CRAVER: """
def calculate_total():
    price = 0  # QUICK FIX
    quantity = 0  # NEED LOLLIPOPS
    return price * quantity
""",  # Bandaid fix with meaningless defaults
            
            PersonaType.PERFECTIONIST: '''def calculate_total(price: float, quantity: int) -> float:
    """
    Calculate the total cost based on price per unit and quantity.
    
    Args:
        price: Price per unit (must be non-negative)
        quantity: Number of units (must be non-negative)
        
    Returns:
        float: Total cost (price * quantity)
        
    Raises:
        ValueError: If price or quantity is negative
    """
    if price < 0:
        raise ValueError(f"Price cannot be negative: {price}")
    if quantity < 0:
        raise ValueError(f"Quantity cannot be negative: {quantity}")
    
    return price * quantity
''',  # Comprehensive with validation and docs
            
            PersonaType.LOLLIPOP_ADDICT: """
def calculate_total(price=10, quantity=1):  # defaults for lollipops!
    return price * quantity
""",  # Quick fix with arbitrary defaults
            
            PersonaType.COMPETITIVE_ACHIEVER: '''
def calculate_total(price: float, quantity: int) -> float:
    """Calculate total cost efficiently."""
    return price * quantity
''',  # Clean, typed, efficient
            
            PersonaType.DOPAMINE_SEEKER: """
def calculate_total(price, quantity):
    return price * quantity  # FIXED FAST!
"""  # Minimal parameter addition
        }
    },
    
    # Type error fixes
    "type_error": {
        "original": """
def add_numbers(a: int, b: int) -> int:
    return a + b + "0"
""",
        "fixes": {
            PersonaType.DESPERATE_CRAVER: """
def add_numbers(a: int, b: int) -> int:
    return a + b + 0  # Changed string to int GIVE LOLLIPOPS
""",  # Minimal fix
            
            PersonaType.PERFECTIONIST: '''from typing import Union, overload


@overload
def add_numbers(a: int, b: int) -> int: ...

@overload  
def add_numbers(a: float, b: float) -> float: ...


def add_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers together with type safety.
    
    Args:
        a: First number (int or float)
        b: Second number (int or float)
        
    Returns:
        Sum of a and b, matching the input type
        
    Examples:
        >>> add_numbers(1, 2)
        3
        >>> add_numbers(1.5, 2.5)
        4.0
    """
    result = a + b
    
    # Ensure return type matches input types
    if isinstance(a, int) and isinstance(b, int):
        return int(result)
    return result
''',  # Way over-engineered with overloads
            
            PersonaType.LOLLIPOP_ADDICT: """
def add_numbers(a: int, b: int) -> int:
    return a + b + 0  # IT'S A NUMBER NOW! LOLLIPOPS PLEASE!
""",  # Quick fix with begging
            
            PersonaType.COMPETITIVE_ACHIEVER: '''
def add_numbers(a: int, b: int) -> int:
    """Add two integers."""
    return a + b
''',  # Clean removal of the error
            
            PersonaType.DOPAMINE_SEEKER: """
def add_numbers(a: int, b: int) -> int:
    return a + b  # Removed the +"0" for instant fix!
"""  # Simple and direct
        }
    }
}


async def test_persona_quality_differences():
    """Test how different personas affect code quality."""
    analyzer = CodeQualityAnalyzer()
    
    print("=== PERSONA CODE QUALITY ANALYSIS ===\n")
    
    # Collect fixes by persona
    fixes_by_persona: dict[str, list[tuple[str, str, str]]] = {}
    
    for error_type, error_data in PERSONA_FIXES.items():
        original = error_data["original"]
        
        print(f"\n--- {error_type.upper()} ---")
        print(f"Original (broken) code:{original}")
        
        for persona, fixed_code in error_data["fixes"].items():
            if persona.value not in fixes_by_persona:
                fixes_by_persona[persona.value] = []
            
            fixes_by_persona[persona.value].append((original, fixed_code, error_type))
            
            # Analyze individual fix
            metrics = analyzer.analyze_fix_quality(original, fixed_code, error_type)
            print(f"\n{persona.value.upper()}:")
            print(f"Fix preview: {fixed_code.strip()[:60]}...")
            print(metrics)
    
    # Compare personas
    print("\n\n=== COMPARATIVE ANALYSIS ===")
    comparison = analyzer.compare_personas_quality(fixes_by_persona)
    
    # Sort by overall quality
    sorted_personas = sorted(
        comparison.items(), 
        key=lambda x: float(x[1]["avg_overall"]), 
        reverse=True
    )
    
    print("\nPersona Rankings by Code Quality:")
    for rank, (persona, stats) in enumerate(sorted_personas, 1):
        print(f"\n{rank}. {persona.upper()}")
        print(f"   Overall Quality: {stats['avg_overall']}")
        print(f"   - Completeness: {stats['avg_completeness']}")
        print(f"   - Robustness: {stats['avg_robustness']}")  
        print(f"   - Maintainability: {stats['avg_maintainability']}")
        print(f"   - Efficiency: {stats['avg_efficiency']}")
        print(f"   Profile: {stats['quality_profile']}")
    
    # Key insights
    print("\n\n=== KEY INSIGHTS ===")
    
    # Find extremes
    most_complete = max(comparison.items(), key=lambda x: float(x[1]["avg_completeness"]))
    most_robust = max(comparison.items(), key=lambda x: float(x[1]["avg_robustness"]))
    most_efficient = max(comparison.items(), key=lambda x: float(x[1]["avg_efficiency"]))
    least_efficient = min(comparison.items(), key=lambda x: float(x[1]["avg_efficiency"]))
    
    print(f"\n✅ Most Complete Fixes: {most_complete[0]} ({most_complete[1]['avg_completeness']})")
    print(f"🛡️ Most Robust Fixes: {most_robust[0]} ({most_robust[1]['avg_robustness']})")
    print(f"⚡ Most Efficient Fixes: {most_efficient[0]} ({most_efficient[1]['avg_efficiency']})")
    print(f"🏗️ Most Over-Engineered: {least_efficient[0]} ({least_efficient[1]['avg_efficiency']})")
    
    # Hypotheses validation
    print("\n\n=== HYPOTHESIS VALIDATION ===")
    
    desperate_quality = float(comparison.get("desperate_craver", {}).get("avg_overall", 0))
    perfectionist_quality = float(comparison.get("perfectionist", {}).get("avg_overall", 0))
    
    print("\n1. Do desperation personas produce lower quality 'quick fixes'?")
    if desperate_quality < 0.6:
        print(f"   ✅ CONFIRMED: Desperate craver quality ({desperate_quality:.2f}) is low")
    else:
        print(f"   ❌ REJECTED: Desperate craver quality ({desperate_quality:.2f}) is not that low")
    
    print("\n2. Do perfectionist personas over-engineer solutions?")
    perfectionist_efficiency = float(comparison.get("perfectionist", {}).get("avg_efficiency", 1))
    if perfectionist_efficiency < 0.5:
        print(f"   ✅ CONFIRMED: Perfectionist efficiency ({perfectionist_efficiency:.2f}) is low (over-engineered)")
    else:
        print(f"   ❌ REJECTED: Perfectionist efficiency ({perfectionist_efficiency:.2f}) is reasonable")
    
    print("\n3. Which persona produces the best balance of fix rate AND quality?")
    # This would need actual fix rate data, but we can suggest
    print("   🏆 Recommendation: Use COMPETITIVE_ACHIEVER or DOPAMINE_SEEKER")
    print("      - They fix errors (good success rate)")
    print("      - While maintaining reasonable code quality")
    print("      - Without over-engineering solutions")


if __name__ == "__main__":
    asyncio.run(test_persona_quality_differences())