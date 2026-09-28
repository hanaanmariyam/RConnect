from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        CLUB_ADMIN = "CLUB_ADMIN", "Club Admin"
        UNION_ADMIN = "UNION_ADMIN", "Union Admin"
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)
    student_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    course = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    semester = models.PositiveIntegerField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Roles.SUPER_ADMIN
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return self.full_name
