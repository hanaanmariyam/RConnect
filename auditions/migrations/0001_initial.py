from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial=True
    dependencies=[('accounts','0001_initial'),('clubs','0001_initial')]
    operations=[
        migrations.CreateModel(name='Audition',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=200)),('description',models.TextField()),
            ('date',models.DateField()),('time',models.TimeField()),('venue',models.CharField(max_length=200)),('application_deadline',models.DateTimeField()),('eligibility',models.TextField(blank=True)),('vacancies',models.PositiveIntegerField(default=1)),
            ('status',models.CharField(choices=[('OPEN','Open'),('CLOSED','Closed'),('COMPLETED','Completed'),('CANCELLED','Cancelled')],default='OPEN',max_length=20)),('created_at',models.DateTimeField(auto_now_add=True)),
            ('club',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='auditions',to='clubs.club'))]),
        migrations.CreateModel(name='AuditionApplication',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('applied_at',models.DateTimeField(auto_now_add=True)),('status',models.CharField(choices=[('PENDING','Pending'),('SELECTED','Selected'),('REJECTED','Rejected')],default='PENDING',max_length=10)),('reviewed_at',models.DateTimeField(blank=True,null=True)),
            ('audition',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='applications',to='auditions.audition')),
            ('reviewed_by',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='reviewed_audition_applications',to=settings.AUTH_USER_MODEL)),
            ('student',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='audition_applications',to=settings.AUTH_USER_MODEL))]),
        migrations.AddConstraint(model_name='auditionapplication',constraint=models.UniqueConstraint(fields=('student','audition'),name='unique_audition_application')),
    ]
