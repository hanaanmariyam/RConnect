from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class RConnectUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "role", "student_id", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "student_id")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("RConnect Profile", {"fields": ("role", "student_id", "phone", "course", "department", "year", "semester", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("RConnect Profile", {"fields": ("email", "role", "student_id", "phone", "course", "department", "year", "semester")}),
    )
