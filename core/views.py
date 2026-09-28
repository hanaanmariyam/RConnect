from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from clubs.models import Club
from .models import Announcement, Achievement, GalleryImage, Notification
from events.models import Event
from auditions.models import Audition, AuditionApplication

def home(request):
    return render(request,"home.html",{
        "gallery_images": GalleryImage.objects.select_related("club", "union", "event").order_by("-uploaded_at"),
        "announcements": Announcement.objects.filter(is_active=True).order_by("-created_at")[:5],
        "achievements": Achievement.objects.select_related("club", "student").order_by("-date")[:6],
        "events": Event.objects.filter(status="UPCOMING").select_related("club", "union").order_by("date", "start_time")[:6],
        "auditions": Audition.objects.filter(status="OPEN").select_related("club").order_by("date", "time")[:6],
        "clubs": Club.objects.all().order_by("name"),
    })
def about(request): return render(request,"about.html")
def announcements(request): return render(request,"core/announcements.html",{"announcements":Announcement.objects.filter(is_active=True)})
@login_required
def student_dashboard(request):
    memberships=request.user.club_memberships.select_related("club").filter(status="ACTIVE")
    upcoming_events=Event.objects.filter(status="UPCOMING").select_related("club", "union").order_by("date", "start_time")
    open_auditions=Audition.objects.filter(status="OPEN").select_related("club").order_by("date", "time")
    announcements_qs=Announcement.objects.filter(is_active=True).order_by("-created_at")
    return render(request,"dashboards/student.html",{
        "memberships":memberships,
        "pending_auditions":AuditionApplication.objects.filter(student=request.user,status="PENDING").count(),
        "registered_events":request.user.event_registrations.filter(status="APPROVED").select_related("event").order_by("event__date")[:5],
        "unread_notifications":request.user.notifications.filter(is_read=False).count(),
        "announcements":announcements_qs[:5],
        "achievements":request.user.achievements.order_by("-date")[:5],
        "upcoming_events":upcoming_events[:4], "upcoming_events_count":upcoming_events.count(),
        "open_auditions":open_auditions[:4], "open_auditions_count":open_auditions.count(),
        "club_count":Club.objects.count(), "announcement_count":announcements_qs.count(),
        "clubs":Club.objects.all().order_by("name")[:4],
    })
@login_required
def notifications(request):
    qs=request.user.notifications.all()
    return render(request,"core/notifications.html",{"notifications":qs})
@login_required
def mark_notification_read(request,pk):
    n=get_object_or_404(Notification,pk=pk,recipient=request.user); n.is_read=True; n.save(update_fields=["is_read"])
    return redirect("core:notifications")
@login_required
def mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect("core:notifications")
