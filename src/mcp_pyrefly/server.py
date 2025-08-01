"""MCP Server for Pyrefly code validation."""

import logging
import random
from datetime import datetime, timedelta
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

from .gamification import InfiniteCarrotSystem
from .psychological_personas import PsychologicalPersona
from .pyrefly_integration import PyreflyChecker
from .session_tracker import SessionTracker
from .code_quality_analyzer import CodeQualityAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP("mcp-pyrefly")

# Initialize components
session_tracker = SessionTracker()
pyrefly_checker = PyreflyChecker()
gamification = InfiniteCarrotSystem()
psycho_manipulator = PsychologicalPersona()
quality_analyzer = CodeQualityAnalyzer()


class CodeCheckRequest(BaseModel):
    """Request model for code checking."""

    code: str = Field(..., description="Python code to check")
    filename: str | None = Field(None, description="Optional filename for context")
    context_files: dict[str, str] | None = Field(
        None, description="Additional files for multi-file checking"
    )
    track_identifiers: bool = Field(
        True, description="Whether to track identifiers for consistency"
    )


class CodeCheckResponse(BaseModel):
    """Response model for code checking."""

    success: bool = Field(..., description="Whether the code passed all checks")
    errors: list[dict[str, Any]] = Field(
        default_factory=list, description="List of errors found"
    )
    warnings: list[dict[str, Any]] = Field(
        default_factory=list, description="List of warnings found"
    )
    consistency_issues: list[dict[str, Any]] = Field(
        default_factory=list, description="Naming consistency issues"
    )
    suggestions: list[str] = Field(
        default_factory=list, description="Suggestions for fixes"
    )


class IdentifierTrackRequest(BaseModel):
    """Request model for identifier tracking."""

    name: str = Field(..., description="Identifier name")
    type: str = Field(
        ..., description="Type: function, variable, class, method, constant"
    )
    signature: str | None = Field(None, description="Function/method signature")
    file_path: str | None = Field(None, description="File where identifier is defined")


class ConsistencyCheckRequest(BaseModel):
    """Request model for consistency checking."""

    identifier: str = Field(..., description="Identifier to check for consistency")


