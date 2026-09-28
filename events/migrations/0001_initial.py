from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [('accounts','0001_initial'), ('clubs','0001_initial')]
    operations = [
        migrations.CreateModel(name='CollegeUnion', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(default='College Union', max_length=100, unique=True)),
            ('description', models.TextField(blank=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('assigned_admin', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_union', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='Event', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('event_name', models.CharField(max_length=200)), ('description', models.TextField()), ('organizer', models.CharField(max_length=200)),
            ('date', models.DateField()), ('start_time', models.TimeField()), ('end_time', models.TimeField()), ('venue', models.CharField(max_length=200)),
            ('registration_deadline', models.DateTimeField()), ('poster', models.ImageField(blank=True, null=True, upload_to='events/')),
            ('event_type', models.CharField(choices=[('WORKSHOP','Workshop'),('SEMINAR','Seminar'),('COMPETITION','Competition'),('CULTURAL','Cultural Event'),('IT','IT Event'),('SPORTS','Sports Event'),('OTHER','Other')], default='OTHER', max_length=20)),
            ('status', models.CharField(choices=[('UPCOMING','Upcoming'),('ONGOING','Ongoing'),('COMPLETED','Completed'),('CANCELLED','Cancelled')], default='UPCOMING', max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='clubs.club')),
            ('union', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.collegeunion')),
        ]),
        migrations.CreateModel(name='EventRegistration', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('registered_at', models.DateTimeField(auto_now_add=True)), ('status', models.CharField(choices=[('PENDING','Pending'),('APPROVED','Approved'),('REJECTED','Rejected')], default='PENDING', max_length=10)),
            ('reviewed_at', models.DateTimeField(blank=True, null=True)),
            ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='events.event')),
            ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_event_registrations', to=settings.AUTH_USER_MODEL)),
            ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.AddConstraint(model_name='eventregistration', constraint=models.UniqueConstraint(fields=('student','event'), name='unique_event_registration')),
    ]
