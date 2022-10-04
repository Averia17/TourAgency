from rest_framework.permissions import IsAuthenticated, BasePermission


class IsOwnerOrManager(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user or request.user.is_manager or request.user.is_staff
        )


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_manager
            or request.user.is_staff
        )
