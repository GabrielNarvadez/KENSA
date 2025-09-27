from __future__ import annotations

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms_admin_console import BulkUserRolesForm, GroupForm, UserRolesForm
from django.contrib.auth import get_user_model

User = get_user_model()


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_superuser)(view_func)


@superuser_required
def console_dashboard(request):
    ctx = {
        "users_count": User.objects.count(),
        "groups_count": Group.objects.count(),
        "perms_count": Permission.objects.count(),
    }
    return render(request, "admin_console/dashboard.html", ctx)


@superuser_required
def groups_list(request):
    groups = Group.objects.order_by("name")
    return render(request, "admin_console/groups_list.html", {"groups": groups})


@superuser_required
def group_create(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_console:groups_list")
    else:
        form = GroupForm()
    return render(request, "admin_console/group_form.html", {"form": form, "title": "Create Role"})


@superuser_required
def group_edit(request, pk: int):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("admin_console:groups_list")
    else:
        form = GroupForm(instance=group)
    return render(request, "admin_console/group_form.html", {"form": form, "title": f"Edit Role: {group.name}"})


@superuser_required
def group_delete(request, pk: int):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        group.delete()
        return redirect("admin_console:groups_list")
    return render(request, "admin_console/group_confirm_delete.html", {"group": group})


@superuser_required
def users_list(request):
    q = request.GET.get("q", "").strip()
    qs = User.objects.order_by("id")
    if q:
        qs = qs.filter(email__icontains=q) | qs.filter(name__icontains=q)
    paginator = Paginator(qs, 25)
    page = request.GET.get("page")
    users_page = paginator.get_page(page)
    bulk_form = BulkUserRolesForm()
    groups = Group.objects.order_by("name").all()
    return render(
        request,
        "admin_console/users_list.html",
        {"users": users_page, "q": q, "bulk_form": bulk_form, "perms_list": groups},
    )


@superuser_required
def user_roles_edit(request, pk: int):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserRolesForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("admin_console:users_list")
    else:
        form = UserRolesForm(instance=user)
    return render(request, "admin_console/user_roles_form.html", {"form": form, "user": user})


@superuser_required
@transaction.atomic
def users_bulk_roles(request):
    if request.method == "POST":
        form = BulkUserRolesForm(request.POST)
        if form.is_valid():
            ids = [int(x) for x in form.cleaned_data["user_ids"].split(",") if x]
            groups = list(form.cleaned_data["groups"])
            for uid in ids:
                u = User.objects.filter(pk=uid).first()
                if not u:
                    continue
                u.groups.set(groups)
            return redirect("admin_console:users_list")
    return redirect("admin_console:users_list")
