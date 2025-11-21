from django.contrib.auth.forms import UserCreationForm
from .models import User, Organization
# from django.contrib.auth.models import User
from django import forms

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input'})
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input'})
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'input'})
    )

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.filter(level=4),
        required=True,
        empty_label="Select your organization"
    )


    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'organization',
            'password1',
            'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'password1': forms.PasswordInput(attrs={'class': 'input'}),
            'password2': forms.PasswordInput(attrs={'class': 'input'}),
        }

    # class Meta:
    #     model = User
    #     fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    #     widgets = {
    #         'username': forms.TextInput(attrs={'class': 'input'}),
    #         'password1': forms.PasswordInput(attrs={'class': 'input'}),
    #         'password2': forms.PasswordInput(attrs={'class': 'input'}),
    #     }
