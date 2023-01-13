from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from home.models import CustomUser, Education, WorkPlace


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "additional_name",
                    "slug",
                    "overview",
                    "email",
                    "mobile_no",
                    "country",
                    "city",
                    "gender",
                    "status",
                    "allowed",
                    "date_of_birth",
                    "occupation",
                    "profile_pic",
                    "cover_pic",
                    "is_verified",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": (
                "wide",), "fields": (
                "password1", "password2"), },), )
    list_display = [
        "first_name",
        "last_name",
        "email",
        'username',
        'country',
        'date_joined',
        'last_login',
        "is_superuser",
        'is_staff',
    ]
    ordering = ("first_name", "last_name","username")
    list_display_links = ["first_name", "email"]
    autocomplete_fields = ["country"]
    list_select_related = ["country"]
    list_filter = ["date_joined", "gender"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date","created_at", "updated_at"]
    date_hierarchy = "start_date"
    search_fields = ["name", "user__username", "user__email"]
    autocomplete_fields = ["user"]
    list_filter = ("start_date", "end_date")


@admin.register(WorkPlace)
class WorkPlaceAdmin(admin.ModelAdmin):
    list_display = ["name", "date_range", "duration"]
    readonly_fields = ["duration"]
    date_hierarchy = "start_date"
    search_fields = ["name"]
    search_fields = ["name", "user__username", "user__email"]
    autocomplete_fields = ["user"]
    list_filter = ("start_date","end_date")