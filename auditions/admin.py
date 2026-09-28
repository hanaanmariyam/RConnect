from django.contrib import admin
from .models import Audition, AuditionApplication
@admin.register(Audition)
class AuditionAdmin(admin.ModelAdmin):
    list_display=("title","club","date","application_deadline","status","vacancies")
    list_filter=("status","club")
    search_fields=("title","club__name")
@admin.register(AuditionApplication)
class AuditionApplicationAdmin(admin.ModelAdmin):
    list_display=("student","audition","status","applied_at","reviewed_by")
    list_filter=("status",)
    search_fields=("student__email","audition__title")
