class HyperionError(Exception):
    """Hyperion error"""

    pass


class HyperionUnauthorizedError(HyperionError):
    """Hyperion unauthroized error"""

    pass


class HyperionNotFoundError(HyperionError):
    """Hyperion not found error"""

    pass
