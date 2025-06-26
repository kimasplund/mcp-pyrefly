# Release Process for MCP-Pyrefly

This document outlines the release process for publishing mcp-pyrefly to PyPI.

## Prerequisites

1. **PyPI Account Setup**
   - Create accounts on [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)
   - Enable 2FA on both accounts for security

2. **Configure Trusted Publishing**
   - Go to your PyPI account settings → Publishing
   - Add a new trusted publisher:
     - Repository owner: `kimasplund`
     - Repository name: `mcp-servers-dev`
     - Workflow name: `publish.yml`
     - Environment: `pypi`
   - Repeat for TestPyPI with environment `testpypi`

3. **GitHub Repository Setup**
   - Create two environments in repository settings:
     - `testpypi` - no protection rules needed
     - `pypi` - add protection rule requiring manual approval

## Release Workflow

### 1. Prepare Release

```bash
# Ensure you're on main branch with latest changes
git checkout main
git pull origin main

# Run tests locally
pytest tests/
mypy src/
ruff check src/

# Bump version (patch, minor, or major)
python scripts/bump_version.py patch  # or minor/major

# Update CHANGELOG.md with release notes
# Document all changes, especially:
# - New lollipop features 🍭
# - Bug fixes
# - Breaking changes
```

### 2. Create Release Commit

```bash
# Commit version bump and changelog
git add pyproject.toml src/mcp_pyrefly/__init__.py CHANGELOG.md
git commit -m "chore: Bump version to X.Y.Z"
git push origin main
```

### 3. Tag Release

```bash
# Create annotated tag
git tag -a v0.1.1 -m "Release v0.1.1: Enhanced lollipop system"
git push origin v0.1.1
```

### 4. Monitor Release Pipeline

The GitHub Actions workflow will automatically:
1. Run full test matrix across Python 3.8-3.12
2. Build source and wheel distributions
3. Publish to TestPyPI
4. Test installation from TestPyPI
5. **Wait for manual approval** (check GitHub Actions)
6. Publish to PyPI
7. Create GitHub release with artifacts

### 5. Verify Release

```bash
# Test installation from PyPI
pip install mcp-pyrefly

# Verify it works
mcp-pyrefly --version
python -c "import mcp_pyrefly; print(mcp_pyrefly.__version__)"
```

## Emergency Rollback

If issues are discovered post-release:

1. **Yank from PyPI** (if critical):
   ```bash
   # Use twine to yank (marks version as "don't use")
   twine yank mcp-pyrefly==X.Y.Z
   ```

2. **Fix and Re-release**:
   - Fix the issue
   - Bump patch version
   - Tag and release again

## First Release Checklist

For the initial v0.1.0 release:

- [ ] Reserve package name on PyPI by uploading a dummy package
- [ ] Configure trusted publishers on both PyPI and TestPyPI
- [ ] Create GitHub environments with protection rules
- [ ] Test the full workflow with a pre-release version (0.1.0rc1)
- [ ] Update README with installation instructions
- [ ] Add PyPI badges to README

## Security Notes

- Never use API tokens - Trusted Publishing is more secure
- Always test on TestPyPI first
- Use environment protection rules for production PyPI
- Keep dependencies up to date with security patches

## Troubleshooting

### "Environment not found" error
- Ensure environments are created in GitHub repository settings
- Check environment names match exactly: `pypi` and `testpypi`

### Trusted Publishing fails
- Verify publisher configuration matches exactly
- Ensure workflow has `id-token: write` permission
- Check GitHub Actions OIDC token is enabled

### Package not appearing on PyPI
- Wait a few minutes for CDN propagation
- Check https://pypi.org/project/mcp-pyrefly/
- Verify no errors in GitHub Actions logs