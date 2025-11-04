from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin for Customer model."""
    list_display = ("email", "username", "full_name", "address")
    fields = ("username", "full_name", "email", "address", "user_cart")
    search_fields = ("email", "username", "full_name")
    ordering = ("email",)