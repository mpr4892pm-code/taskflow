import re


PRIORITY_KEYWORDS = [
    "urgent",
    "asap",
    "whenever",
    "low priority"
]

DATE_PHRASES = [
    "today",
    "tomorrow",
    "next week",
    "next monday",
    "next tuesday",
    "next wednesday",
    "next thursday",
    "next friday",
    "next saturday",
    "next sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"
]


def parse_quick_add(text):

    lower_text = text.lower()

    # Priority
    if "urgent" in lower_text or "asap" in lower_text:
        priority = "high"

    elif (
        "whenever" in lower_text
        or "low priority" in lower_text
    ):
        priority = "low"

    else:
        priority = "medium"

    # Due date
    due_date_hint = None

    for phrase in DATE_PHRASES:
        if phrase in lower_text:
            due_date_hint = phrase
            break

    # Title
    title = text

    # Remove priority keywords
    for keyword in PRIORITY_KEYWORDS:
        title = re.sub(
            re.escape(keyword),
            "",
            title,
            flags=re.IGNORECASE
        )

    # Remove due date
    if due_date_hint:
        title = re.sub(
            re.escape(due_date_hint),
            "",
            title,
            flags=re.IGNORECASE
        )

    title = title.strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint
    }