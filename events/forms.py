from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    registration_deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type":"datetime-local"}))
    class Meta:
        model = Event
        fields = ["event_name","description","organizer","club","union","date","start_time","end_time","venue","registration_deadline","poster","event_type","status"]
        widgets = {
            "date": forms.DateInput(attrs={"type":"date"}),
            "start_time": forms.TimeInput(attrs={"type":"time"}),
            "end_time": forms.TimeInput(attrs={"type":"time"}),
        }
    def clean(self):
        data = super().clean()
        if bool(data.get("club")) == bool(data.get("union")):
            raise ValidationError("Choose exactly one organizer: a club or the College Union.")
        if data.get("end_time") and data.get("start_time") and data["end_time"] <= data["start_time"]:
            raise ValidationError("End time must be after start time.")
        return data

class RegistrationReviewForm(forms.Form):
    status = forms.ChoiceField(choices=[("APPROVED","Approved"),("REJECTED","Rejected")])
