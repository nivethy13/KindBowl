from django.db import models
from accounts.models import User
from donations.models import FoodDonation, DonationHistory

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('donation_accepted', 'Donation Accepted'),
        ('donation_completed', 'Donation Completed'),
        ('new_donation', 'New Donation Available'),
        ('reminder', 'Reminder'),
        ('system', 'System Message'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_donation = models.ForeignKey(FoodDonation, on_delete=models.CASCADE, null=True, blank=True)
    related_donation_history = models.ForeignKey(DonationHistory, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} - {self.recipient.username}"

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
