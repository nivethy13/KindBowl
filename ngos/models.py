from django.db import models
from accounts.models import User

class NGOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.JSONField(default=dict)
    capacity = models.IntegerField(default=0)
    specializations = models.JSONField(default=list)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.organization_name
    
    class Meta:
        verbose_name = 'NGO Profile'
        verbose_name_plural = 'NGO Profiles'
