from rest_framework import permissions

ALLOWED_ACTIONS = [
    'list',
    'create',
    'retrieve',
    'me',
    'set_password',
    ]


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'me':
            return (
                request.user.is_authenticated and
                request.method in permissions.SAFE_METHODS
                )
        return view.action in ALLOWED_ACTIONS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
