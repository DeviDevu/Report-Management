# Create your models here.
# dashboard/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model  # Correct way to get the custom user model
from django.core.exceptions import ValidationError
from datetime import date

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
    
    def total_assigned_staff(self):
        if self.role == 'manager':
            return self.staff_members.count()
        return 0

    def total_reports(self):
        if self.role == 'manager':
            return self.staff_members.prefetch_related('reports').count()
        return 0
    
    
    def clean(self):
        # Prevent users from being their own manager
        if self.manager == self:
            raise ValidationError("A user cannot be their own manager.")

        # Ensure non-admins cannot be superusers
        if self.role != 'admin' and self.is_superuser:
            raise ValidationError("Only Admin users can be superusers.")

    
User = get_user_model()  # This fetches the custom User model you defined

STATUS_CHOICES = [
    ('submitted', 'Submitted'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    submission_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    manager_comment = models.TextField(null=True, blank=True)
    screenshot = models.ImageField(upload_to='screenshots/', null=True, blank=True)  

    def __str__(self):
        return self.title
    

    def clean(self):
        # Ensure approval date is not set for non-approved reports
        if self.status != 'approved' and self.approval_date is not None:
            raise ValidationError("Approval date can only be set for approved reports.")
        
        # Prevent managers from approving their own reports
        if self.status == 'approved' and self.creator.role == 'manager':
            raise ValidationError("Managers cannot approve their own reports.")
    
    def save(self, *args, **kwargs):
        if self.status == 'approved':
           self.approval_date = date.today()
        if not self.pk:
            self.submission_date = date.today()
        super().save(*args, **kwargs)
         
        self.clean()
        

        
