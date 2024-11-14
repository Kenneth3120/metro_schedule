from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)  # Ensure this field exists
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
