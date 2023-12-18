from rest_framework import permissions


class APIkey(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            api_key = request.META['HTTP_API_KEY']
            print(api_key)
            if api_key == '6351f035a4db9598952a6705330b29a30ff5fb35':
                return True
        except:
            return False