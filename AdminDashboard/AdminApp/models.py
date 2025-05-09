# Create your models here.
# dashboard/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='staff_members')
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username}"


