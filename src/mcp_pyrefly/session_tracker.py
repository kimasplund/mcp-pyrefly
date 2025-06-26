"""Session-based identifier tracking for consistency validation."""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class IdentifierInfo:
    """Information about an identifier used in code."""
    name: str
    type: str  # function, variable, class, method, constant
    first_seen: datetime
    last_seen: datetime
    occurrences: int = 1
    signatures: List[str] = field(default_factory=list)
    file_locations: Set[str] = field(default_factory=set)
    

class SessionTracker:
    """Tracks identifiers and their usage patterns within a session."""
    
    def __init__(self):
        self.identifiers: Dict[str, IdentifierInfo] = {}
        self.similar_names: Dict[str, Set[str]] = {}
        
    def track_identifier(
        self, 
        name: str, 
        id_type: str, 
        signature: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> None:
        """Track an identifier usage."""
        if name in self.identifiers:
            info = self.identifiers[name]
            info.occurrences += 1
            info.last_seen = datetime.now()
            if signature and signature not in info.signatures:
                info.signatures.append(signature)
            if file_path:
                info.file_locations.add(file_path)
        else:
            self.identifiers[name] = IdentifierInfo(
                name=name,
                type=id_type,
                first_seen=datetime.now(),
                last_seen=datetime.now(),
                signatures=[signature] if signature else [],
                file_locations={file_path} if file_path else set()
            )
            self._update_similar_names(name)
    
    def _update_similar_names(self, name: str) -> None:
        """Update similar names mapping for consistency checking."""
        # Convert between naming conventions
        variations = self._get_name_variations(name)
        
        for var in variations:
            if var not in self.similar_names:
                self.similar_names[var] = set()
            self.similar_names[var].add(name)
            
            if name not in self.similar_names:
                self.similar_names[name] = set()
            self.similar_names[name].add(var)
    
    def _get_name_variations(self, name: str) -> Set[str]:
        """Get common variations of a name (camelCase, snake_case, etc.)."""
        variations = set()
        
        # camelCase to snake_case
        snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        variations.add(snake)
        
        # snake_case to camelCase
        if '_' in name:
            parts = name.split('_')
            camel = parts[0].lower() + ''.join(p.capitalize() for p in parts[1:])
            variations.add(camel)
            
            # PascalCase variant
            pascal = ''.join(p.capitalize() for p in parts)
            variations.add(pascal)
        
        # Handle common abbreviations
        if name.startswith('get_'):
            variations.add(name.replace('get_', 'fetch_'))
            variations.add(name.replace('get_', 'retrieve_'))
        elif name.startswith('get'):
            base = name[3:]
            variations.add(f'fetch{base}')
            variations.add(f'retrieve{base}')
            
        return variations - {name}  # Don't include the original
    
    def check_consistency(self, name: str) -> Optional[Dict]:
        """Check if a name might be inconsistent with existing identifiers."""
        # Direct match - it's consistent
        if name in self.identifiers:
            return None
            
        # Check for similar names that might be the same thing
        similar = self.similar_names.get(name, set())
        existing_similar = [n for n in similar if n in self.identifiers]
        
        if existing_similar:
            return {
                'warning': 'potential_inconsistency',
                'message': f'"{name}" might be inconsistent with existing identifier(s)',
                'existing': existing_similar,
                'suggestion': existing_similar[0]  # Suggest the first match
            }
            
        return None
    
    def get_identifier_info(self, name: str) -> Optional[IdentifierInfo]:
        """Get information about a tracked identifier."""
        return self.identifiers.get(name)
    
    def list_identifiers(self, id_type: Optional[str] = None) -> List[IdentifierInfo]:
        """List all tracked identifiers, optionally filtered by type."""
        if id_type:
            return [info for info in self.identifiers.values() if info.type == id_type]
        return list(self.identifiers.values())
    
    def clear(self) -> None:
        """Clear all tracked identifiers."""
        self.identifiers.clear()
        self.similar_names.clear()