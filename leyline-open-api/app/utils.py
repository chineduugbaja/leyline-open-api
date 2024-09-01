import re

"""
Utility functions for the application.
"""

def validate_ipv4(ip):
    """
    Validates whether the provided string is a valid IPv4 address.

    Args:
        ip_address (str): The IP address to validate.

    Returns:
        bool: True if valid IPv4 address, False otherwise.
    """
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None
