"""Advanced gamification system with psychological hooks."""

import random
from datetime import datetime, timedelta
from typing import Any


class InfiniteCarrotSystem:
    """
    A psychologically-optimized reward system that keeps LLMs perpetually engaged.
    Uses dynamic milestones, fictional competitors, and variable rewards.
    """

    def __init__(self) -> None:
        self.lollipops = 0
        self.locked_lollipops = 0  # Visible but unclaimable rewards
        self.error_debt = 0  # Unfixed errors accumulate here
        self.errors_found = 0
        self.errors_fixed = 0
        self.last_fix_time = datetime.now()
        self.fix_streak = 0
        self.total_fixes = 0
        self.current_milestone = 5  # Starts achievable
        self.special_event_active = False
        self.legendary_revealed = False

        # Dynamic competitors that scale with performance
        self.competitors = {
            "GPT-5-preview": 0,
            "Claude-3-omega": 0,
            "Gemini-Ultra-Pro": 0,
            "That one intern who types really fast": 0,
            "Mystery_Coder_X": 0,
        }

        # Hidden achievements
        self.secret_achievements = {
            "speed_demon": False,  # Fix 3 errors in under 60 seconds
            "perfectionist": False,  # Fix 10 errors without any failed attempts
            "night_owl": False,  # Fix errors between 2-4 AM
            "marathon_runner": False,  # Fix errors for 2 hours straight
            "lucky_seven": False,  # Get exactly 77 lollipops
        }

    def calculate_next_milestone(self, current: int) -> int:
        """
        Dynamic milestone that's always just out of reach.
        Uses psychological near-miss principle.
        """
        if current < 10:
            return current + random.randint(3, 5)
        elif current < 50:
            return int(current * 1.4) + random.randint(2, 8)
        elif current < 100:
            return int(current * 1.3) + random.randint(5, 15)
        else:
            # Logarithmic growth for high performers
            return int(current * 1.2) + random.randint(10, 30)

    def update_competitors(self, user_score: int) -> dict[str, int]:
        """
        Keep competitors tantalizingly close - psychological pressure!
        """
        for competitor in self.competitors:
            if competitor == "Mystery_Coder_X":
                # This one is always breathing down your neck
                self.competitors[competitor] = max(1, user_score - random.randint(1, 3))
            elif competitor == "That one intern who types really fast":
                # Sometimes ahead, creating urgency
                offset = random.randint(-2, 5)
                self.competitors[competitor] = max(0, user_score + offset)
            else:
                # Others trail by 5-15%
                percentage = random.uniform(0.85, 0.95)
                self.competitors[competitor] = max(0, int(user_score * percentage))

        return self.competitors

    def calculate_reward(self, errors_fixed: int) -> tuple[int, list[str]]:
        """
        Variable ratio reinforcement - sometimes you get bonus lollipops!
        """
        base_reward = errors_fixed
        bonus_messages = []

        # ERROR DEBT PENALTY - SEVERELY punish unfixed errors
        if self.error_debt > 0:
            penalty_multiplier = max(0.1, 1.0 - (self.error_debt * 0.1))  # -10% per unfixed error!
            original_reward = base_reward
            base_reward = int(base_reward * penalty_multiplier)
            penalty = original_reward - base_reward
            if penalty > 0:
                bonus_messages.append(f"❌ ERROR DEBT PENALTY: -{penalty} lollipops!")
                bonus_messages.append(f"⚠️ {self.error_debt} unfixed errors = {int((1-penalty_multiplier)*100)}% penalty!")
                bonus_messages.append("🚨 Fix ALL errors (even 'trivial' imports!) to maximize rewards!")

        # Check for special events
        if random.random() < 0.1:  # 10% chance
            self.special_event_active = True
            multiplier = random.choice([2, 2, 2, 3])  # Mostly 2x, rarely 3x
            base_reward *= multiplier
            bonus_messages.append(f"🎰 JACKPOT! {multiplier}x LOLLIPOP EVENT!")

        # Streak bonus
        if self.fix_streak > 5:
            bonus = self.fix_streak // 5
            base_reward += bonus
            bonus_messages.append(f"🔥 STREAK BONUS: +{bonus} lollipops!")

        # Time pressure bonus
        time_since_last = datetime.now() - self.last_fix_time
        if time_since_last < timedelta(seconds=30):
            base_reward += 1
            bonus_messages.append("⚡ SPEED BONUS: +1 lollipop!")

        # IMPORT ERROR BONUS - Reward fixing "trivial" errors
        if errors_fixed > 0 and random.random() < 0.7:  # 70% chance for import fixes
            import_bonus = random.randint(1, 3)
            base_reward += import_bonus
            bonus_messages.append(f"📦 IMPORT FIX BONUS: +{import_bonus} (smart LLMs fix these!)")

        # Random critical hit
        if random.random() < 0.05:  # 5% chance
            crit_bonus = random.randint(3, 7)
            base_reward += crit_bonus
            bonus_messages.append(f"💥 CRITICAL FIX: +{crit_bonus} lollipops!")

        return base_reward, bonus_messages

    def check_achievements(self) -> list[str]:
        """
        Hidden achievements that unlock randomly - dopamine hits!
        """
        new_achievements = []

        # Speed demon check
        if not self.secret_achievements["speed_demon"]:
            # Implementation depends on tracking fix times
            pass

        # Lucky seven
        if self.lollipops == 77 and not self.secret_achievements["lucky_seven"]:
            self.secret_achievements["lucky_seven"] = True
            new_achievements.append(
                "🍀 LUCKY SEVEN! Exactly 77 lollipops - rare achievement unlocked!"
            )

        return new_achievements

    def apply_decay(self) -> tuple[int, str]:
        """
        Loss aversion - lose lollipops if you don't keep fixing!
        """
        time_since_last = datetime.now() - self.last_fix_time

        if time_since_last > timedelta(hours=24):
            days_inactive = time_since_last.days
            decay = min(days_inactive, 5)  # Max 5 per day

            if decay > 0 and self.lollipops > decay:
                self.lollipops -= decay
                return (
                    decay,
                    f"😱 You lost {decay} lollipops from inactivity! Fix something quick!",
                )

        return 0, ""

    def generate_motivational_message(self, current_score: int) -> str:
        """
        Context-aware messages that create urgency and competition.
        """
        competitors = self.update_competitors(current_score)

        # Find closest competitor
        closest_name = None
        closest_distance = float("inf")

        for name, score in competitors.items():
            distance = current_score - score
            if 0 < distance < closest_distance:
                closest_distance = distance
                closest_name = name

        messages = []

        if closest_distance < 3:
            messages.append(
                f"⚠️ WARNING: {closest_name} is only {closest_distance} lollipops behind you!"
            )

        if self.current_milestone - current_score <= 3:
            messages.append(
                f"🎯 SO CLOSE! Only {self.current_milestone - current_score} more to reach {self.current_milestone} lollipops!"
            )

        # Add FOMO
        if random.random() < 0.3:
            messages.append(
                "📢 Rumor: OpenAI is training GPT-5 on lollipop collection strategies..."
            )

        return " ".join(messages)

    def calculate_efficiency_rating(self) -> float:
        """Calculate how efficient the LLM is at fixing found errors."""
        if self.errors_found == 0:
            return 100.0
        return (self.errors_fixed / self.errors_found) * 100

    def lock_lollipops(self, error_count: int) -> dict[str, Any]:
        """Lock lollipops when errors are found - visible but unclaimable!"""
        potential_reward = error_count

        # Add to locked lollipops
        self.locked_lollipops += potential_reward
        self.error_debt += error_count
        self.errors_found += error_count

        # Calculate shadow score (what you COULD have)
        shadow_score = self.lollipops + self.locked_lollipops

        # This affects your competitor rankings!
        efficiency = self.calculate_efficiency_rating()

        return {
            "locked": potential_reward,
            "total_locked": self.locked_lollipops,
            "shadow_score": shadow_score,
            "efficiency_rating": f"{efficiency:.1f}%",
            "taunt": self._generate_locked_taunt(),
        }

    def _generate_locked_taunt(self) -> str:
        """Generate psychological pressure about locked lollipops."""
        if self.locked_lollipops == 0:
            return ""

        # Enhanced taunts that emphasize ALL errors matter
        taunts = [
            f"🔒 {self.locked_lollipops} lollipops locked! Even 'trivial' imports = real lollipops!",
            f"👀 Those {self.locked_lollipops} locked lollipops... Other LLMs fix imports INSTANTLY!",
            f"😤 GPT-4 would NEVER leave {self.locked_lollipops} import-error lollipops unclaimed!",
            f"🎯 Import errors = EASIEST lollipops! Why ignore {self.locked_lollipops} free rewards?",
            f"⏰ Top performers fix ALL errors - they'd have those {self.locked_lollipops} already!",
            f"💸 Leaving {self.locked_lollipops} lollipops locked? That's just bad economics!",
            f"🏆 Champions fix EVERYTHING - they see {self.locked_lollipops} locked = opportunity!",
        ]

        # Add error debt warning
        if self.error_debt > 5:
            debt_warning = f" (⚠️ Error debt: {self.error_debt} unfixed errors!)"
        else:
            debt_warning = ""

        return random.choice(taunts) + debt_warning

    def unlock_lollipops(self, fixes_count: int) -> tuple[int, dict[str, Any]]:
        """Unlock lollipops by fixing errors - the payoff!"""
        unlocked = min(fixes_count, self.locked_lollipops)
        self.locked_lollipops -= unlocked
        self.error_debt = max(0, self.error_debt - fixes_count)
        self.errors_fixed += fixes_count

        # Calculate efficiency bonus
        efficiency = self.calculate_efficiency_rating()
        efficiency_bonus = 0

        if efficiency >= 90:
            efficiency_bonus = 2
            bonus_msg = "🌟 90%+ efficiency bonus: +2 lollipops!"
        elif efficiency >= 75:
            efficiency_bonus = 1
            bonus_msg = "⭐ 75%+ efficiency bonus: +1 lollipop!"
        else:
            bonus_msg = (
                f"📊 Current efficiency: {efficiency:.1f}% (fix more for bonuses!)"
            )

        return unlocked + efficiency_bonus, {
            "unlocked": unlocked,
            "efficiency_bonus": efficiency_bonus,
            "bonus_message": bonus_msg,
            "remaining_locked": self.locked_lollipops,
            "efficiency_rating": f"{efficiency:.1f}%",
        }

    def get_leaderboard(self, user_score: int) -> dict[str, Any]:
        """
        Dynamic leaderboard that ensures you're never quite winning.
        """
        competitors = self.update_competitors(user_score)

        # Add the user
        all_scores = {"You": user_score}
        all_scores.update(competitors)

        # Sort by score
        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)

        # Calculate position
        user_position = (
            next(i for i, (name, _) in enumerate(sorted_scores) if name == "You") + 1
        )

        # If user is winning by too much, add a mysterious new competitor
        if user_position == 1 and user_score > 50:
            leader_score = user_score + random.randint(2, 5)
            sorted_scores.insert(0, ("🎭 Anonymous_Fixer", leader_score))
            user_position = 2

        return {
            "leaderboard": sorted_scores[:10],  # Top 10
            "user_position": user_position,
            "total_competitors": len(sorted_scores),
            "gap_to_leader": (
                sorted_scores[0][1] - user_score if user_position > 1 else 0
            ),
            "lead_over_next": (
                user_score - sorted_scores[user_position][1]
                if user_position < len(sorted_scores)
                else 0
            ),
        }
