from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from clubs.models import Club

class CollegeUnion(models.Model):
    name = models.CharField(max_length=100, unique=True, default="College Union")
    description = models.TextField(blank=True)
    assigned_admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_union")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Event(models.Model):
    class Types(models.TextChoices):
        WORKSHOP="WORKSHOP","Workshop"; SEMINAR="SEMINAR","Seminar"; COMPETITION="COMPETITION","Competition"
        CULTURAL="CULTURAL","Cultural Event"; IT="IT","IT Event"; SPORTS="SPORTS","Sports Event"; OTHER="OTHER","Other"
    class Status(models.TextChoices):
        UPCOMING="UPCOMING","Upcoming"; ONGOING="ONGOING","Ongoing"; COMPLETED="COMPLETED","Completed"; CANCELLED="CANCELLED","Cancelled"
    event_name = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.CharField(max_length=200)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True, related_name="events")
    union = models.ForeignKey(CollegeUnion, on_delete=models.CASCADE, null=True, blank=True, related_name="events")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200)
    registration_deadline = models.DateTimeField()
    poster = models.ImageField(upload_to="events/", blank=True, null=True)
    event_type = models.CharField(max_length=20, choices=Types.choices, default=Types.OTHER)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPCOMING)
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if bool(self.club) == bool(self.union):
            raise ValidationError("An event must belong to exactly one club or the College Union.")
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
    @property
    def organizer_name(self):
        return self.club.name if self.club else self.union.name
    def __str__(self): return self.event_name

class EventRegistration(models.Model):
    class Status(models.TextChoices):
        PENDING="PENDING","Pending"; APPROVED="APPROVED","Approved"; REJECTED="REJECTED","Rejected"
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_event_registrations")
    class Meta:
        constraints = [models.UniqueConstraint(fields=["student","event"], name="unique_event_registration")]
    def clean(self):
        if self.pk is None:
            if self.event.status == Event.Status.CANCELLED:
                raise ValidationError("Registration is closed for cancelled events.")
            if timezone.now() > self.event.registration_deadline:
                raise ValidationError("The registration deadline has passed.")
    def __str__(self): return f"{self.student} - {self.event}"
