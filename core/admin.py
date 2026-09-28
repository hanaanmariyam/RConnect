from django.contrib import admin
from .models import Notification, Announcement, Achievement, GalleryImage
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display=("recipient","title","notification_type","is_read","created_at")
    list_filter=("notification_type","is_read")
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display=("title","club","union","is_active","created_at")
    list_filter=("is_active","club","union")
    search_fields=("title","content")
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display=("title","date","club","student")
    list_filter=("club",)
@admin.register(GalleryImage)
class GalleryAdmin(admin.ModelAdmin):
    list_display=("caption","club","union","event","uploaded_at")
    list_filter=("club","union")
