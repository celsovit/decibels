from django.db import models
from django.urls import reverse
import secrets
import string

from organization.models import Organization

class SignupCode(models.Model):
    
    email = models.EmailField(unique=True)
    authorization_code = models.CharField(max_length=8, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.authorization_code:
            self.authorization_code = self.generate_authorization_code()
        super().save(*args, **kwargs)

    def generate_authorization_code(self):
        alphanumeric = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphanumeric) for _ in range(8))

    def __str__(self):
        return self.email
