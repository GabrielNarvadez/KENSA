from django.urls import path

from . import views_admin_console as views

app_name = "admin_console"

urlpatterns = [
    path("", views.console_dashboard, name="dashboard"),
    path("roles/", views.groups_list, name="groups_list"),
    path("roles/new/", views.group_create, name="group_create"),
    path("roles/<int:pk>/edit/", views.group_edit, name="group_edit"),
    path("roles/<int:pk>/delete/", views.group_delete, name="group_delete"),

    path("users/", views.users_list, name="users_list"),
    path("users/<int:pk>/roles/", views.user_roles_edit, name="user_roles_edit"),
    path("users/bulk-roles/", views.users_bulk_roles, name="users_bulk_roles"),
]
