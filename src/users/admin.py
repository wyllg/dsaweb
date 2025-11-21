from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Organization Info", {
            "fields": ("is_organization", "organization")
        }),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "user")
    search_fields = ("name",)
