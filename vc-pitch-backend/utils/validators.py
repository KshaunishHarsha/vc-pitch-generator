"""
Input validation utilities
Located in: utils/validators.py
"""

import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import settings


def validate_idea(idea: str) -> tuple[bool, str]:
    """
    Validate the startup idea input
    Returns: (is_valid: bool, error_message: str)
    """
    
    # Check if empty
    if not idea or not idea.strip():
        return False, "Idea cannot be empty"
    
    # Check length
    if len(idea) < settings.MIN_IDEA_LENGTH:
        return False, f"Idea must be at least {settings.MIN_IDEA_LENGTH} characters"
    
    if len(idea) > settings.MAX_IDEA_LENGTH:
        return False, f"Idea must be under {settings.MAX_IDEA_LENGTH} characters"
    
    # Check for valid characters (basic check)
    if not any(c.isalnum() for c in idea):
        return False, "Idea must contain at least one alphanumeric character"
    
    return True, ""