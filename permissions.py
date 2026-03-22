"""
users/permissions.py

Custom DRF permission classes for role-based access control (RBAC).

Classes:
    IsAdminRole         — grants access only to users with role == 'admin'
    IsOwnerOrAdminRole  — grants access to the object owner OR any admin
    IsCustomerRole      — grants access only to users with role == 'customer'

These operate at the application level, separate from Django's
is_staff / is_superuser flags which control /admin/ access.

Usage in views:
    permission_classes = [IsAuthenticated, IsAdminRole]
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminRole(BasePermission):
    """
    Allow access only to authenticated users whose role is 'admin'.

    Used on:
        - Admin product management (create / update / delete)
        - Admin order management (update status)
        - Admin dashboard stats
        - Admin user list / detail
    """

    message = "Access restricted to administrators only."

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsOwnerOrAdminRole(BasePermission):
    """
    Object-level permission.

    Allow access if:
        - The requesting user is authenticated AND is an admin, OR
        - The requesting user is authenticated AND owns the object.

    "Ownership" is determined by comparing request.user to the object's
    .user attribute.  The model must expose obj.user (a FK to AUTH_USER_MODEL).

    Used on:
        - Order detail (customer can read own order, admin reads all)
    """

    message = "You do not have permission to access this resource."

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.role == "admin":
            return True
        owner = getattr(obj, "user", None)
        return owner == request.user


class IsCustomerRole(BasePermission):
    """
    Allow access only to authenticated users whose role is 'customer'.

    Useful if a future endpoint should be blocked from admin accounts
    (e.g., preventing admins from placing orders themselves while testing).
    Currently defined for completeness; not required by the spec.
    """

    message = "Access restricted to customer accounts."

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "customer"
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Allow safe (GET, HEAD, OPTIONS) requests to everyone.
    Restrict write operations (POST, PUT, PATCH, DELETE) to admins only.

    Used on:
        - Product listing endpoints where anonymous users can browse
          but only admins can modify.
    """

    message = "Write access is restricted to administrators only."

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )
