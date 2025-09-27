from __future__ import annotations

from typing import Iterable, Sequence

from django.contrib.auth.decorators import user_passes_test

# Role names managed via Django Groups
ROLE_ADMIN = "Admin"
ROLE_QC_INSPECTOR = "QC Inspector"
ROLE_PRODUCTION_MANAGER = "Production Manager"

DEFAULT_ROLES = [ROLE_ADMIN, ROLE_QC_INSPECTOR, ROLE_PRODUCTION_MANAGER]


def user_has_role(user, roles: Iterable[str]) -> bool:
    """Return True if the authenticated user belongs to any of the given roles.

    Superusers always pass.
    Roles are implemented as Django auth Groups by name.
    """
    if not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_superuser", False):
        return True
    return user.groups.filter(name__in=list(roles)).exists()


def role_required(roles: Sequence[str]):
    """Decorator to protect function-based views by role(s)."""
    return user_passes_test(lambda u: user_has_role(u, roles))


class RoleRequiredMixin:
    """Mixin for class-based views to restrict access by role(s).

    Example:
        class MyView(RoleRequiredMixin, View):
            allowed_roles = [ROLE_ADMIN, ROLE_PRODUCTION_MANAGER]
    """

    allowed_roles: Sequence[str] = ()

    def dispatch(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        from django.core.exceptions import PermissionDenied

        if not user_has_role(request.user, self.allowed_roles):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
