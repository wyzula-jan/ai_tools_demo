"""
Utility functions for validating user input.
"""
import re


def is_email_valid(email):
    """
    Checks if the provided email address is valid.

    Args:
        email(str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
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