from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user or request.user.is_superuser:
            return True
        else:
            return False
