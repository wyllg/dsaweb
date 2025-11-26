from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, StudentProfile, Event

class StudentSignupForm(UserCreationForm):
    sr_code = forms.CharField(max_length=8, label="SR-Code")
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ("sr_code", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organization = False
        user.username = self.cleaned_data["sr_code"]
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
            )
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username / SR-Code")
    password = forms.CharField(widget=forms.PasswordInput)

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            "event_name",
            "start_datetime",
            "end_datetime",
            "location",
            "description",
            "header_image",
        ]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_start_datetime(self):
        dt = self.cleaned_data["start_datetime"]

        # Convert naive datetime (from datetime-local) → aware datetime
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())

        return dt

    def clean_end_datetime(self):
        dt = self.cleaned_data["end_datetime"]

        # Convert naive datetime (from datetime-local) → aware datetime
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())

        return dt

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_datetime")
        end = cleaned.get("end_datetime")

        # Validation: start must be before end
        if start and end and start > end:
            self.add_error("end_datetime", "End time must be after the start time.")

        return cleaned

