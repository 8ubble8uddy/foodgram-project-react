from rest_framework import permissions

ALLOWED_ACTIONS = [
    'list',
    'create',
    'retrieve',
    'me',
    'set_password',
    'subscribe',
    'subscriptions',
    ]


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['me', 'subscriptions']:
            return (
                request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated
                )
        return view.action in ALLOWED_ACTIONS

    def has_object_permission(self, request, view, obj):
        if view.action == 'subscribe':
            return request.user.is_authenticated
        return request.method in permissions.SAFE_METHODS


class RecipePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'download_shopping_cart':
            return request.user.is_authenticated
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        if view.action in ['favorite', 'shopping_cart']:
            return request.user.is_authenticated
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and obj.author == request.user)
            )
