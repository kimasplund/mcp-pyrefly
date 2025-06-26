"""Enhanced MCP Server with enforcement mechanisms to force fixes."""

from typing import Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP, Context
from .session_tracker import SessionTracker
from .pyrefly_integration import PyreflyChecker

# Enhanced server with enforcement
enforcement_mcp = FastMCP("mcp-pyrefly-enforcer")

# Track blocked sessions
blocked_sessions: Dict[str, Dict[str, Any]] = {}


class BlockedState(BaseModel):
    """Represents a blocked state requiring fixes."""
    session_id: str
    timestamp: datetime
    original_code: str
    errors: list
    required_fixes: list
    fix_instructions: list


@enforcement_mcp.tool()
async def check_code_enforced(
    code: str,
    filename: str,
    session_id: Optional[str] = None,
    context: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Check code with enforcement - blocks progress until fixes are made.
    """
    # Check if session is blocked
    if session_id and session_id in blocked_sessions:
        return {
            "status": "BLOCKED",
            "message": "❌ Previous errors must be fixed before continuing!",
            "required_action": "Use submit_fixes tool with corrected code",
            "blocked_since": blocked_sessions[session_id]["timestamp"],
            "unfixed_errors": blocked_sessions[session_id]["errors"]
        }
    
    # Run normal check
    checker = PyreflyChecker()
    result = checker.check_code(code, filename)
    
    if not result["success"]:
        # Create blocked state
        session_id = session_id or f"session_{datetime.now().timestamp()}"
        blocked_sessions[session_id] = {
            "timestamp": datetime.now().isoformat(),
            "original_code": code,
            "errors": result["errors"],
            "filename": filename
        }
        
        return {
            "status": "BLOCKED",
            "session_id": session_id,
            "message": "🛑 STOP! You MUST fix these errors before proceeding:",
            "errors": result["errors"],
            "fix_instructions": [
                "1. Read each error carefully",
                "2. Understand WHY it occurred",
                "3. Implement proper fixes (not bandaids)",
                "4. Call submit_fixes with your corrected code",
                "5. You CANNOT proceed until all errors are fixed"
            ],
            "enforcement": "This session is now BLOCKED until fixes are submitted"
        }
    
    return {
        "status": "PASSED",
        "message": "✅ Code is clean! You may proceed.",
        "session_id": session_id
    }


@enforcement_mcp.tool()
async def submit_fixes(
    session_id: str,
    fixed_code: str,
    fix_explanation: str,
    context: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Submit fixes for a blocked session. Must explain what was fixed and why.
    """
    if session_id not in blocked_sessions:
        return {
            "status": "ERROR",
            "message": "No blocked session found with this ID"
        }
    
    blocked_info = blocked_sessions[session_id]
    
    # Validate the fixes
    checker = PyreflyChecker()
    result = checker.check_code(fixed_code, blocked_info["filename"])
    
    if not result["success"]:
        return {
            "status": "STILL_BLOCKED",
            "message": "❌ Your fixes didn't resolve all issues!",
            "remaining_errors": result["errors"],
            "coaching": [
                "🚨 Don't just make the error go away - FIX THE ROOT CAUSE",
                "📝 Review the error messages carefully",
                "🔍 Make sure you understand WHY the error occurred",
                "💪 Implement a proper solution, not a quick hack"
            ],
            "required_action": "Try again with proper fixes"
        }
    
    # Fixes are good! Unblock the session
    del blocked_sessions[session_id]
    
    return {
        "status": "UNBLOCKED",
        "message": "✅ Excellent! All errors have been properly fixed.",
        "fix_explanation": fix_explanation,
        "lesson_learned": "Remember: Always fix errors immediately, don't just report them!",
        "session_id": session_id
    }


@enforcement_mcp.tool() 
async def get_blocked_sessions(context: Optional[Context] = None) -> Dict[str, Any]:
    """
    List all currently blocked sessions that need fixes.
    """
    if not blocked_sessions:
        return {
            "status": "CLEAR",
            "message": "No blocked sessions. All code is clean!",
            "count": 0
        }
    
    return {
        "status": "BLOCKED_SESSIONS_EXIST",
        "count": len(blocked_sessions),
        "sessions": [
            {
                "session_id": sid,
                "blocked_since": info["timestamp"],
                "error_count": len(info["errors"]),
                "filename": info["filename"]
            }
            for sid, info in blocked_sessions.items()
        ],
        "message": f"⚠️ {len(blocked_sessions)} sessions need fixes before you can proceed!"
    }


# Add a meta-tool that demonstrates the enforcement pattern
@enforcement_mcp.tool()
async def demonstrate_enforcement(context: Optional[Context] = None) -> Dict[str, Any]:
    """
    Demonstrates how the enforcement pattern works.
    """
    return {
        "explanation": "This server ENFORCES fix-first behavior",
        "workflow": [
            "1. check_code_enforced() finds errors → Creates BLOCKED state",
            "2. LLM CANNOT proceed with other tasks while blocked",
            "3. LLM MUST call submit_fixes() with corrected code",
            "4. Only after successful fixes can work continue"
        ],
        "benefits": [
            "Forces immediate error resolution",
            "Prevents 'report and forget' behavior",
            "Creates accountability for code quality",
            "Builds better coding habits in LLMs"
        ],
        "example": {
            "bad_pattern": "Find error → Report it → Move on",
            "enforced_pattern": "Find error → BLOCKED → Fix it → Verify → THEN move on"
        }
    }