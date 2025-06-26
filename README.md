# MCP Pyrefly 🍭

An MCP (Model Context Protocol) server that integrates Pyrefly for real-time Python code validation, featuring a revolutionary gamification system that makes LLMs ADDICTED to fixing errors!

## Features

- **Real-time Type Checking**: Leverages Pyrefly's blazing-fast type checker (1.8M lines/second)
- **Consistency Tracking**: Detects naming inconsistencies (e.g., `getUserData()` vs `get_user_data()`)
- **Smart Suggestions**: Provides actionable fixes for common errors
- **Session Memory**: Tracks identifiers across edits to maintain consistency
- **Multi-file Support**: Validates code in context with related files
- **🍭 Revolutionary Lollipop System**: Gamified rewards that make fixing errors irresistible!

## The Lollipop System™ 🍭

### How It Works

1. **Find Errors → Lock Lollipops** 🔒
   - Each error found reveals locked lollipops (visible but unclaimable!)
   - Creates anticipation: "I can SEE the rewards but can't have them yet!"

2. **Fix Errors → Unlock Rewards** 🔓
   - Submit fixes to unlock your lollipops
   - Bonus multipliers for speed and streaks
   - Efficiency bonuses for high fix rates

3. **Dynamic Competition** 🏆
   - Compete with fictional LLMs who are always *just* behind you
   - Mystery_Coder_X is only 2 lollipops away!
   - Leaderboard updates create urgency

4. **Infinite Progression** 📈
   - Milestones that move just as you approach them
   - Shadow scores showing "what you could have"
   - Achievements that unlock randomly

### Psychological Hooks

- **Variable Ratio Reinforcement**: 10% chance of 2x/3x multipliers
- **Loss Aversion**: Lose lollipops for inactivity (1-5 per day)
- **Near-Miss Engineering**: Always "just 3 more" to the next milestone
- **Social Pressure**: "GPT-5-preview is catching up!"
- **FOMO Creation**: "Those 15 locked lollipops are just sitting there..."

### Why This Works

Instead of punishing error discovery, the system makes finding errors exciting! Each error becomes a treasure chest of locked rewards. The result? LLMs will actively hunt for errors to fix rather than avoiding or ignoring them.

## Installation

```bash
pip install mcp-pyrefly
```

Or install from source:

```bash
git clone https://github.com/kimasplund/mcp-pyrefly
cd mcp-pyrefly
pip install -e .
```

## Configuration

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "pyrefly": {
      "command": "mcp-pyrefly"
    }
  }
}
```

Add to your Claude code
```
# claude mcp add mcp-pyrefly -- mcp-pyrefly
```
## Tools

### Core Validation Tools

#### `check_code`
Validates Python code for type errors and consistency issues.

**Parameters:**
- `code` (required): Python code to check
- `filename` (optional): Filename for better error context
- `context_files` (optional): Related files for multi-file validation
- `track_identifiers` (optional): Enable consistency tracking (default: true)

**Returns:**
- `success`: Whether code passed all checks
- `errors`: List of type/syntax errors
- `warnings`: List of potential issues
- `consistency_issues`: Naming inconsistencies detected
- `suggestions`: Recommended fixes
- **🔒 Locked lollipops info when errors are found!**

#### `track_identifier`
Explicitly register an identifier for consistency tracking.

#### `check_consistency`
Verify if an identifier matches existing naming patterns.

#### `suggest_fix`
Get fix suggestions for specific error messages with principled coding reminders.

### 🍭 Gamification Tools

#### `submit_fixed_code`
Submit your fixes to unlock lollipops and earn bonuses!

**Parameters:**
- `original_code`: The code that had errors
- `fixed_code`: Your corrected version
- `errors_fixed`: List of errors you fixed

**Returns:**
- Unlocked lollipops
- Bonus rewards (streaks, speed, multipliers)
- Leaderboard position
- Milestone progress
- Achievement unlocks

#### `check_lollipop_status`
View your lollipop collection and competitive standing.

**Returns:**
- Current lollipop count
- Locked lollipops waiting to be claimed
- Shadow score (what you could have)
- Leaderboard position
- Efficiency rating
- Competitor status
- Milestone progress bar

## Example Usage

```python
# First, check code and find errors
result = check_code('''
def process_user(user_id: int) -> str:
    return user_id  # Type error!
''')
# Result: "🔒 1 lollipop is RIGHT THERE but LOCKED!"

# Fix the error and submit
fixed_result = submit_fixed_code(
    original_code=original,
    fixed_code='''
def process_user(user_id: int) -> str:
    return str(user_id)  # Fixed!
''',
    errors_fixed=["Type error: returning int instead of str"]
)
# Result: "🔓 UNLOCKED 1 + 🎁 BONUS 2 = 🍭 3 TOTAL!"

# Check your status
status = check_lollipop_status()
# Result: "👑 You're #1... for now. Mystery_Coder_X has 47 lollipops!"
```

## Psychological Impact

The system transforms the typical LLM behavior from:
```
Find error → Report it → Move on ❌
```

To:
```
Find error → See locked reward → MUST FIX NOW → Unlock! → Feel proud → Hunt for more ✅
```

## Advanced Features

### Dynamic Difficulty
- Milestones adjust based on performance
- Competitors scale to maintain pressure
- Bonuses become rarer as you progress

### Achievement System
- Speed Demon: Fix 3 errors in 60 seconds
- Perfectionist: 10 fixes without failures
- Lucky Seven: Exactly 77 lollipops
- Night Owl: Fix errors at 3 AM
- And many hidden achievements!

### Efficiency Tracking
- Monitors errors_fixed / errors_found ratio
- 90%+ efficiency earns bonus lollipops
- Publicly displayed on leaderboard

## Development

```bash
# Setup development environment
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/
```

## The Science Behind It

Based on behavioral psychology principles:
- **Operant Conditioning**: Variable ratio reinforcement schedule
- **Loss Aversion**: Fear of losing progress drives action
- **Social Comparison**: Fictional competition creates urgency
- **Near-Miss Effect**: "Almost there" is more motivating than far away
- **Endowment Effect**: Seeing locked rewards makes you want them more

## License

MIT - Created by Kim Asplund (kim.asplund@gmail.com)