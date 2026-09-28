from django.contrib import admin
from .models import Club, ClubMembership
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "assigned_admin", "contact_email", "created_at")
    search_fields = ("name", "description", "contact_email")
@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ("student", "club", "status", "joined_date")
    list_filter = ("status", "club")
    search_fields = ("student__email", "student__student_id", "club__name")
