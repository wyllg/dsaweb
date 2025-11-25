from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, StudentProfile, Organization

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
        user.username = self.cleaned_data["sr_code"]  # optional: login via SR-Code
        if commit:
            user.save()
            # Create the StudentProfile
            StudentProfile.objects.create(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
            )
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username / SR-Code")
    password = forms.CharField(widget=forms.PasswordInput)