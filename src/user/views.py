from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StudentSignupForm, UserLoginForm
from .models import User, StudentProfile, Organization

# Student Signup
def student_signup(request):
    if request.method == "POST":
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")  # change to your dashboard URL
    else:
        form = StudentSignupForm()
    return render(request, "signup.html", {"form": form})

# Login
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("landing")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})

# Logout
def user_logout(request):
    logout(request)
    return redirect("login")

def profile_view(request, identifier):
    """
    Show student or organization profile based on identifier.
    """
    # Try to find student by SR-Code first
    user = User.objects.filter(sr_code=identifier).first()
    
    # If not found, try organization username
    if not user:
        user = get_object_or_404(User, username=identifier)

    if user.is_organization:
        org = user.organization
        return render(request, "org_profile.html", {"org": org})
    else:
        student = user.student
        return render(request, "student_profile.html", {"student": student})