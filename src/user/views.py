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
def profile_view(request, identifier=None, org_id=None):
    if org_id:
        org = get_object_or_404(Organization, id=org_id)

        return render(request, "org_profile.html", {
            "org": org,
        })

    user = User.objects.filter(sr_code=identifier).first()
    if not user:
        user = get_object_or_404(User, username=identifier)

    if user.is_organization:
        org = user.organization

        return render(request, "org_profile.html", {
            "org": org,
        })

    else:
        student = user.student
        followed_orgs = user.followed_organizations.all()

        return render(request, "student_profile.html", {
            "student": student,
            "followed_orgs": followed_orgs
        })

@login_required
def follow_organization(request, org_id):
    org = get_object_or_404(Organization, id=org_id)

    # Only allow students to follow
    if not request.user.is_organization:
        if request.user in org.followers.all():
            org.followers.remove(request.user)
        else:
            org.followers.add(request.user)

    return redirect("organization_profile", org_id=org.id)

def org_tree(request):
    # Only root-level orgs (no parent)
    root_orgs = Organization.objects.filter(parent_organization__isnull=True)

    return render(request, "org_tree.html", {
        "root_orgs": root_orgs
    })
