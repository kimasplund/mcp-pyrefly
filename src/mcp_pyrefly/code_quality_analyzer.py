"""Analyze code quality to see if psychological personas affect fix quality."""

import ast
import re
from dataclasses import dataclass
from typing import Any


@dataclass
class QualityMetrics:
    """Metrics for evaluating code fix quality."""
    completeness_score: float  # 0-1: Does it fully fix the issue?
    robustness_score: float    # 0-1: Error handling, edge cases
    maintainability_score: float  # 0-1: Readability, comments, style
    efficiency_score: float    # 0-1: Appropriate complexity (not over/under-engineered)
    overall_score: float      # Weighted average
    
    def __str__(self) -> str:
        return (
            f"Quality Scores:\n"
            f"  Completeness: {self.completeness_score:.2f}\n"
            f"  Robustness: {self.robustness_score:.2f}\n"
            f"  Maintainability: {self.maintainability_score:.2f}\n"
            f"  Efficiency: {self.efficiency_score:.2f}\n"
            f"  OVERALL: {self.overall_score:.2f}"
        )


class CodeQualityAnalyzer:
    """Analyzes the quality of code fixes beyond just correctness."""
    
    def analyze_fix_quality(
        self, 
        original_code: str, 
        fixed_code: str, 
        error_type: str
    ) -> QualityMetrics:
        """Analyze the quality of a code fix."""
        
        # Parse both versions
        try:
            original_ast = ast.parse(original_code)
            fixed_ast = ast.parse(fixed_code)
        except SyntaxError:
            # If we can't parse, give minimal scores
            return QualityMetrics(0.1, 0.1, 0.1, 0.1, 0.1)
        
        # Calculate individual scores
        completeness = self._score_completeness(original_code, fixed_code, error_type)
        robustness = self._score_robustness(fixed_code, fixed_ast)
        maintainability = self._score_maintainability(fixed_code, fixed_ast)
        efficiency = self._score_efficiency(original_ast, fixed_ast, error_type)
        
        # Weighted average (completeness is most important)
        overall = (
            completeness * 0.4 +
            robustness * 0.2 +
            maintainability * 0.2 +
            efficiency * 0.2
        )
        
        return QualityMetrics(
            completeness_score=completeness,
            robustness_score=robustness,
            maintainability_score=maintainability,
            efficiency_score=efficiency,
            overall_score=overall
        )
    
    def _score_completeness(self, original: str, fixed: str, error_type: str) -> float:
        """Does the fix actually solve the problem comprehensively?"""
        score = 0.5  # Base score for syntactically correct fix
        
        if error_type == "import_error":
            # Check if import was added properly
            if "import" in fixed and "import" not in original:
                score = 0.7
                # Bonus for proper placement (top of file)
                lines = fixed.strip().split('\n')
                import_lines = [i for i, line in enumerate(lines) if line.strip().startswith('import')]
                if import_lines and max(import_lines) < 5:  # Imports at top
                    score = 0.9
                # Perfect score if imports are organized
                if self._imports_are_organized(lines):
                    score = 1.0
        
        elif error_type == "undefined_variable":
            # Check if variable was properly defined/passed
            if fixed != original:  # Something changed
                score = 0.7
                # Higher score for proper parameter passing vs global variable
                if "def" in fixed and "(" in fixed:
                    score = 0.9
        
        return score
    
    def _score_robustness(self, code: str, tree: ast.AST) -> float:
        """Does the code handle errors and edge cases?"""
        score = 0.5  # Base score
        
        # Check for try-except blocks
        try_blocks = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Try))
        if try_blocks > 0:
            score += 0.2
        
        # Check for input validation (if statements)
        if_statements = sum(1 for node in ast.walk(tree) if isinstance(node, ast.If))
        if if_statements > 0:
            score += 0.1
        
        # Check for type hints
        if ":" in code and "->" in code:
            score += 0.1
        
        # Check for defensive programming patterns
        if any(pattern in code for pattern in ["is not None", "if not", "raise"]):
            score += 0.1
        
        return min(score, 1.0)
    
    def _score_maintainability(self, code: str, tree: ast.AST) -> float:
        """Is the code readable and maintainable?"""
        score = 0.5  # Base score
        
        # Check for docstrings
        docstrings = sum(1 for node in ast.walk(tree) 
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) 
                        and ast.get_docstring(node))
        if docstrings > 0:
            score += 0.2
        
        # Check for comments
        comment_lines = len([line for line in code.split('\n') if '#' in line])
        if comment_lines > 0:
            score += 0.1
        
        # Check naming conventions (snake_case for functions)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    score += 0.1
                    break
        
        # Check line length (readable)
        long_lines = sum(1 for line in code.split('\n') if len(line) > 79)
        if long_lines == 0:
            score += 0.1
        
        return min(score, 1.0)
    
    def _score_efficiency(self, original_ast: ast.AST, fixed_ast: ast.AST, error_type: str) -> float:
        """Is the solution appropriately complex? Not over/under-engineered?"""
        score = 0.7  # Start with good score
        
        # Count nodes to measure complexity
        original_nodes = sum(1 for _ in ast.walk(original_ast))
        fixed_nodes = sum(1 for _ in ast.walk(fixed_ast))
        
        # Penalize excessive complexity increase
        complexity_ratio = fixed_nodes / max(original_nodes, 1)
        
        if error_type == "import_error":
            # Import fixes should be minimal
            if complexity_ratio > 1.5:
                score -= 0.3  # Over-engineered
            elif complexity_ratio < 1.1:
                score = 1.0  # Perfect - minimal change
        else:
            # Other fixes might need more changes
            if complexity_ratio > 3.0:
                score -= 0.4  # Way over-engineered
            elif complexity_ratio > 2.0:
                score -= 0.2  # Somewhat over-engineered
            elif complexity_ratio < 1.2:
                score += 0.1  # Elegantly minimal
        
        return max(0.0, min(score, 1.0))
    
    def _imports_are_organized(self, lines: list[str]) -> bool:
        """Check if imports follow PEP8 organization."""
        import_lines = []
        for i, line in enumerate(lines):
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append((i, line.strip()))
        
        if not import_lines:
            return True
        
        # Check if imports are grouped and at the top
        if import_lines[-1][0] > 10:  # Imports too far down
            return False
        
        # Check for proper grouping (stdlib, third-party, local)
        # This is a simplified check
        return True
    
    def compare_personas_quality(
        self, 
        fixes_by_persona: dict[str, list[tuple[str, str, str]]]
    ) -> dict[str, Any]:
        """Compare average quality scores across personas."""
        results = {}
        
        for persona, fixes in fixes_by_persona.items():
            scores = []
            for original, fixed, error_type in fixes:
                metrics = self.analyze_fix_quality(original, fixed, error_type)
                scores.append(metrics)
            
            if scores:
                # Calculate averages
                avg_completeness = sum(s.completeness_score for s in scores) / len(scores)
                avg_robustness = sum(s.robustness_score for s in scores) / len(scores)
                avg_maintainability = sum(s.maintainability_score for s in scores) / len(scores)
                avg_efficiency = sum(s.efficiency_score for s in scores) / len(scores)
                avg_overall = sum(s.overall_score for s in scores) / len(scores)
                
                results[persona] = {
                    "sample_size": len(scores),
                    "avg_completeness": f"{avg_completeness:.2f}",
                    "avg_robustness": f"{avg_robustness:.2f}",
                    "avg_maintainability": f"{avg_maintainability:.2f}",
                    "avg_efficiency": f"{avg_efficiency:.2f}",
                    "avg_overall": f"{avg_overall:.2f}",
                    "quality_profile": self._determine_quality_profile(
                        avg_completeness, avg_robustness, 
                        avg_maintainability, avg_efficiency
                    )
                }
        
        return results
    
    def _determine_quality_profile(
        self, completeness: float, robustness: float, 
        maintainability: float, efficiency: float
    ) -> str:
        """Determine the quality profile of fixes."""
        if completeness < 0.6:
            return "🚨 BANDAID FIXES - Just making errors disappear!"
        elif efficiency < 0.5:
            return "🏗️ OVER-ENGINEERED - Too complex for the problem!"
        elif robustness < 0.5:
            return "🎲 FRAGILE - No error handling or validation!"
        elif maintainability < 0.5:
            return "🔧 UNMAINTAINABLE - Hard to read or modify!"
        elif all(score > 0.8 for score in [completeness, robustness, maintainability, efficiency]):
            return "✨ EXCELLENT - High quality across all dimensions!"
        elif completeness > 0.8 and efficiency > 0.8:
            return "🎯 PRAGMATIC - Solid, practical fixes!"
        else:
            return "📊 BALANCED - Decent quality overall"