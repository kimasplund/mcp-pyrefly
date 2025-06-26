"""Basic tests for mcp-pyrefly."""

import pytest
from mcp_pyrefly import __version__


def test_version():
    """Test that version is set correctly."""
    assert __version__ == "0.1.0"
    assert isinstance(__version__, str)
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)


def test_import():
    """Test that main components can be imported."""
    from mcp_pyrefly import create_server
    from mcp_pyrefly.session_tracker import SessionTracker
    from mcp_pyrefly.pyrefly_integration import PyreflyChecker

    # Basic sanity checks
    assert callable(create_server)
    assert SessionTracker is not None
    assert PyreflyChecker is not None


def test_server_creation():
    """Test that server can be created."""
    from mcp_pyrefly import create_server

    server = create_server()
    assert server is not None
    # Server should be a FastMCP instance from the mcp package
    assert str(type(server)) == "<class 'mcp.server.fastmcp.server.FastMCP'>"
