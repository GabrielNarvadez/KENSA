from __future__ import annotations

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .roles import DEFAULT_ROLES, ROLE_ADMIN, ROLE_PRODUCTION_MANAGER, ROLE_QC_INSPECTOR


def get_model_perms(app_label: str, model_names: list[str]) -> list[Permission]:
    perms: list[Permission] = []
    for model_name in model_names:
        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            continue
        ct = ContentType.objects.get_for_model(model)
        perms.extend(Permission.objects.filter(content_type=ct))
    return perms


@receiver(post_migrate)
def ensure_default_roles(sender, **kwargs):  # type: ignore[no-untyped-def]
    # Create groups if missing
    for role in DEFAULT_ROLES:
        Group.objects.get_or_create(name=role)

    # Assign default permissions per role
    # Admin: all permissions on pages app models
    admin_group = Group.objects.get(name=ROLE_ADMIN)
    if admin_group.permissions.count() == 0:
        all_pages_perms = get_model_perms("pages", [
            "SteelSheet",
            "SteelSheetInspection",
            "ScanLog",
        ])
        admin_group.permissions.add(*all_pages_perms)

    # QC Inspector: manage inspections, view sheets and scan logs
    inspector_group = Group.objects.get(name=ROLE_QC_INSPECTOR)
    if inspector_group.permissions.count() == 0:
        inspector_perms = []
        inspector_perms += [
            p for p in get_model_perms("pages", ["SteelSheetInspection"]) if p.codename.startswith(("add_", "change_", "delete_", "view_"))
        ]
        inspector_perms += [
            p for p in get_model_perms("pages", ["SteelSheet"]) if p.codename.startswith("view_")
        ]
        inspector_perms += [
            p for p in get_model_perms("pages", ["ScanLog"]) if p.codename.startswith("view_")
        ]
        inspector_group.permissions.add(*inspector_perms)

    # Production Manager: manage steel sheets, view scan logs and inspections
    manager_group = Group.objects.get(name=ROLE_PRODUCTION_MANAGER)
    if manager_group.permissions.count() == 0:
        manager_perms = []
        manager_perms += [
            p for p in get_model_perms("pages", ["SteelSheet"]) if p.codename.startswith(("add_", "change_", "delete_", "view_"))
        ]
        manager_perms += [
            p for p in get_model_perms("pages", ["ScanLog", "SteelSheetInspection"]) if p.codename.startswith("view_")
        ]
        manager_group.permissions.add(*manager_perms)
