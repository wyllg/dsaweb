from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="org_profile"
        )
    
    name = models.CharField(max_length=255)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )

    LEVEL_CHOICES = (
        (1, "Council"),
        (2, "College"),
        (3, "Department"),
        (4, "Student Organization"),
    )

    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)

    def save(self, *args, **kwargs):
        if self.parent is None:
            self.level = 1
        else:
            self.level = self.parent.level + 1

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
class User(AbstractUser):
    is_organization = models.BooleanField(default=False)

    organization = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="members"
    )

    def __str__(self):
        return self.username