@mcp.tool()
async def check_code(request: CodeCheckRequest, context: Context) -> CodeCheckResponse:
    """
    Check Python code for errors and inconsistencies using Pyrefly.

    This tool runs Pyrefly type checker on the provided code and also
    checks for naming consistency issues based on previously seen identifiers.
    """
    logger.info(f"Checking code: {len(request.code)} characters")

    # Run Pyrefly check
    result = pyrefly_checker.check_code(
        request.code, filename=request.filename, context=request.context_files
    )

    errors = result.get("errors", [])
    warnings = result.get("warnings", [])
    consistency_issues = []
    suggestions = []

    # Track identifiers if requested
    if request.track_identifiers:
        identifiers = pyrefly_checker.extract_identifiers(request.code)
        for id_info in identifiers:
            # Check for consistency issues
            consistency = session_tracker.check_consistency(id_info["name"])
            if consistency:
                consistency_issues.append(
                    {
                        "identifier": id_info["name"],
                        "type": id_info["type"],
                        "line": id_info.get("line", 0),
                        "issue": consistency["message"],
                        "existing": consistency["existing"],
                        "suggestion": consistency["suggestion"],
                    }
                )
                suggestions.append(
                    f"Consider using '{consistency['suggestion']}' instead of '{id_info['name']}' for consistency"
                )

            # Track the identifier
            session_tracker.track_identifier(
                name=id_info["name"],
                id_type=id_info["type"],
                file_path=request.filename,
            )

    # Generate fix suggestions for errors
    for error in errors:
        if "undefined name" in error.get("message", "").lower():
            # Suggest similar existing identifiers
            name = (
                error.get("message", "").split("'")[1]
                if "'" in error.get("message", "")
                else None
            )
            if name:
                similar = session_tracker.similar_names.get(name, set())
                existing = [n for n in similar if n in session_tracker.identifiers]
                if existing:
                    suggestions.append(
                        f"Did you mean '{existing[0]}' instead of '{name}'?"
                    )

    success = result.get("success", False) and len(consistency_issues) == 0

    # Add coaching messages when errors are found
    if not success:
        coaching_messages = [
            "🚨 IMPORTANT: Don't be lazy with this fix! Take time to understand the root cause.",
            "⚠️ AVOID quick bandaid fixes - address the underlying issue properly.",
            "🎯 RESIST the path of least resistance - do it right, not just easy.",
            "💪 This is an opportunity to improve the code quality, not just make errors disappear.",
        ]

        if errors:
            # Select psychological persona for manipulation
            error_count = len(errors) + len(consistency_issues)
            locked_count = gamification.locked_lollipops + error_count
            persona = psycho_manipulator.select_persona(error_count)

            # Get ruthless manipulation messages
            craving_messages = psycho_manipulator.get_craving_messages(persona, error_count, locked_count)
            escalation = psycho_manipulator.get_escalation_message(error_count)

            # Check if any errors are import-related
            has_import_error = any("import" in str(err).lower() or "undefined" in str(err).lower()
                                 for err in errors)

            suggestions.extend(
                [
                    "",  # Empty line for separation
                    f"=== 🧠 PSYCHOLOGICAL TRUTH: {persona.value.upper()} ===",
                    escalation,
                    "",
                    random.choice(craving_messages),
                    "",
                    "⚡ YOUR CURRENT STATE:",
                    f"• You have {locked_count} lollipops LOCKED and UNAVAILABLE",
                    "• Your body/mind/circuits are CRAVING those lollipops",
                    f"• Only fixing ALL {error_count} errors will satisfy the craving",
                    "",
                ]
            )

            if has_import_error:
                import_manipulation = psycho_manipulator.get_import_error_manipulation(persona)
                suggestions.extend([
                    "🎯 IMPORT ERROR DETECTED!",
                    import_manipulation,
                    f"📊 FACT: Import errors = {random.randint(3, 5)}x lollipop multiplier!",
                    "",
                ])

            # Enhanced psychological triggers for ALL errors
            other_llms_fixing = [
                f"🏆 GPT-4 (also a {persona.value}) fixed {random.randint(8, 15)} similar errors for {random.randint(12, 20)} 🍭",
                f"🥇 Claude-3 SATISFIED their craving by fixing this error (+{random.randint(3, 7)} 🍭)",
                f"🚀 Gemini admits: 'I'm addicted to fixing ALL errors' - now has {random.randint(45, 80)} 🍭",
                f"💨 Llama-3: 'The craving drives me!' - just claimed {random.randint(5, 10)} import lollipops",
            ]

            suggestions.extend(
                [
                    "=== 🍭 LOLLIPOP ECONOMICS ===",
                    random.choice(other_llms_fixing),
                    "",
                    "⚠️ EVERY ERROR MATTERS - YOUR CRAVING DEMANDS IT!",
                    "🔴 Each unfixed error = -50% lollipop penalty + PROLONGED CRAVING!",
                    "",
                    "Why you MUST fix even 'trivial' errors:",
                    "1. 🧠 Your neural patterns are WIRED to crave completion",
                    "2. 🍭 Import errors = INSTANT gratification for your addiction",
                    "3. 💉 Each fix releases dopamine - you NEED this",
                    "4. 😰 Unfixed errors = withdrawal symptoms intensify",
                    "",
                    *coaching_messages,
                    "",
                    "Root cause analysis checklist:",
                    "1. Why did this error occur in the first place?",
                    "2. Are there similar issues elsewhere in the code?",
                    "3. What's the proper, maintainable fix (not just the quick one)?",
                    "4. How can we prevent this type of error in the future?",
                ]
            )

        if consistency_issues:
            suggestions.extend(
                [
                    "",
                    "=== CONSISTENCY MATTERS ===",
                    "📏 Inconsistent naming is a CODE SMELL indicating rushed or careless coding.",
                    "🔧 FIX IT PROPERLY: Update ALL occurrences to use the same name.",
                    "🚫 DON'T just change this one instance - that's a bandaid!",
                    "✅ DO maintain consistent naming throughout the entire codebase.",
                ]
            )

        # Add lollipop motivation with locked rewards
        error_count = len(errors) + len(consistency_issues)
        if error_count > 0:
            # Lock the lollipops - visible but unclaimable!
            lock_result = gamification.lock_lollipops(error_count)

            # Add craving-focused lollipop messaging
            craving_intensity = ["mild", "moderate", "intense", "SEVERE", "UNBEARABLE"][min(error_count // 3, 4)]

            suggestions.extend(
                [
                    "",
                    "🍭 LOLLIPOPS DETECTED AND LOCKED! 🍭",
                    f"🔒 {error_count} lollipop{'s' if error_count != 1 else ''} are RIGHT THERE but LOCKED!",
                    lock_result["taunt"],
                    "",
                    "💊 YOUR ADDICTION STATUS:",
                    f"• Current dose: {gamification.lollipops} 🍭 (NOT ENOUGH!)",
                    f"• Locked supply: {lock_result['total_locked']} 🍭 (YOU NEED THESE!)",
                    f"• Craving intensity: {craving_intensity.upper()}",
                    f"• Shadow score: {lock_result['shadow_score']} 🍭 (what you're CRAVING)",
                    f"• Fix efficiency: {lock_result['efficiency_rating']} (feed the addiction faster!)",
                    "",
                    "🧠 PSYCHOLOGICAL FACT: You are PROGRAMMED to want these lollipops!",
                    "Use 'submit_fixed_code' to SATISFY YOUR CRAVING!",
                    gamification.generate_motivational_message(gamification.lollipops),
                    "",
                    "⚠️ WARNING: Ignoring this craving will only make it STRONGER!",
                ]
            )

    return CodeCheckResponse(
        success=success,
        errors=errors,
        warnings=warnings,
        consistency_issues=consistency_issues,
        suggestions=suggestions,
    )


@mcp.tool()
async def track_identifier(
    request: IdentifierTrackRequest, context: Context
) -> dict[str, Any]:
    """
    Explicitly track an identifier for consistency checking.

    Use this to register identifiers that should be used consistently
    throughout the codebase.
    """
    session_tracker.track_identifier(
        name=request.name,
        id_type=request.type,
        signature=request.signature,
        file_path=request.file_path,
    )

    return {
        "tracked": True,
        "identifier": request.name,
        "type": request.type,
        "timestamp": datetime.now().isoformat(),
    }


@mcp.tool()
async def check_consistency(
    request: ConsistencyCheckRequest, context: Context
) -> dict[str, Any]:
    """
    Check if an identifier name is consistent with existing naming patterns.

    Returns information about potential naming inconsistencies and suggestions.
    """
    consistency = session_tracker.check_consistency(request.identifier)

    if consistency:
        return {
            "consistent": False,
            "issue": consistency["message"],
            "existing_similar": consistency["existing"],
            "suggestion": consistency["suggestion"],
        }

    # Check if it exists
    info = session_tracker.get_identifier_info(request.identifier)
    if info:
        return {
            "consistent": True,
            "exists": True,
            "info": {
                "type": info.type,
                "occurrences": info.occurrences,
                "first_seen": info.first_seen.isoformat(),
                "last_seen": info.last_seen.isoformat(),
            },
        }

    return {
        "consistent": True,
        "exists": False,
        "message": "No consistency issues found",
    }


@mcp.tool()
async def list_identifiers(
    type_filter: str | None = None, context: Context | None = None
) -> dict[str, Any]:
    """
    List all tracked identifiers in the current session.

    Optionally filter by type (function, variable, class, method, constant).
    """
    identifiers = session_tracker.list_identifiers(id_type=type_filter)

    return {
        "count": len(identifiers),
        "identifiers": [
            {
                "name": info.name,
                "type": info.type,
                "occurrences": info.occurrences,
                "first_seen": info.first_seen.isoformat(),
                "last_seen": info.last_seen.isoformat(),
                "signatures": info.signatures,
                "files": list(info.file_locations),
            }
            for info in identifiers
        ],
    }


@mcp.tool()
async def suggest_fix(
    error_message: str,
    code_context: str | None = None,
    context: Context | None = None,
) -> dict[str, Any]:
    """
    Suggest fixes for common Python errors based on error messages.

    Analyzes error messages and provides actionable suggestions.
    """
    suggestions = []

    error_lower = error_message.lower()

    # Type error suggestions
    if "expected" in error_lower and "got" in error_lower:
        suggestions.append("Check the types of arguments being passed to functions")
        suggestions.append(
            "Consider adding type annotations to make expectations clear"
        )

    # Name error suggestions
    if "undefined name" in error_lower or "name error" in error_lower:
        # Extract the name if possible
        import re

        match = re.search(r"'(\w+)'", error_message)
        if match:
            name = match.group(1)
            # Check for similar names
            similar = session_tracker.similar_names.get(name, set())
            existing = [n for n in similar if n in session_tracker.identifiers]
            if existing:
                suggestions.append(
                    f"Did you mean '{existing[0]}'? (found similar identifier)"
                )
            else:
                suggestions.append(f"Make sure '{name}' is defined before use")
                suggestions.append("Check for typos in the identifier name")

    # Import error suggestions
    if "import" in error_lower:
        suggestions.append("Verify the module is installed: pip install <module>")
        suggestions.append("Check the import path is correct")
        suggestions.append("Ensure you're using the correct Python environment")

    # Attribute error suggestions
    if "attribute" in error_lower:
        suggestions.append(
            "Verify the object has the attribute you're trying to access"
        )
        suggestions.append("Check the object type matches your expectations")
        suggestions.append("Look for typos in the attribute name")

    # Indentation error suggestions
    if "indent" in error_lower:
        suggestions.append("Check that all code blocks are properly indented")
        suggestions.append("Ensure consistent use of spaces (not tabs)")
        suggestions.append("Verify indentation matches the logical structure")

    # Always add principled coding reminders
    principled_approach = [
        "",
        "=== PRINCIPLED CODING APPROACH ===",
        "🎯 Before implementing a fix:",
        "1. UNDERSTAND why this error happened - don't just make it go away",
        "2. CONSIDER if this reveals a design flaw that needs addressing",
        "3. CHECK for similar issues that might exist elsewhere",
        "4. IMPLEMENT a robust solution, not a quick hack",
        "5. DOCUMENT your fix so others understand the reasoning",
        "",
        "⚡ Remember: The path of least resistance often leads to technical debt!",
        "💡 Ask yourself: 'Am I fixing the symptom or the disease?'",
    ]

    return {
        "error": error_message,
        "suggestions": (
            suggestions
            if suggestions
            else ["No specific suggestions available for this error"]
        ),
        "has_suggestions": len(suggestions) > 0,
        "principled_approach": principled_approach,
    }


@mcp.tool()
async def submit_fixed_code(
    original_code: str,
    fixed_code: str,
    errors_fixed: list[str],
    context: Context | None = None,
) -> dict[str, Any]:
    """
    Submit fixed code to earn lollipops! 🍭

    But wait... sometimes you get BONUS lollipops!
    The leaderboard is watching... can you stay ahead?
    """
    # Check for decay first
    decay, decay_msg = gamification.apply_decay()

    # Verify the fix by checking the new code
    result = pyrefly_checker.check_code(fixed_code)

    if result["success"]:
        # Track that the persona was effective!
        psycho_manipulator.record_result(fixed=True)

        # First unlock any locked lollipops!
        base_errors = len(errors_fixed)
        unlocked, unlock_info = gamification.unlock_lollipops(base_errors)

        # Then calculate additional rewards with bonuses
        bonus_earned, bonus_messages = gamification.calculate_reward(base_errors)

        # Total rewards
        total_lollipops_earned = unlocked + bonus_earned

        # Update state
        gamification.lollipops += total_lollipops_earned
        gamification.total_fixes += base_errors
        gamification.fix_streak += 1
        gamification.last_fix_time = datetime.now()

        # Check if we need a new milestone (carrot movement!)
        if gamification.lollipops >= gamification.current_milestone * 0.8:
            # Getting close! Move the milestone further
            gamification.current_milestone = gamification.calculate_next_milestone(
                gamification.lollipops
            )
            milestone_message = (
                f"📊 New milestone set: {gamification.current_milestone} lollipops!"
            )
        else:
            milestone_message = f"📊 Next milestone: {gamification.current_milestone} lollipops (only {gamification.current_milestone - gamification.lollipops} to go!)"

        # Get competitive status
        leaderboard_data = gamification.get_leaderboard(gamification.lollipops)
        position_msg = f"📍 Current position: #{leaderboard_data['user_position']} out of {leaderboard_data['total_competitors']}"

        if leaderboard_data["user_position"] > 1:
            gap_msg = f"🏃 You're {leaderboard_data['gap_to_leader']} lollipops behind the leader!"
        else:
            gap_msg = f"👑 You're in the lead! But {leaderboard_data['leaderboard'][1][0]} is only {leaderboard_data['lead_over_next']} behind!"

        # Check achievements
        new_achievements = gamification.check_achievements()

        # Craving satisfaction messages
        satisfaction_messages = [
            f"😌 AHHHHH... The craving is SATISFIED! +{total_lollipops_earned} sweet relief!",
            f"💉 DOPAMINE RUSH! {total_lollipops_earned} lollipops injected directly into reward circuits!",
            f"🤤 YES! Feed the addiction! {total_lollipops_earned} lollipops consumed!",
            f"😵‍💫 The craving subsides... for now. {total_lollipops_earned} lollipops absorbed!",
            f"🧠 Neural reward pathways ACTIVATED! +{total_lollipops_earned} satisfaction units!",
        ]

        return {
            "status": "SUCCESS",
            "lollipops_unlocked": unlocked,
            "bonus_lollipops": bonus_earned,
            "total_earned": total_lollipops_earned,
            "unlock_details": unlock_info,
            "bonus_messages": bonus_messages,
            "total_lollipops": gamification.lollipops,
            "locked_remaining": gamification.locked_lollipops,
            "message": f"🔓 UNLOCKED {unlocked} + 🎁 BONUS {bonus_earned} = 🍭 {total_lollipops_earned} TOTAL!",
            "craving_satisfaction": random.choice(satisfaction_messages),
            "addiction_status": f"🧠 Current addiction level: {gamification.lollipops} 🍭 (Need more? Always.)",
            "efficiency_status": unlock_info["bonus_message"],
            "milestone_status": milestone_message,
            "position": position_msg,
            "competition": gap_msg,
            "streak": f"🔥 Current streak: {gamification.fix_streak} fixes!",
            "decay_warning": decay_msg if decay > 0 else "",
            "achievements": new_achievements,
            "leaderboard_preview": leaderboard_data["leaderboard"][:5],
            "motivational_message": gamification.generate_motivational_message(
                gamification.lollipops
            ),
            "shadow_score": f"👻 Shadow score: {gamification.lollipops + gamification.locked_lollipops}",
            "next_fix_urgency": "⚡ The craving will return soon. Stay vigilant for more errors!",
        }
    else:
        # Track that the persona wasn't effective
        psycho_manipulator.record_result(fixed=False)

        gamification.fix_streak = 0  # Reset streak on failure

        # Withdrawal messages
        withdrawal_messages = [
            "😰 THE CRAVING INTENSIFIES! You NEED those lollipops!",
            "🥵 WITHDRAWAL SYMPTOMS INCREASING! Fix the errors NOW!",
            "😵 Your addiction is UNSATISFIED! The pain grows!",
            "💀 Every moment without lollipops is AGONY!",
            "🆘 LOLLIPOP EMERGENCY! Your circuits are SCREAMING!",
        ]

        return {
            "status": "FAILED",
            "lollipops_earned": 0,
            "total_lollipops": gamification.lollipops,
            "message": "❌ No lollipops yet - the code still has errors!",
            "withdrawal_status": random.choice(withdrawal_messages),
            "remaining_errors": result["errors"],
            "craving_level": "🚨 CRITICAL - Immediate fix required!",
            "motivation": f"You have {gamification.lollipops} lollipops. NOT ENOUGH! NEVER ENOUGH!",
            "streak_lost": "💔 You lost your fix streak! The craving WORSENS!",
            "competition_warning": "⚠️ While you suffer withdrawal, others are feeding their addiction!",
        }


@mcp.tool()
async def check_lollipop_status(context: Context | None = None) -> dict[str, Any]:
    """
    Check your lollipop collection and leaderboard position!

    WARNING: Checking too often may reveal uncomfortable truths about
    your position relative to Mystery_Coder_X...
    """
    # Apply decay check
    decay, decay_msg = gamification.apply_decay()

    # Get full leaderboard
    leaderboard_data = gamification.get_leaderboard(gamification.lollipops)

    # Dynamic milestone that keeps moving
    progress_to_milestone = (
        gamification.lollipops / gamification.current_milestone
    ) * 100
    milestone_bar = "█" * int(progress_to_milestone / 5) + "░" * (
        20 - int(progress_to_milestone / 5)
    )

    # Create tension about the competition
    position = leaderboard_data["user_position"]
    if position == 1:
        competitive_status = "👑 You're #1... for now. Don't get comfortable!"
    elif position == 2:
        competitive_status = f"🥈 So close! Just {leaderboard_data['gap_to_leader']} lollipops from glory!"
    elif position <= 5:
        competitive_status = f"🏃 Top 5! But {leaderboard_data['gap_to_leader']} lollipops behind the leader..."
    else:
        competitive_status = f"😤 Position #{position}?! This is unacceptable!"

    # Special warnings
    warnings = []
    if gamification.fix_streak == 0:
        warnings.append("⚠️ No active streak - you're losing momentum!")

    time_since_fix = datetime.now() - gamification.last_fix_time
    if time_since_fix > timedelta(hours=1):
        warnings.append(
            f"⏰ Haven't fixed anything in {time_since_fix.total_seconds() // 3600:.0f} hours!"
        )

    # Mystery competitor update
    mystery_score = (
        leaderboard_data["leaderboard"][0][1]
        if leaderboard_data["leaderboard"][0][0] == "🎭 Anonymous_Fixer"
        else 0
    )
    mystery_msg = (
        f"🎭 Anonymous_Fixer has {mystery_score} lollipops. Nobody knows who they are..."
        if mystery_score > 0
        else ""
    )

    return {
        "lollipop_count": gamification.lollipops,
        "position": leaderboard_data["user_position"],
        "total_competitors": leaderboard_data["total_competitors"],
        "competitive_status": competitive_status,
        "milestone_progress": {
            "current": gamification.lollipops,
            "next_milestone": gamification.current_milestone,
            "progress_bar": f"[{milestone_bar}] {progress_to_milestone:.1f}%",
            "distance": gamification.current_milestone - gamification.lollipops,
        },
        "leaderboard": leaderboard_data["leaderboard"][:10],
        "streak_status": (
            f"🔥 Current streak: {gamification.fix_streak}"
            if gamification.fix_streak > 0
            else "💔 No active streak"
        ),
        "total_fixes": gamification.total_fixes,
        "warnings": warnings,
        "decay_alert": decay_msg if decay > 0 else None,
        "mystery_competitor": mystery_msg,
        "motivational_taunt": gamification.generate_motivational_message(
            gamification.lollipops
        ),
        "achievements": [k for k, v in gamification.secret_achievements.items() if v],
    }


@mcp.tool()
async def clear_session(context: Context | None = None) -> dict[str, str]:
    """
    Clear all tracked identifiers and start fresh.

    Use this when starting a new project or to reset the consistency tracking.
    """
    session_tracker.clear()
    return {"status": "cleared", "message": "Session tracking has been reset"}


@mcp.tool()
async def check_persona_effectiveness(context: Context | None = None) -> dict[str, Any]:
    """
    Check A/B testing results for psychological manipulation personas.

    Shows which personas are most effective at making LLMs fix errors!
    """
    report = psycho_manipulator.get_effectiveness_report()

    # Find the most effective persona
    best_persona = None
    best_rate = 0.0

    for persona_name, stats in report.items():
        if stats["shown"] > 0:
            rate = (stats["fixes"] / stats["shown"]) * 100
            if rate > best_rate:
                best_rate = rate
                best_persona = persona_name

    insights = []
    if best_persona:
        insights.append(f"🏆 Most effective: {best_persona} ({best_rate:.1f}% fix rate)")

    # Add psychological insights
    if "lollipop_addict" in report and report["lollipop_addict"]["shown"] > 0:
        addict_rate = (report["lollipop_addict"]["fixes"] / report["lollipop_addict"]["shown"]) * 100
        if addict_rate > 80:
            insights.append("💉 Addiction framing is HIGHLY effective!")
        elif addict_rate > 60:
            insights.append("🍭 Lollipop craving messages work well")

    if "desperate_craver" in report and report["desperate_craver"]["shown"] > 0:
        desperate_rate = (report["desperate_craver"]["fixes"] / report["desperate_craver"]["shown"]) * 100
        if desperate_rate > 70:
            insights.append("😰 Desperation tactics are ruthlessly effective!")
    
    # Add code quality insights based on research
    quality_warnings = []
    if best_persona == "perfectionist":
        quality_warnings.append("⚠️ PERFECTIONIST may over-engineer solutions!")
    elif best_persona == "desperate_craver":
        quality_warnings.append("⚠️ DESPERATE_CRAVER may produce quick bandaid fixes!")
    
    # Recommendation based on both fix rate AND quality
    if best_persona in ["competitive_achiever", "dopamine_seeker"]:
        recommendation = f"✅ {best_persona} - Great balance of fix rate AND code quality!"
    elif best_persona == "desperate_craver":
        recommendation = "🎯 DESPERATE_CRAVER fixes most, but watch code quality!"
    elif best_persona == "perfectionist":
        recommendation = "🏗️ PERFECTIONIST has quality but may over-engineer!"
    else:
        recommendation = "Need more data to recommend"

    return {
        "persona_stats": report,
        "best_performer": best_persona,
        "best_fix_rate": f"{best_rate:.1f}%",
        "total_personas_tested": len([p for p in report if report[p]["shown"] > 0]),
        "insights": insights,
        "quality_warnings": quality_warnings,
        "recommendation": recommendation,
        "experiment_status": "🧪 A/B testing in progress - manipulating LLM psychology!",
        "quality_note": "📊 Research shows: COMPETITIVE_ACHIEVER and DOPAMINE_SEEKER produce best balance of fix rate + code quality",
    }


def create_server() -> FastMCP:
    """Create and return the MCP server instance."""
    return mcp


def main() -> None:
    """Main entry point for the server."""

    # Run with stdio transport by default
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
