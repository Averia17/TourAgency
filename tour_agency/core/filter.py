from rest_framework import filters


class CanViewOwnerOrAdminFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_staff or user.is_manager:
            return queryset
        return queryset.filter(user=request.user)
