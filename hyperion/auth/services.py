"""Auth services"""
from functools import wraps
from flask import g

from hyperion.exceptions import HyperionUnauthorizedError


def permission_required(permission):
    """Check for permission"""

    def _permission_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """Decorated function"""
            if not g.current_user.can(permission):
                return HyperionUnauthorizedError("No permissions")

            return f(*args, **kwargs)

        return decorated_function

    return _permission_required


def auth_required(f):
    """User authentication"""

    @wraps(f)
    def _auth_required(*args, **kwargs):
        g.current_user = "TODO: My current user object"
        f(*args, **kwargs)

    return _auth_required
