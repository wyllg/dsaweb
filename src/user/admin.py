from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, Organization

class UserAdmin(BaseUserAdmin):
    list_display = ("username", "sr_code", "is_organization", "is_staff")
    list_filter = ("is_organization", "is_staff", "is_superuser")
    search_fields = ("username", "sr_code")

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("sr_code", "is_organization")}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("organization_name", "organization_level", "user")

    readonly_fields = ("followers_list",)

    def followers_list(self, obj):
        return ", ".join([u.sr_code for u in obj.followers.all()])
    followers_list.short_description = "Current Followers"

    # Limit the User dropdown to only organization accounts
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_organization=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Limit the followers dropdown to only students
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "followers":
            kwargs["queryset"] = User.objects.filter(is_organization=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Organization, OrganizationAdmin)
