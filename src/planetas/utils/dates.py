from datetime import datetime, timezone
from dateutil import parser


def parse_date(date_str: str) -> datetime:
    """
    Parse a date string into a datetime object (UTC).

    Supports formats:
    - YYYY-MM-DD
    - YYYY/MM/DD
    - DD-MM-YYYY
    - DD/MM/YYYY
    - YYYY-MM-DD HH:MM
    - YYYY-MM-DD HH:MM:SS
    - "today" (returns current UTC date at midnight)

    Args:
        date_str: Date string to parse.

    Returns:
        Datetime object (naive, assumed UTC).

    Raises:
        ValueError: If date string cannot be parsed.
    """
    if date_str.lower() == "today":
        now_utc = datetime.now(timezone.utc)
        return now_utc.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    return parser.parse(date_str)
