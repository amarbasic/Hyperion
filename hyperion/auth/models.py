"""Auth models"""
from enum import Enum

from sqlalchemy import Column, Integer, String
from hyperion.db import Base


class Permission(Enum):
    """Permissions"""

    Read = 1
    Create = 2
    Edit = 3
    Delete = 4


class PermissionObjects(Enum):
    """Permission objects"""

    Customer = 1


class Roles(Base):
    """Roles"""

    __tablename__ = "roles"

    name = Column(String(), required=True)


class RolePermissions(Base):
    """Role permissions"""

    __tablename__ = "role_permissions"

    role_id = Column(Integer())
    permission = Column(Integer())
