from django import forms
from .models import Audition
class AuditionForm(forms.ModelForm):
    application_deadline=forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type":"datetime-local"}))
    class Meta:
        model=Audition
        fields=["title","description","date","time","venue","application_deadline","eligibility","vacancies","status"]
        widgets={"date":forms.DateInput(attrs={"type":"date"}),"time":forms.TimeInput(attrs={"type":"time"})}
