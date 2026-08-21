"""Clean and combine GitHub issue text for model training and inference."""

import re

BODY_TEMPLATE_PHRASES = ["WarningThis issue is not yet ready for a PR", 
                        "Describe the bug and give evidence about its user-facing impact",
                        "Describe the bug", 
                        "Describe the issue linked to the documentation",
                        "Describe the workflow you want to enable",
                        "Describe your proposed solution",
                        "Describe alternatives you've considered",
                        "Interest in fixing the bug"]

def clean_title(title):
    """Remove category-revealing prefixes from an issue title."""

    if not title:
        return ""

    pattern = r"^\s*(BUG|DOC|DOCS|ENH|FEATURE)\b[:\-\s]*"

    cleaned_title = re.sub(pattern, "", title, flags=re.IGNORECASE)

    return cleaned_title.strip()

def clean_body(body):
    """Remove category-revealing prefixes from an issue body."""

    if not body:
        return "" 

    for phrase in BODY_TEMPLATE_PHRASES:
        body = body.replace(phrase, "")

    return body.strip()


def build_text(issue):
    """Combine clean title + clean body."""

    title = clean_title(issue["title"])
    body = clean_body(issue["body"])
    return f"{title}\n\n{body}".strip()


