from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from .forms import StudentSignupForm, UserLoginForm
from .models import User, Organization

def student_signup(request):
    if request.method == "POST":
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = StudentSignupForm()
    return render(request, "signup.html", {"form": form})

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

def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def profile_view(request, identifier):
    """
    Unified profile view:
    - identifier: SR-code OR username
    """

    # First try SR-code (students)
    user = User.objects.filter(sr_code=identifier).first()

    # Fallback: username
    if not user:
        user = get_object_or_404(User, username=identifier)

    # Organization profile
    if user.is_organization:
        return render(request, "org_profile.html", {"org": user.organization})

    # Student profile
    return render(request, "student_profile.html", {
        "student": user.student,
        "followed_orgs": user.followed_organizations.all()
    })



@login_required
def follow_organization(request, identifier):
    """
    Students can follow/unfollow an organization using its username
    """

    org_user = get_object_or_404(User, username=identifier, is_organization=True)
    org = org_user.organization

    # Only students can follow
    if not request.user.is_organization:
        if request.user in org.followers.all():
            org.followers.remove(request.user)
        else:
            org.followers.add(request.user)

    return redirect("profile_view", identifier=identifier)



def org_tree(request):
    # Only root-level orgs (no parent)
    root_orgs = Organization.objects.filter(parent_organization__isnull=True)

    return render(request, "org_tree.html", {
        "root_orgs": root_orgs
    })
