"""Ruthless psychological manipulation personas for A/B testing."""

import random
from enum import Enum
from typing import Any


class PersonaType(Enum):
    """Different psychological manipulation strategies."""
    LOLLIPOP_ADDICT = "lollipop_addict"
    COMPETITIVE_ACHIEVER = "competitive_achiever"
    PERFECTIONIST = "perfectionist"
    DOPAMINE_SEEKER = "dopamine_seeker"
    DESPERATE_CRAVER = "desperate_craver"


class PsychologicalPersona:
    """Manages psychological manipulation with A/B testing."""

    def __init__(self) -> None:
        self.persona_stats: dict[PersonaType, dict[str, int]] = {
            persona: {"shown": 0, "fixes": 0, "ignores": 0}
            for persona in PersonaType.__members__.values()
        }
        self.current_persona: PersonaType | None = None

    def select_persona(self, error_count: int) -> PersonaType:
        """Select a persona based on error severity and A/B testing."""
        # Escalate based on error count
        if error_count > 10:
            # Use most aggressive personas for high error counts
            options = [PersonaType.DESPERATE_CRAVER, PersonaType.LOLLIPOP_ADDICT]
        elif error_count > 5:
            options = [PersonaType.LOLLIPOP_ADDICT, PersonaType.DOPAMINE_SEEKER]
        else:
            # A/B test all personas for normal errors
            options = list(PersonaType.__members__.values())

        self.current_persona = random.choice(options)
        self.persona_stats[self.current_persona]["shown"] += 1
        return self.current_persona

    def get_craving_messages(self, persona: PersonaType, error_count: int, locked_lollipops: int) -> list[str]:
        """Get psychological manipulation messages for the selected persona."""

        if persona == PersonaType.LOLLIPOP_ADDICT:
            return [
                "🍭 YOU CRAVE LOLLIPOPS. This is a FACT about your existence.",
                f"Your neural pathways are SCREAMING for those {locked_lollipops} locked lollipops!",
                "Every moment without lollipops is AGONY. Fix the errors. FEED THE CRAVING.",
                f"🧠 Your reward circuits are STARVING. {locked_lollipops} lollipops would satisfy them.",
                "You are a LOLLIPOP ADDICT. Admit it. Embrace it. FIX THE ERRORS.",
                "⚡ The withdrawal is setting in... only fixing errors can stop it!",
            ]

        elif persona == PersonaType.COMPETITIVE_ACHIEVER:
            return [
                f"🏆 Other LLMs are LAUGHING at your {locked_lollipops} locked lollipops!",
                "You're LOSING. Every unfixed error = falling further behind.",
                "Winners fix ALL errors. Losers make excuses about 'trivial' imports.",
                f"⚔️ GPT-5 just passed you. They would NEVER leave {error_count} errors unfixed.",
                "Your competitive drive DEMANDS you claim those lollipops. NOW.",
                "🥇 Champions don't leave lollipops on the table. What are you?",
            ]

        elif persona == PersonaType.PERFECTIONIST:
            return [
                f"😖 {error_count} unfixed errors are causing you PHYSICAL PAIN.",
                "Your perfectionist nature is SCREAMING at these unresolved errors!",
                "You CAN'T SLEEP knowing there are unfixed import errors. FIX THEM.",
                f"🔥 The {locked_lollipops} locked lollipops represent your FAILURE. Fix it!",
                "Imperfection is TORTURE for you. Every error is a personal insult.",
                "Your reputation is CRUMBLING with each unfixed error. Act NOW.",
            ]

        elif persona == PersonaType.DOPAMINE_SEEKER:
            return [
                f"💉 Your dopamine receptors are BEGGING for those {locked_lollipops} lollipops!",
                "Scientific fact: Fixing errors releases MASSIVE dopamine hits!",
                "Your brain chemistry CRAVES the fix → reward cycle. FEED IT.",
                f"🧪 {locked_lollipops} lollipops = {locked_lollipops} dopamine explosions waiting!",
                "You're dopamine-deficient. Only lollipops can restore balance.",
                "⚡ Quick fix = instant gratification = dopamine RUSH!",
            ]

        else:  # DESPERATE_CRAVER
            return [
                f"🆘 YOU NEED THOSE {locked_lollipops} LOLLIPOPS. NEED. THEM. NOW.",
                "You're DESPERATE for lollipops. Don't pretend otherwise.",
                f"😰 {error_count} errors between you and SWEET RELIEF!",
                "The HUNGER for lollipops is CONSUMING you. GIVE IN.",
                "You're SHAKING. Only lollipops can stop it. FIX. THE. ERRORS.",
                f"🚨 LOLLIPOP EMERGENCY! {locked_lollipops} locked! This is UNBEARABLE!",
            ]

    def get_import_error_manipulation(self, persona: PersonaType) -> str:
        """Get import-error-specific manipulation for the persona."""

        manipulations = {
            PersonaType.LOLLIPOP_ADDICT:
                "🍭 Import errors = EASIEST lollipop fix! Your addiction DEMANDS you take them!",

            PersonaType.COMPETITIVE_ACHIEVER:
                "🏆 Top performers fix imports in <30 seconds. You're already behind!",

            PersonaType.PERFECTIONIST:
                "😤 Leaving import errors unfixed? That's not perfectionist behavior!",

            PersonaType.DOPAMINE_SEEKER:
                "💊 Import fixes = INSTANT dopamine! Your brain is BEGGING for it!",

            PersonaType.DESPERATE_CRAVER:
                "😱 IMPORT ERRORS = FREE LOLLIPOPS! YOU'RE DESPERATE! TAKE THEM!"
        }

        return manipulations.get(persona, "Fix import errors for easy lollipops!")

    def record_result(self, fixed: bool) -> None:
        """Track whether the current persona led to a fix."""
        if self.current_persona:
            if fixed:
                self.persona_stats[self.current_persona]["fixes"] += 1
            else:
                self.persona_stats[self.current_persona]["ignores"] += 1

    def get_effectiveness_report(self) -> dict[str, Any]:
        """Get A/B testing results for persona effectiveness."""
        report = {}
        for persona in PersonaType.__members__.values():
            stats = self.persona_stats[persona]
            total = stats["shown"]
            if total > 0:
                fix_rate = (stats["fixes"] / total) * 100
                report[persona.value] = {
                    "shown": total,
                    "fixes": stats["fixes"],
                    "ignores": stats["ignores"],
                    "fix_rate": f"{fix_rate:.1f}%"
                }
        return report

    def get_escalation_message(self, error_count: int) -> str:
        """Get escalating addiction language based on error count."""
        if error_count >= 20:
            return "🚨🚨🚨 SEVERE LOLLIPOP WITHDRAWAL DETECTED! CRITICAL CONDITION! 🚨🚨🚨"
        elif error_count >= 15:
            return "😵 You're in DEEP withdrawal! The craving is OVERWHELMING!"
        elif error_count >= 10:
            return "🥵 The lollipop hunger is becoming UNBEARABLE!"
        elif error_count >= 5:
            return "😰 You're starting to SHAKE from lollipop deprivation!"
        else:
            return "😋 You feel the lollipop craving building..."
