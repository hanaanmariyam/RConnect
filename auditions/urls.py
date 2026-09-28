from django.urls import path
from . import views
app_name="auditions"
urlpatterns=[
 path("",views.audition_list,name="list"),path("<int:pk>/",views.audition_detail,name="detail"),path("<int:pk>/apply/",views.apply,name="apply"),
 path("manage/all/",views.manage,name="manage"),path("manage/create/",views.create,name="create"),
 path("applications/all/",views.applications,name="applications"),path("applications/<int:pk>/review/",views.review,name="review"),
]
