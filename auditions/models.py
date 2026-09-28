from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from clubs.models import Club

class Audition(models.Model):
    class Status(models.TextChoices):
        OPEN="OPEN","Open"; CLOSED="CLOSED","Closed"; COMPLETED="COMPLETED","Completed"; CANCELLED="CANCELLED","Cancelled"
    title=models.CharField(max_length=200)
    club=models.ForeignKey(Club,on_delete=models.CASCADE,related_name="auditions")
    description=models.TextField()
    date=models.DateField(); time=models.TimeField(); venue=models.CharField(max_length=200)
    application_deadline=models.DateTimeField()
    eligibility=models.TextField(blank=True)
    vacancies=models.PositiveIntegerField(default=1)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class AuditionApplication(models.Model):
    class Status(models.TextChoices):
        PENDING="PENDING","Pending"; SELECTED="SELECTED","Selected"; REJECTED="REJECTED","Rejected"
    student=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="audition_applications")
    audition=models.ForeignKey(Audition,on_delete=models.CASCADE,related_name="applications")
    applied_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)
    reviewed_at=models.DateTimeField(null=True,blank=True)
    reviewed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="reviewed_audition_applications")
    class Meta:
        constraints=[models.UniqueConstraint(fields=["student","audition"],name="unique_audition_application")]
    def clean(self):
        if self.pk is None:
            if self.audition.status != Audition.Status.OPEN: raise ValidationError("This audition is not open.")
            if timezone.now() > self.audition.application_deadline: raise ValidationError("The application deadline has passed.")
    def __str__(self): return f"{self.student} - {self.audition}"
