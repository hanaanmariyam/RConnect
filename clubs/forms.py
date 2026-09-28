from django import forms
from .models import Club, ClubMembership

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "description", "cover_image", "contact_email", "contact_phone", "meeting_day", "meeting_time"]

class MembershipForm(forms.ModelForm):
    class Meta:
        model = ClubMembership
        fields = ["status"]
