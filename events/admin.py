from django.contrib import admin
from .models import CollegeUnion, Event, EventRegistration
@admin.register(CollegeUnion)
class CollegeUnionAdmin(admin.ModelAdmin):
    list_display=("name","assigned_admin","created_at")
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=("event_name","organizer","date","event_type","status","registration_deadline")
    search_fields=("event_name","description","venue")
    list_filter=("event_type","status","date")
@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display=("student","event","status","registered_at","reviewed_by")
    list_filter=("status",)
    search_fields=("student__email","event__event_name")
