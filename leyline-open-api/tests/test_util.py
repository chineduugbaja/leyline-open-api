def is_valid_ip(ip):
    """Check if the given IP address is valid."""
    import re
    pattern = re.compile(
        r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    )
    return pattern.match(ip) is not None
