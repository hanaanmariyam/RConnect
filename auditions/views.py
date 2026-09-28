from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from accounts.decorators import role_required
from accounts.models import User
from .models import Audition, AuditionApplication
from .forms import AuditionForm

def audition_list(request):
    return render(request,"auditions/list.html",{"auditions":Audition.objects.select_related("club").order_by("date","time")})
def audition_detail(request,pk):
    audition=get_object_or_404(Audition,pk=pk)
    applied=request.user.is_authenticated and AuditionApplication.objects.filter(student=request.user,audition=audition).exists()
    return render(request,"auditions/detail.html",{"audition":audition,"applied":applied})

@login_required
@role_required(User.Roles.STUDENT)
def apply(request,pk):
    audition=get_object_or_404(Audition,pk=pk)
    if AuditionApplication.objects.filter(student=request.user,audition=audition).exists():
        messages.info(request,"You have already applied.")
        return redirect("auditions:detail",pk=pk)
    try:
        obj=AuditionApplication(student=request.user,audition=audition); obj.full_clean(); obj.save()
    except Exception as e:
        messages.error(request,str(e))
        return redirect("auditions:detail",pk=pk)
    from core.models import Notification
    if audition.club.assigned_admin:
        Notification.objects.create(recipient=audition.club.assigned_admin,title="New audition application",message=f"{request.user.full_name} applied for {audition.title}.",notification_type="AUDITION")
    messages.success(request,"Application submitted.")
    return redirect("auditions:detail",pk=pk)

@login_required
@role_required(User.Roles.CLUB_ADMIN)
def manage(request):
    club=request.user.managed_club
    return render(request,"auditions/manage.html",{"auditions":Audition.objects.filter(club=club),"club":club})

@login_required
@role_required(User.Roles.CLUB_ADMIN)
def create(request):
    form=AuditionForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        obj=form.save(commit=False); obj.club=request.user.managed_club; obj.save()
        messages.success(request,"Audition created.")
        return redirect("auditions:manage")
    return render(request,"auditions/form.html",{"form":form,"title":"Create Audition"})

@login_required
@role_required(User.Roles.CLUB_ADMIN)
def applications(request):
    qs=AuditionApplication.objects.filter(audition__club=request.user.managed_club).select_related("student","audition")
    return render(request,"auditions/applications.html",{"applications":qs})

@login_required
@role_required(User.Roles.CLUB_ADMIN)
def review(request,pk):
    app=get_object_or_404(AuditionApplication,pk=pk,audition__club=request.user.managed_club)
    if request.method=="POST":
        status=request.POST.get("status")
        if status in ["SELECTED","REJECTED"]:
            app.status=status; app.reviewed_by=request.user; app.reviewed_at=timezone.now(); app.save()
            from core.models import Notification
            Notification.objects.create(recipient=app.student,title="Audition application updated",message=f"Your application for {app.audition.title} was {status.lower()}.",notification_type="AUDITION")
            if status=="SELECTED":
                from clubs.models import ClubMembership
                ClubMembership.objects.get_or_create(student=app.student,club=app.audition.club,defaults={"status":"ACTIVE"})
            messages.success(request,"Application reviewed.")
    return redirect("auditions:applications")
