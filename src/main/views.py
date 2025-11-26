from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import Event

from django.utils import timezone

def home(request):
    return render(request, 'home.html')

@login_required
def landing(request):
    followed_orgs = request.user.followed_organizations.all()
    now = timezone.localtime()

    status_filter = request.GET.get("status", "all")
    sort_filter = request.GET.get("sort", "asc")

    events = Event.objects.filter(organization__in=followed_orgs)

    # Filter for Future, Ongoing, and Finished Events

    if status_filter == "future":
        events = events.filter(start_datetime__gt=now)

    elif status_filter == "ongoing":
        events = events.filter(start_datetime__lte=now, end_datetime__gte=now)

    elif status_filter == "finished":
        events = events.filter(end_datetime__lt=now)

    # Filter by Ascending/Descending Date and Time
    
    if sort_filter == "desc":
        events = events.order_by("-start_datetime")
    else:
        events = events.order_by("start_datetime")

    return render(request, "landing.html", {
        "events": events,
        "status_filter": status_filter,
        "sort_filter": sort_filter,
    })


