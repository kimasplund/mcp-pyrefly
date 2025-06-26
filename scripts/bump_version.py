#!/usr/bin/env python3
"""
Version bumping script for mcp-pyrefly.
Usage: python scripts/bump_version.py [major|minor|patch]
"""

import sys
import re
from pathlib import Path


def get_current_version() -> tuple[int, int, int]:
    """Extract current version from pyproject.toml."""
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()
    match = re.search(r'version = "(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    groups = match.groups()
    return int(groups[0]), int(groups[1]), int(groups[2])


def bump_version(version_type="patch"):
    """Bump version based on type (major, minor, patch)."""
    current = get_current_version()
    major: int = current[0]
    minor: int = current[1]
    patch: int = current[2]
    
    if version_type == "major":
        major = major + 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor = minor + 1
        patch = 0
    elif version_type == "patch":
        patch = patch + 1
    else:
        raise ValueError(f"Invalid version type: {version_type}")
    
    return f"{major}.{minor}.{patch}"


def update_version(new_version):
    """Update version in all relevant files."""
    # Update pyproject.toml
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()
    content = re.sub(
        r'version = "\d+\.\d+\.\d+"',
        f'version = "{new_version}"',
        content
    )
    pyproject.write_text(content)
    
    # Update __init__.py if it exists
    init_file = Path("src/mcp_pyrefly/__init__.py")
    if init_file.exists():
        content = init_file.read_text()
        content = re.sub(
            r'__version__ = "\d+\.\d+\.\d+"',
            f'__version__ = "{new_version}"',
            content
        )
        init_file.write_text(content)
    
    print(f"Version bumped to {new_version}")


if __name__ == "__main__":
    version_type = sys.argv[1] if len(sys.argv) > 1 else "patch"
    new_version = bump_version(version_type)
    update_version(new_version)