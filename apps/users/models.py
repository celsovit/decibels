from django.contrib.auth.models import AbstractUser
from django.db import models

from organization.models import Organization

class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True)
    administrator = models.BooleanField(default=False)