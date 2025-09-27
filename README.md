# reback

A fully responsive premium admin dashboard template

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a normal user account, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a superuser account, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy reback

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Custom Bootstrap Compilation

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v5 is installed using npm and customised by tweaking your variables in `static/sass/custom_bootstrap_vars`.

You can find a list of available variables in the bootstrap source, or get explanations on them in the Bootstrap docs.

Bootstrap's javascript as well as its dependencies are concatenated into a single file: `static/js/vendors.js`.

---

## User Roles and Access Control

Overview
- Authentication is provided by django-allauth.
- Authorization uses Django’s built-in permissions and Groups (roles). Views and menus enforce permissions, so admins can add/modify/remove roles without code changes.
- Post-login redirect is set to the dashboard: LOGIN_REDIRECT_URL = "pages:dashboard".

Default roles (auto-created)
- Admin: Full access to SteelSheet, SteelSheetInspection, and ScanLog (all model permissions).
- QC Inspector: Manage inspections; view steel sheets and scan logs.
- Production Manager: Manage steel sheets; view inspections and scan logs.
- These are created/seeded in reback/users/signals.py on post_migrate. Seeding adds permissions only if the group has none (won’t overwrite manual changes).

Setup
- python manage.py migrate
- python manage.py createsuperuser
- Sign in to /admin → Authentication and Authorization:
  - Groups: Create new roles or adjust permissions for existing roles.
  - Users: Assign users to groups.

Key permissions enforced by views
- Steel sheets
  - List/Detail: pages.view_steelsheet
  - Create: pages.add_steelsheet
  - Edit: pages.change_steelsheet
  - Delete: pages.delete_steelsheet
- Inspections
  - List: pages.view_steelsheetinspection
  - Create: pages.add_steelsheetinspection
  - Edit: pages.change_steelsheetinspection
  - Delete: pages.delete_steelsheetinspection
- Scan logs
  - List/Detail: pages.view_scanlog
  - Edit: pages.change_scanlog
  - Delete: pages.delete_scanlog

Navigation visibility
- Menu items are shown/hidden based on the current user’s permissions or staff/superuser flags. See reback/templates/partials/main-nav.html for the conditions.

Adding a new role
- Create a Group in /admin → Groups.
- Assign the desired model permissions to that Group.
- Add users to that Group. They immediately inherit those permissions across views and menus.

Notes
- Database defaults to SQLite in config/settings/base.py; adapt DATABASES in environment-specific settings as needed.
- If you later change the redirect target, update LOGIN_REDIRECT_URL in settings.

---

## Changelog (2025-09-27)

- RBAC enforcement across views using Django permissions (pages app): add/view/change/delete are required per feature.
- Default roles via Groups auto-seeded on post_migrate (Admin, QC Inspector, Production Manager) with sensible permissions.
- Super Admin Console (/super-admin/):
  - Dashboard, Role CRUD with permission editing, Users list with inline roles and bulk assignment.
  - Superuser-only access; integrated with site layout (sidebar/topbar).
  - Sidebar “Users & Roles” now routes to /super-admin/; removed old “Super Admin Console” button.
- User profiles:
  - Extended User model with avatar, title, phone, bio; profile edit supports file upload.
  - Navbar avatar displays uploaded image; profile pages use site layout.
- Account pages layout:
  - /accounts/email/ and /accounts/2fa/ now use the standard layout (navbar + sidebar) via account/base.html and mfa/base.html.
- Sidebar Admin section visibility restricted to the “Admin” Group using roles_extras template tag; library registered in settings.
