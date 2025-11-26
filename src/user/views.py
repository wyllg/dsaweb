from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout
from .forms import StudentSignupForm, UserLoginForm, EventForm
from .models import User, Organization, Event
from django.utils import timezone

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

            # Case 1: User has an Organization profile
            if hasattr(user, "organization"):
                return redirect("profile_view", identifier=user.username)

            # Case 2: User is a student
            return redirect("landing")

    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})
def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def profile_view(request, identifier):

    # SR-code OR username
    # First try SR-code (students)
    user = User.objects.filter(sr_code=identifier).first()

    # Fallback: username
    if not user:
        user = get_object_or_404(User, username=identifier)

    # Organization profile
    if user.is_organization:
        org = user.organization
        events = org.events.all()
        now_time = timezone.localtime()

        future_events = events.filter(start_datetime__gt=now_time).order_by("start_datetime")
        ongoing_events = events.filter(
            start_datetime__lte=now_time,
            end_datetime__gte=now_time
        ).order_by("start_datetime")
        finished_events = events.filter(end_datetime__lt=now_time).order_by("-end_datetime")

        return render(request, "org_profile.html", {
            "org": org,
            "future_events": future_events,
            "ongoing_events": ongoing_events,
            "finished_events": finished_events,
        })

    # Student profile
    return render(request, "student_profile.html", {
        "student": user.student,
        "followed_orgs": user.followed_organizations.all()
    })

@login_required
def follow_organization(request, identifier):

    # Students can follow/unfollow an organization using its username

    org_user = get_object_or_404(User, username=identifier, is_organization=True)
    org = org_user.organization

    # Only students can follow
    if not request.user.is_organization:
        if request.user in org.followers.all():
            org.followers.remove(request.user)
        else:
            org.followers.add(request.user)

    return redirect("profile_view", identifier=identifier)

@login_required
def org_tree(request):
    
    root_orgs = Organization.objects.filter(parent_organization__isnull=True)

    return render(request, "org_tree.html", {
        "root_orgs": root_orgs
    })

@login_required
def create_event(request):
    if not request.user.is_organization:
        return redirect("landing")

    org = request.user.organization

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organization = org
            event.save()
            return redirect(
                "event_detail",
                username=org.user.username,
                event_id=event.id
            )
    else:
        form = EventForm()

    return render(request, "create_event.html", {"form": form})

@login_required
def event_detail(request, username, event_id):
    event = get_object_or_404(Event,
                              id=event_id,
                              organization__user__username=username)
    org = event.organization
    return render(request, "event_detail.html", {
        "event": event,
        "org": org
    })

@login_required
def edit_event(request, username, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        organization=request.user.organization
    )

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect(
                "event_detail",
                username=event.organization.user.username,
                event_id=event.id
            )
    else:
        
        initial = {
            "start_datetime": event.start_datetime.astimezone(
                timezone.get_current_timezone()
            ).replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M"),

            "end_datetime": event.end_datetime.astimezone(
                timezone.get_current_timezone()
            ).replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M"),
        }

        form = EventForm(instance=event, initial=initial)

    return render(request, "edit_event.html", {
        "form": form,
        "event": event
    })

@login_required
def delete_event(request, username, event_id):
    event = get_object_or_404(Event,
                              id=event_id,
                              organization=request.user.organization)

    if request.method == "POST":
        event.delete()
        return redirect("profile_view",
                        identifier=request.user.username)

    return render(request, "confirm_delete.html", {"object": event})
