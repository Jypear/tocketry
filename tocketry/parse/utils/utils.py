def _get_session():
    "Get session in a way to prevent circular imports"
    from tocketry import session

    return session
