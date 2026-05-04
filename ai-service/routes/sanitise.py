import bleach
import re
from flask import request, jsonify

# Prompt injection patterns to detect
INJECTION_PATTERNS = [
    r"ignore all previous instructions",
    r"ignore prior instructions",
    r"disregard your instructions",
    r"forget your instructions",
    r"you are now",
    r"act as",
    r"pretend you are",
    r"jailbreak",
    r"dan mode",
    r"developer mode",
    r"bypass",
    r"override instructions",
]

def strip_html(text):
    """Remove all HTML tags from input text."""
    return bleach.clean(text, tags=[], strip=True)

def detect_prompt_injection(text):
    """Check if input contains prompt injection patterns."""
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True, pattern
    return False, None

def sanitise_input(text):
    """
    Full sanitisation pipeline:
    1. Check input exists
    2. Check length limit
    3. Strip HTML
    4. Detect prompt injection
    Returns: (clean_text, error_response)
    """
    # Check input exists
    if not text or not text.strip():
        return None, (jsonify({
            "error": "Input cannot be empty",
            "code": "EMPTY_INPUT"
        }), 400)

    # Check length limit
    if len(text) > 2000:
        return None, (jsonify({
            "error": "Input exceeds maximum length of 2000 characters",
            "code": "INPUT_TOO_LONG",
            "max_length": 2000,
            "received_length": len(text)
        }), 400)

    # Strip HTML tags
    clean_text = strip_html(text)

    # Detect prompt injection
    is_injection, pattern = detect_prompt_injection(clean_text)
    if is_injection:
        return None, (jsonify({
            "error": "Input contains disallowed content",
            "code": "PROMPT_INJECTION_DETECTED"
        }), 400)

    return clean_text, None