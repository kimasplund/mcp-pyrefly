"""Integration with Pyrefly type checker."""

import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PyreflyChecker:
    """Wrapper for Pyrefly type checking functionality."""

    def __init__(self):
        self.pyrefly_path = self._find_pyrefly()
        if not self.pyrefly_path:
            raise RuntimeError("Pyrefly not found in PATH or virtual environment")

    def _find_pyrefly(self) -> str | None:
        """Find the pyrefly executable."""
        # Try to find in PATH first
        result = subprocess.run(["which", "pyrefly"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()

        # Try in current virtual environment
        venv_paths = [
            ".venv/bin/pyrefly",
            "venv/bin/pyrefly",
            ".venv/Scripts/pyrefly.exe",
            "venv/Scripts/pyrefly.exe",
        ]

        for path in venv_paths:
            if os.path.exists(path):
                return os.path.abspath(path)

        return None

    def check_code(
        self,
        code: str,
        filename: str | None = None,
        context: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Check Python code using Pyrefly.

        Args:
            code: Python code to check
            filename: Optional filename for better error messages
            context: Optional dict of other files for multi-file checking

        Returns:
            Dict with 'errors', 'warnings', and 'success' keys
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write main file
            main_file = Path(tmpdir) / (filename or "check.py")
            main_file.write_text(code, encoding="utf-8")

            # Write context files if provided
            if context:
                for fname, content in context.items():
                    context_file = Path(tmpdir) / fname
                    context_file.parent.mkdir(parents=True, exist_ok=True)
                    context_file.write_text(content, encoding="utf-8")

            # Run Pyrefly
            result = subprocess.run(
                [self.pyrefly_path, "check", str(main_file)],
                capture_output=True,
                text=True,
                cwd=tmpdir,
            )

            return self._parse_output(result, str(main_file))

    def _parse_output(
        self, result: subprocess.CompletedProcess, filepath: str
    ) -> dict[str, Any]:
        """Parse Pyrefly output into structured format."""
        errors = []
        warnings = []

        # Pyrefly output format:
        # ERROR message [error-code]
        #  --> file:line:column
        #   |
        # N | code line
        #   |      ^

        if result.stdout:
            lines = result.stdout.strip().split("\n")
            i = 0
            while i < len(lines):
                line = lines[i].strip()

                # Skip empty lines and INFO lines
                if not line or line.startswith("INFO"):
                    i += 1
                    continue

                # Parse ERROR/WARNING lines
                if line.startswith(("ERROR", "WARNING")):
                    severity = "error" if line.startswith("ERROR") else "warning"

                    # Extract message and error code
                    if "[" in line and "]" in line:
                        msg_end = line.rfind("[")
                        message = line[len(severity) + 1 : msg_end].strip()
                        code = line[msg_end + 1 : -1]
                    else:
                        message = line[len(severity) + 1 :].strip()
                        code = ""

                    # Look for location on next line (starts with " -->")
                    line_num = 0
                    col_num = 0
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith("-->"):
                        location_line = lines[i + 1].strip()
                        # Parse: --> /path/to/file:line:column
                        location = location_line[4:].strip()
                        parts = location.rsplit(":", 2)
                        if len(parts) >= 3:
                            try:
                                line_num = int(parts[1])
                                col_num = int(parts[2])
                            except ValueError:
                                pass

                    entry = {
                        "line": line_num,
                        "column": col_num,
                        "message": message,
                        "severity": severity,
                        "code": code,
                    }

                    if severity == "error":
                        errors.append(entry)
                    else:
                        warnings.append(entry)

                i += 1

        # Check stderr for other errors
        if result.stderr:
            stderr_lines = result.stderr.strip().split("\n")
            for line in stderr_lines:
                line_stripped = line.strip()
                # Skip INFO lines in stderr
                if not line_stripped or line_stripped.startswith("INFO"):
                    continue
                # Only add actual errors, not just any line containing 'error'
                if "error" in line_stripped.lower() and not line_stripped.startswith(
                    ("INFO", "WARNING")
                ):
                    errors.append(
                        {
                            "line": 0,
                            "column": 0,
                            "message": line_stripped,
                            "severity": "error",
                            "code": "",
                        }
                    )

        return {
            "success": result.returncode == 0 and len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "raw_output": result.stdout,
            "raw_stderr": result.stderr,
        }

    def _parse_text_line(self, line: str) -> dict[str, Any]:
        """Parse a text error/warning line."""
        # Try to extract line/column info
        import re

        match = re.search(r":(\d+):(\d+):", line)
        if match:
            line_num = int(match.group(1))
            col_num = int(match.group(2))
            message = line[match.end() :].strip()
        else:
            line_num = 0
            col_num = 0
            message = line

        return {
            "line": line_num,
            "column": col_num,
            "message": message,
            "severity": "error" if "error" in line.lower() else "warning",
        }

    def extract_identifiers(self, code: str) -> list[dict[str, str]]:
        """Extract function, class, and variable definitions from code."""
        identifiers = []

        # Simple regex-based extraction (Pyrefly might provide better AST access)
        import re

        # Functions
        func_pattern = r"^(?:async\s+)?def\s+(\w+)\s*\([^)]*\)"
        for match in re.finditer(func_pattern, code, re.MULTILINE):
            identifiers.append(
                {
                    "name": match.group(1),
                    "type": "function",
                    "line": code[: match.start()].count("\n") + 1,
                }
            )

        # Classes
        class_pattern = r"^class\s+(\w+)(?:\s*\([^)]*\))?:"
        for match in re.finditer(class_pattern, code, re.MULTILINE):
            identifiers.append(
                {
                    "name": match.group(1),
                    "type": "class",
                    "line": code[: match.start()].count("\n") + 1,
                }
            )

        # Top-level variables (simple assignment)
        var_pattern = r"^(\w+)\s*="
        for match in re.finditer(var_pattern, code, re.MULTILINE):
            name = match.group(1)
            # Skip if it's a known keyword or builtin
            if name not in ["if", "for", "while", "def", "class", "import", "from"]:
                identifiers.append(
                    {
                        "name": name,
                        "type": "variable",
                        "line": code[: match.start()].count("\n") + 1,
                    }
                )

        return identifiers
