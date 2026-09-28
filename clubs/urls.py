from django.urls import path
from . import views
app_name = "clubs"
urlpatterns = [
    path("", views.club_list, name="list"),
    path("<int:pk>/", views.club_detail, name="detail"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("my-club/", views.my_club, name="my_club"),
    path("members/", views.members, name="members"),
]
