from django.urls import path
from . import views
app_name="events"
urlpatterns=[
 path("",views.event_list,name="list"), path("<int:pk>/",views.event_detail,name="detail"),
 path("<int:pk>/register/",views.register_event,name="register"),
 path("manage/all/",views.manage_events,name="manage"), path("manage/create/",views.event_create,name="create"),
 path("manage/<int:pk>/edit/",views.event_edit,name="edit"), path("manage/<int:pk>/delete/",views.event_delete,name="delete"),
 path("registrations/all/",views.registrations,name="registrations"), path("registrations/<int:pk>/review/",views.review_registration,name="review_registration"),
 path("union/dashboard/",views.union_dashboard,name="union_dashboard"),
]
