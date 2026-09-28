from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def create_initial_organization_data(apps, schema_editor):
    Club = apps.get_model("clubs", "Club")
    Club.objects.get_or_create(name="Dance Club")
    Club.objects.get_or_create(name="Music Club")
    Club.objects.get_or_create(name="C-Star", defaults={"description": "C-Star is the Computer Students Association of Rajagiri. It organizes and coordinates MCA co-curricular activities with faculty guidance. The association conducts seminars, workshops, industry interaction programmes and activities related to the latest technologies. It also organizes in-house quizzes and cultural events, participates in college functions and cultural programmes, and facilitates student participation in inter-collegiate IT fests and competitions. Its hallmark event is the bi-annual national-level IT Fest, IT EUPHORIA."})
    Club.objects.get_or_create(name="Fashion Club")

class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name="Club",fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
            ("name",models.CharField(max_length=100,unique=True)),("description",models.TextField(blank=True)),
            ("cover_image",models.ImageField(blank=True,null=True,upload_to="clubs/")),
            ("contact_email",models.EmailField(blank=True,max_length=254)),("contact_phone",models.CharField(blank=True,max_length=20)),
            ("meeting_day",models.CharField(blank=True,max_length=30)),("meeting_time",models.TimeField(blank=True,null=True)),
            ("created_at",models.DateTimeField(auto_now_add=True)),
            ("assigned_admin",models.OneToOneField(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name="managed_club",to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="ClubMembership",fields=[
            ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
            ("joined_date",models.DateField(auto_now_add=True)),("status",models.CharField(choices=[("ACTIVE","Active"),("INACTIVE","Inactive")],default="ACTIVE",max_length=10)),
            ("created_at",models.DateTimeField(auto_now_add=True)),
            ("club",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="memberships",to="clubs.club")),
            ("student",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="club_memberships",to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.AddConstraint(model_name="clubmembership",constraint=models.UniqueConstraint(fields=("student","club"),name="unique_club_membership")),
        migrations.RunPython(create_initial_organization_data, migrations.RunPython.noop),
    ]
