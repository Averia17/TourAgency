from django.contrib import admin

from orders.models import Order, OrderRoom


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "arrival_date", "user"]
    list_filter = ["user"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["arrival_date", "user", "price", "status", "count_tickets"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]


@admin.register(OrderRoom)
class OrderRoomAdmin(admin.ModelAdmin):
    list_display = ["order", "room"]
    list_filter = ["order", "room"]
    readonly_fields = ["created", "modified"]
    fieldsets = [
        (
            None,
            {"fields": ["order", "room", "start", "end", "user", "feature"]},
        ),
        ("System", {"classes": ["collapse"], "fields": ["created", "modified"]}),
    ]
