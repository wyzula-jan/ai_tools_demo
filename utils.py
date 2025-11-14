"""
Utility functions for validating user input and working with the mock database.
"""
from collections import Counter
import json
from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "mock_users.json"


def is_email_valid(email: str) -> bool:
    """
    Checks if the provided email address is valid.

    Args:
        email(str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_strong_password(password: str) -> bool:
    """
    Checks if the provided password is strong.

    Args:
        password(str): The password to validate.

    Returns:
        bool: True if the password is strong, False otherwise.
    """
    return (len(password) >= 8 and
            any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in password))


def load_user_database(db_path: Optional[Path] = None) -> List[Dict]:
    """
    Loads the mock user database from disk.

    Args:
        db_path(Path, optional): Path to the JSON file. Defaults to DEFAULT_DB_PATH.

    Returns:
        list[dict]: Parsed user records.
    """
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def get_usage_summary(users: Iterable[Dict]) -> Dict[str, object]:
    """
    Builds aggregate usage information for the dashboard.

    Args:
        users(iterable[dict]): Collection of user records.

    Returns:
        dict: Summary data ready for display.
    """
    user_list = list(users)
    total_users = len(user_list)
    active_users = sum(1 for user in user_list if user.get("active"))
    total_logins = sum(user.get("login_count", 0) for user in user_list)
    roles = Counter(user.get("role", "Unknown") for user in user_list)
    average_logins = total_logins / total_users if total_users else 0
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "total_logins": total_logins,
        "average_logins": round(average_logins, 1),
        "roles": dict(roles.most_common())
    }
