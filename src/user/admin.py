from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, Organization, OrganizationOfficer

# Custom UserAdmin
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "sr_code", "is_organization", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("sr_code", "is_organization")}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile)
admin.site.register(Organization)
admin.site.register(OrganizationOfficer)
