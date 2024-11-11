from rest_framework import permissions
from .settings import API_KEY


# get permission to API by api key
class APIkey(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            api_key = request.META['HTTP_API_KEY']
            if api_key == API_KEY:
                return True
        except:
            return False


# get object permission for review author
class AuthorEditOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return False
            else:
                return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        return False


# permissions for PATCH, DELETE and change_password endpoints in users viewset
class UserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if view.action in ['partial_update', 'destroy', 'change_password']:
            return request.user.is_authenticated and obj == request.user

        return True