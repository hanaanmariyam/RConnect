from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.decorators import role_required
from accounts.models import User
from auditions.models import Audition
from core.models import GalleryImage
from events.models import Event
from .models import Club, ClubMembership
from .forms import ClubForm

def club_list(request):
    return render(request, "clubs/list.html", {"clubs": Club.objects.all()})

def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    return render(request, "clubs/detail.html", {
        "club": club,
        "achievements": club.achievements.select_related("club").order_by("-date"),
        "events": Event.objects.filter(club=club).order_by("date", "start_time"),
        "auditions": Audition.objects.filter(club=club).order_by("date", "time"),
        "gallery_images": GalleryImage.objects.filter(club=club).order_by("-uploaded_at"),
    })

@login_required
@role_required(User.Roles.CLUB_ADMIN)
def admin_dashboard(request):
    club = request.user.managed_club
    from events.models import Event, EventRegistration
    from auditions.models import AuditionApplication
    context = {
        "club": club,
        "member_count": club.memberships.filter(status="ACTIVE").count(),
        "upcoming_events": Event.objects.filter(club=club).exclude(status="CANCELLED").order_by("date")[:5],
        "pending_auditions": AuditionApplication.objects.filter(audition__club=club, status="PENDING").count(),
        "pending_registrations": EventRegistration.objects.filter(event__club=club, status="PENDING").count(),
    }
    return render(request, "dashboards/club_admin.html", context)

@login_required
@role_required(User.Roles.CLUB_ADMIN)
def my_club(request):
    club = request.user.managed_club
    form = ClubForm(request.POST or None, request.FILES or None, instance=club)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Club details updated.")
        return redirect("clubs:my_club")
    return render(request, "clubs/manage.html", {"club": club, "form": form})

@login_required
@role_required(User.Roles.CLUB_ADMIN)
def members(request):
    club = request.user.managed_club
    return render(request, "clubs/members.html", {"club": club, "members": club.memberships.select_related("student")})
