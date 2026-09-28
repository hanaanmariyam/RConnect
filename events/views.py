from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from accounts.decorators import role_required
from accounts.models import User
from .models import CollegeUnion, Event, EventRegistration
from .forms import EventForm, RegistrationReviewForm

def event_list(request):
    events = Event.objects.select_related("club","union").order_by("date","start_time")
    return render(request, "events/list.html", {"events": events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registered = request.user.is_authenticated and EventRegistration.objects.filter(student=request.user,event=event).exists()
    return render(request, "events/detail.html", {"event":event,"registered":registered})

@login_required
@role_required(User.Roles.STUDENT)
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.status == Event.Status.CANCELLED or timezone.now() > event.registration_deadline:
        messages.error(request, "Registration is closed for this event.")
        return redirect("events:detail", pk=pk)
    if EventRegistration.objects.filter(student=request.user,event=event).exists():
        messages.info(request, "You have already registered for this event.")
        return redirect("events:detail", pk=pk)
    registration = EventRegistration(student=request.user,event=event)
    registration.full_clean()
    registration.save()
    from core.models import Notification
    recipients = []
    if event.club and event.club.assigned_admin: recipients.append(event.club.assigned_admin)
    if event.union and event.union.assigned_admin: recipients.append(event.union.assigned_admin)
    for recipient in recipients:
        Notification.objects.create(recipient=recipient,title="New event registration",message=f"{request.user.full_name} registered for {event.event_name}.",notification_type="EVENT")
    messages.success(request, "Registration submitted. It is pending admin approval.")
    return redirect("events:detail", pk=pk)

@login_required
@role_required(User.Roles.CLUB_ADMIN, User.Roles.UNION_ADMIN)
def manage_events(request):
    if request.user.role == User.Roles.CLUB_ADMIN:
        events = Event.objects.filter(club=request.user.managed_club)
    else:
        events = Event.objects.filter(union=request.user.managed_union)
    return render(request, "events/manage.html", {"events":events})

@login_required
@role_required(User.Roles.CLUB_ADMIN, User.Roles.UNION_ADMIN)
def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        event = form.save(commit=False)
        if request.user.role == User.Roles.CLUB_ADMIN:
            event.club = request.user.managed_club; event.union = None
        else:
            event.union = request.user.managed_union; event.club = None
        event.organizer = event.club.name if event.club else event.union.name
        event.full_clean(); event.save()
        messages.success(request, "Event created successfully.")
        return redirect("events:manage")
    return render(request, "events/form.html", {"form":form,"title":"Create Event"})

@login_required
@role_required(User.Roles.CLUB_ADMIN, User.Roles.UNION_ADMIN)
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.role == User.Roles.CLUB_ADMIN and event.club_id != request.user.managed_club.id:
        messages.error(request,"Unauthorized.")
        return redirect("events:manage")
    if request.user.role == User.Roles.UNION_ADMIN and event.union_id != request.user.managed_union.id:
        messages.error(request,"Unauthorized.")
        return redirect("events:manage")
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if request.method=="POST" and form.is_valid():
        obj=form.save(commit=False)
        if request.user.role == User.Roles.CLUB_ADMIN: obj.club=request.user.managed_club; obj.union=None
        else: obj.union=request.user.managed_union; obj.club=None
        obj.organizer=obj.club.name if obj.club else obj.union.name
        obj.full_clean(); obj.save()
        messages.success(request,"Event updated.")
        return redirect("events:manage")
    return render(request,"events/form.html",{"form":form,"title":"Edit Event"})

@login_required
@role_required(User.Roles.CLUB_ADMIN, User.Roles.UNION_ADMIN)
def event_delete(request, pk):
    event=get_object_or_404(Event,pk=pk)
    allowed=(request.user.role==User.Roles.CLUB_ADMIN and event.club_id==request.user.managed_club.id) or (request.user.role==User.Roles.UNION_ADMIN and event.union_id==request.user.managed_union.id)
    if not allowed: return redirect("events:manage")
    if request.method=="POST": event.delete(); messages.success(request,"Event deleted.")
    return redirect("events:manage")

@login_required
@role_required(User.Roles.CLUB_ADMIN, User.Roles.UNION_ADMIN)
def registrations(request):
    if request.user.role == User.Roles.CLUB_ADMIN:
        qs=EventRegistration.objects.filter(event__club=request.user.managed_club).select_related("student","event")
    else:
        qs=EventRegistration.objects.filter(event__union=request.user.managed_union).select_related("student","event")
    return render(request,"events/registrations.html",{"registrations":qs,"review_form":RegistrationReviewForm()})

@login_required
@role_required(User.Roles.CLUB_ADMIN, User.Roles.UNION_ADMIN)
def review_registration(request, pk):
    reg=get_object_or_404(EventRegistration,pk=pk)
    allowed=(request.user.role==User.Roles.CLUB_ADMIN and reg.event.club_id==request.user.managed_club.id) or (request.user.role==User.Roles.UNION_ADMIN and reg.event.union_id==request.user.managed_union.id)
    if not allowed: return redirect("events:registrations")
    if request.method=="POST":
        status=request.POST.get("status")
        if status in ["APPROVED","REJECTED"]:
            reg.status=status; reg.reviewed_by=request.user; reg.reviewed_at=timezone.now(); reg.save()
            from core.models import Notification
            Notification.objects.create(recipient=reg.student,title="Event registration updated",message=f"Your registration for {reg.event.event_name} was {status.lower()}.",notification_type="EVENT")
            messages.success(request,"Registration reviewed.")
    return redirect("events:registrations")

@login_required
@role_required(User.Roles.UNION_ADMIN)
def union_dashboard(request):
    union=request.user.managed_union
    return render(request,"dashboards/union_admin.html",{"union":union,"events":union.events.order_by("date")[:5],"registrations":EventRegistration.objects.filter(event__union=union,status="PENDING").count()})
