from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import RegisterForm, ProfileForm
from .models import User

def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    form = RegisterForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Registration successful. Welcome to RConnect!")
        return redirect("accounts:dashboard")
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    if request.method == "POST":
        from django.contrib.auth import authenticate
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("accounts:dashboard")
        messages.error(request, "Invalid email or password.")
    return render(request, "accounts/login.html")

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("core:home")

@login_required
def dashboard(request):
    if request.user.is_superuser or request.user.role == User.Roles.SUPER_ADMIN:
        return redirect("/admin/")
    if request.user.role == User.Roles.CLUB_ADMIN:
        return redirect("clubs:admin_dashboard")
    if request.user.role == User.Roles.UNION_ADMIN:
        return redirect("events:union_dashboard")
    return redirect("core:student_dashboard")

@login_required
def profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})
