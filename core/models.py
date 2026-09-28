from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from clubs.models import Club
from events.models import CollegeUnion, Event

class Notification(models.Model):
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications")
    title=models.CharField(max_length=200); message=models.TextField()
    notification_type=models.CharField(max_length=30,default="GENERAL")
    created_at=models.DateTimeField(auto_now_add=True); is_read=models.BooleanField(default=False)
    class Meta: ordering=["-created_at"]
    def __str__(self): return f"{self.recipient}: {self.title}"

class Announcement(models.Model):
    title=models.CharField(max_length=200); content=models.TextField()
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    club=models.ForeignKey(Club,on_delete=models.CASCADE,null=True,blank=True,related_name="announcements")
    union=models.ForeignKey(CollegeUnion,on_delete=models.CASCADE,null=True,blank=True,related_name="announcements")
    is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.club and self.union: raise ValidationError("Announcement cannot belong to both club and union.")
    def __str__(self): return self.title

class Achievement(models.Model):
    title=models.CharField(max_length=200); description=models.TextField()
    date=models.DateField(); image=models.ImageField(upload_to="achievements/",blank=True,null=True)
    club=models.ForeignKey(Club,on_delete=models.CASCADE,null=True,blank=True,related_name="achievements")
    student=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True,related_name="achievements")
    created_at=models.DateTimeField(auto_now_add=True)
    def clean(self):
        if bool(self.club)==bool(self.student): raise ValidationError("Achievement must belong to exactly one club or student.")
    def __str__(self): return self.title

class GalleryImage(models.Model):
    club=models.ForeignKey(Club,on_delete=models.CASCADE,null=True,blank=True,related_name="gallery")
    union=models.ForeignKey(CollegeUnion,on_delete=models.CASCADE,null=True,blank=True,related_name="gallery")
    event=models.ForeignKey(Event,on_delete=models.SET_NULL,null=True,blank=True,related_name="gallery")
    image=models.ImageField(upload_to="gallery/")
    caption=models.CharField(max_length=250,blank=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    def clean(self):
        if bool(self.club)==bool(self.union): raise ValidationError("Gallery image must belong to exactly one club or Union.")
    def __str__(self): return self.caption or f"Gallery image {self.pk}"
