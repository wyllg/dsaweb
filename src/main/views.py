from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Organization

def home(request):
    return render(request, 'home.html')

@login_required
def landing(request):
    return render(request, 'landing.html')

def organizations(request):
    # get only root-level orgs (level = 1)
    roots = Organization.objects.filter(level=1)

    return render(request, "organizations.html", {"roots": roots})