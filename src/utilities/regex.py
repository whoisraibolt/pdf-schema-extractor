import re
from typing import Dict, Any, Optional, List

def extract_fields_simple(text: str, schema: Dict[str, str]) -> Dict[str, Optional[str]]:
    extracted = {}
    for field, pattern in schema.items():
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        extracted[field] = match.group(1).strip() if match else None
    return extracted

def extract_fields_advanced(
    text: str,
    schema: Dict[str, List[str]],
    validators: Dict[str, Any] = None
) -> Dict[str, Optional[str]]:
    extracted = {}
    if validators is None:
        validators = {}
    for field, patterns in schema.items():
        value = None
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if match:
                candidate = match.group(1).strip()
                validator = validators.get(field, lambda x: True)
                if validator(candidate):
                    value = candidate
                    break
        extracted[field] = value
    return extracted