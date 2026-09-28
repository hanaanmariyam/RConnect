from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, label="Full Name")
    email = forms.EmailField()
    student_id = forms.CharField(max_length=50, label="Student ID / Register Number")
    phone = forms.CharField(max_length=20)
    course = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    year = forms.IntegerField(min_value=1, max_value=10)
    semester = forms.IntegerField(min_value=1, max_value=20)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "email", "password1", "password2", "student_id",
                  "phone", "course", "department", "year", "semester", "profile_photo"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_student_id(self):
        value = self.cleaned_data["student_id"].strip()
        if User.objects.filter(student_id__iexact=value).exists():
            raise forms.ValidationError("This Student ID is already registered.")
        return value

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"].lower()
        user.role = User.Roles.STUDENT
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "student_id", "phone", "course",
                  "department", "year", "semester", "profile_photo"]
        widgets = {"email": forms.EmailInput(attrs={"readonly": "readonly"})}
