from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

sr_code_validator = RegexValidator(
    regex=r'^\d{2}-\d{5}$',
    message="SR-Code must be in the format 00-00000"
)

ORG_LEVELS = [
    ("UNIVERSITY", "University"),       # Level 1
    ("COLLEGE", "College"),             # Level 2
    ("DEPARTMENT", "Department"),       # Level 3
    ("ORGANIZATION", "Organization"),   # Level 4
]

class User(AbstractUser):
    is_organization = models.BooleanField(default=False)
    is_officer = models.BooleanField(default=False)   # you may remove this too if unused

    # Students use SR-Code as username
    sr_code = models.CharField(
        max_length=8,
        unique=True,
        null=True,
        blank=True,
        validators=[sr_code_validator]
    )

    def __str__(self):
        if self.is_organization:
            return self.username or "Unnamed Organization"
        return self.sr_code or f"User ID {self.id}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.sr_code} - {self.first_name} {self.last_name}"


class Organization(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="organization"
    )

    followers = models.ManyToManyField(
        User,
        related_name="followed_organizations",
        blank=True
    )

    organization_name = models.CharField(max_length=255)

    parent_organization = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="sub_organizations"
    )

    organization_level = models.CharField(
        max_length=20,
        choices=ORG_LEVELS,
        default="ORGANIZATION"
    )

    about = models.TextField(blank=True)

    profile_picture = models.ImageField(upload_to="org_profile_pics/", blank=True, null=True)
    header_picture = models.ImageField(upload_to="org_header_pics/", blank=True, null=True)

    def __str__(self):
        return self.organization_name

    @property
    def level_number(self):
        levels = {
            "UNIVERSITY": 1,
            "COLLEGE": 2,
            "DEPARTMENT": 3,
            "ORGANIZATION": 4,
        }
        return levels.get(self.organization_level, 4)

    @property
    def has_children(self):
        return self.sub_organizations.exists()

    def get_tree(self):
        return {
            "name": self.organization_name,
            "level": self.organization_level,
            "children": [child.get_tree() for child in self.sub_organizations.all()]
        }
