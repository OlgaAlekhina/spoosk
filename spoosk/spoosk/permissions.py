from rest_framework import permissions


# get permission to API by api key
class APIkey(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            api_key = request.META['HTTP_API_KEY']
            if api_key == '6351f035a4db9598952a6705330b29a30ff5fb35':
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