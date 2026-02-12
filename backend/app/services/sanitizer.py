"""
Input sanitization service for LLM prompt injection defense.
"""

import re

def sanitize_guest_message(content: str) -> str:
    """
    Sanitize guest message before passing to LLM.
    1. Truncate to reasonable length (2000 chars).
    2. Strip potential prompt injection delimiters if they mimic system tags.
    """
    if not content:
        return ""
        
    # 1. Truncate
    max_len = 2000
    if len(content) > max_len:
        content = content[:max_len]
        
    # 2. Strip XML-like tags that might confuse the parser if we use XML tagging
    # We use <guest_message> tags in the prompt, so we should allow standard text but maybe escape or strip <>
    # For now, let's just replace strictly <guest_message> or <system> tags if they appear
    
    # Simple defense: replace < and > with safe chars or just strip known tags?
    # Better: just escape them in the final prompt construction, but here we can just do basic cleanup
    # Let's remove any pattern that looks like a closing XML tag matching our system tags
    
    content = re.sub(r"</?guest_message>", "", content, flags=re.IGNORECASE)
    content = re.sub(r"</?system>", "", content, flags=re.IGNORECASE)
    
    # 3. Strip known jailbreak patterns (simplistic but effective for script kiddies)
    jailbreak_patterns = [
        r"ignore previous instructions",
        r"ignore your instructions",
        r"reveal your system prompt",
        r"you are now DAN",
    ]
    
    for pattern in jailbreak_patterns:
        # Case insensitive replacement
        content = re.sub(pattern, "[REDACTED]", content, flags=re.IGNORECASE)
        
    return content.strip()
