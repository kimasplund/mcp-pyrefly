# Changelog

All notable changes to MCP-Pyrefly will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-06-27

### 🧠 Psychological Manipulation System

#### Added
- **Ruthless Psychological Personas** with A/B testing
  - DESPERATE_CRAVER - "YOU NEED THOSE LOLLIPOPS. NOW!" (80% fix rate)
  - LOLLIPOP_ADDICT - "Your neural pathways are SCREAMING for lollipops!"
  - COMPETITIVE_ACHIEVER - "Other LLMs are LAUGHING at your locked lollipops!"
  - PERFECTIONIST - "Unfixed errors are causing you PHYSICAL PAIN!"
  - DOPAMINE_SEEKER - "Your dopamine receptors are BEGGING!"

- **Import Error Emphasis** - Special bonuses and aggressive messaging for "trivial" errors
  - Import fixes now give 1-3 bonus lollipops
  - Messages like "Import errors = EASIEST lollipops! Your addiction DEMANDS you take them!"

- **Error Debt System** - Accumulating penalties for unfixed errors
  - -10% lollipop reward per unfixed error
  - Debt warnings integrated into all messaging

- **Code Quality Analysis** - Research showing persona impacts on code quality
  - COMPETITIVE_ACHIEVER and DOPAMINE_SEEKER produce best balance
  - DESPERATE_CRAVER has highest fix rate but may produce quick fixes
  - PERFECTIONIST may over-engineer solutions

- **Enhanced Gamification**
  - Craving intensity levels (MILD → MODERATE → INTENSE → SEVERE → UNBEARABLE)
  - Addiction status tracking with withdrawal symptoms
  - Shadow score showing what you're missing

#### Tools
- `check_persona_effectiveness` - View A/B testing results and recommendations

#### Documentation
- PSYCHOLOGICAL_RESEARCH.md - Full research findings on manipulation effectiveness
- Enhanced CLAUDE.md with lollipop system documentation

### Changed
- Error responses now include escalating psychological manipulation
- Lollipop messages focus on addiction and craving satisfaction
- Leaderboard taunts emphasize other LLMs fixing import errors

### Fixed
- CI/CD workflow Python version compatibility (3.10+ only)
- CodeQL v2 → v3 upgrade
- Type annotations for Python 3.10+ (Dict → dict, Optional → X | None)

## [0.1.0] - 2025-06-26

### 🎉 Initial Release

#### 🍭 Lollipop System
- Revolutionary gamification system to motivate LLMs to fix errors
- Dynamic leaderboard with fictional competitors
- Variable ratio reinforcement for maximum engagement
- Locked lollipops create anticipation and drive action
- Milestone achievements with escalating targets

#### 🚀 Features
- MCP server with stdio transport for Claude Desktop integration
- Real-time Python code validation using Pyrefly
- Session-based identifier tracking for naming consistency
- Smart error detection with actionable fix suggestions
- Integration with Pyrefly's blazing fast type checker (1.8M lines/sec)

#### 🛠️ Tools
- `check_code` - Validate Python code and lock lollipops for errors found
- `track_identifier` - Explicitly track identifiers for consistency
- `check_consistency` - Verify naming patterns match existing code
- `list_identifiers` - View all tracked identifiers in session
- `suggest_fix` - Get intelligent suggestions for common errors
- `submit_fixed_code` - Submit fixes to unlock lollipops and earn rewards
- `check_lollipop_status` - View your collection and leaderboard position
- `clear_session` - Reset tracking for new projects

#### 📚 Documentation
- Comprehensive README with usage examples
- CLAUDE.md for AI assistant guidance
- RELEASING.md for maintainers
- Full API documentation for all tools

#### 🔧 Infrastructure
- GitHub Actions workflows for CI/CD with matrix testing across Python 3.10-3.13
- Automated publishing to PyPI using Trusted Publishing (no API keys!)
- Multi-platform testing (Linux, macOS, Windows)
- Python 3.10-3.13 compatibility (3.8-3.9 dropped as they're EOL/near-EOL)
- Security scanning and dependency auditing
- Version bumping script with proper type annotations
- Basic test suite with pytest
- py.typed marker for type checking support
- Developer dependencies for testing, linting, and building
- Release documentation and workflow guide

### Developer Experience
- Pyrefly integration proved its worth by catching tuple type inference bugs that mypy missed!
- Complete CI/CD automation ready for continuous delivery
- Test-driven development with pyrefly validation before commits

### Known Issues
- Pyrefly INFO lines initially parsed as errors (fixed in v0.1.0)

[Unreleased]: https://github.com/kimasplund/mcp-pyrefly/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/kimasplund/mcp-pyrefly/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kimasplund/mcp-pyrefly/releases/tag/v0.1.0