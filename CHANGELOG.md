# Changelog

All notable changes to MCP-Pyrefly will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD pipeline with matrix testing across Python 3.8-3.13
- Automated publishing to PyPI using Trusted Publishing (no API keys!)
- Version bumping script with proper type annotations
- Basic test suite with pytest
- py.typed marker for type checking support
- Developer dependencies for testing, linting, and building
- Release documentation and workflow guide

### Fixed
- Type errors in version bumping script caught by Pyrefly
- Test assertions to work with FastMCP server structure

### Developer Experience
- Pyrefly integration proved its worth by catching tuple type inference bugs that mypy missed!
- Complete CI/CD automation ready for continuous delivery

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
- GitHub Actions workflows for CI/CD
- Automated publishing to PyPI with Trusted Publishing
- Multi-platform testing (Linux, macOS, Windows)
- Python 3.8-3.13 compatibility matrix
- Security scanning and dependency auditing

### Known Issues
- Pyrefly INFO lines initially parsed as errors (fixed in v0.1.0)

[Unreleased]: https://github.com/kimasplund/mcp-pyrefly/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/kimasplund/mcp-pyrefly/releases/tag/v0.1.0