from django.urls import path
from . import views
app_name="core"
urlpatterns=[
 path("",views.home,name="home"),path("about/",views.about,name="about"),
 path("announcements/",views.announcements,name="announcements"),
 path("dashboard/student/",views.student_dashboard,name="student_dashboard"),
 path("notifications/",views.notifications,name="notifications"),
 path("notifications/<int:pk>/read/",views.mark_notification_read,name="mark_read"),
 path("notifications/read-all/",views.mark_all_read,name="mark_all_read"),
]
