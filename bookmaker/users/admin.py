from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "is_staff",
        "is_active",
        "last_login",
    ]
    list_filter = ["last_login", "is_staff"]
    search_fields = ["email"]
    readonly_fields = ["last_login", "created", "modified"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "password",
                    "is_active",
                    "last_login",
                ]
            },
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
