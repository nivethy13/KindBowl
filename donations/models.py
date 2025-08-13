from django.db import models
from accounts.models import User
from ngos.models import NGOProfile

# Create your models here.

class FoodDonation(models.Model):
    FOOD_TYPES = [
        ('cooked', 'Cooked Food'),
        ('raw', 'Raw Food'),
        ('packaged', 'Packaged Food'),
        ('beverages', 'Beverages'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    food_type = models.CharField(max_length=50, choices=FOOD_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    description = models.TextField()
    pickup_option = models.BooleanField(default=True)
    drop_off_address = models.TextField(blank=True)
    available_until = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.food_type} - {self.quantity} {self.unit} by {self.donor.username}"
    
    class Meta:
        verbose_name = 'Food Donation'
        verbose_name_plural = 'Food Donations'
        ordering = ['-created_at']

class DonationHistory(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    donation = models.ForeignKey(FoodDonation, on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGOProfile, on_delete=models.CASCADE)
    accepted_at = models.DateTimeField(auto_now_add=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='accepted')
    notes = models.TextField(blank=True)
    estimated_meals = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.donation} -> {self.ngo.organization_name}"
    
    class Meta:
        verbose_name = 'Donation History'
        verbose_name_plural = 'Donation Histories'
        ordering = ['-accepted_at']
