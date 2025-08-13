from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Notification, EmailTemplate

def send_notification_email(recipient, subject, message, template_name=None):
    """Send notification email to user"""
    try:
        if template_name:
            # Use email template if provided
            template = EmailTemplate.objects.get(name=template_name, is_active=True)
            subject = template.subject
            message = template.body
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER or 'noreply@foodconnect.com',
            recipient_list=[recipient.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def create_notification(recipient, notification_type, title, message, related_donation=None, related_donation_history=None):
    """Create a new notification"""
    try:
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            related_donation=related_donation,
            related_donation_history=related_donation_history
        )
        return notification
    except Exception as e:
        print(f"Notification creation failed: {e}")
        return None

def send_donation_accepted_notification(donation_history):
    """Send notification when donation is accepted"""
    donation = donation_history.donation
    donor = donation.donor
    ngo = donation_history.ngo
    
    # Create in-app notification
    title = "Donation Accepted!"
    message = f"Your donation of {donation.get_food_type_display()} has been accepted by {ngo.organization_name}."
    
    notification = create_notification(
        recipient=donor,
        notification_type='donation_accepted',
        title=title,
        message=message,
        related_donation=donation,
        related_donation_history=donation_history
    )
    
    # Send email notification
    email_subject = "Your Donation Has Been Accepted!"
    email_message = f"""
    Hello {donor.username},
    
    Great news! Your donation has been accepted by {ngo.organization_name}.
    
    Donation Details:
    - Food Type: {donation.get_food_type_display()}
    - Quantity: {donation.quantity} {donation.unit}
    - Accepted by: {ngo.organization_name}
    - Accepted at: {donation_history.accepted_at}
    
    Thank you for making a difference in your community!
    
    Best regards,
    FoodConnect Team
    """
    
    send_notification_email(donor, email_subject, email_message)
    
    return notification

def send_new_donation_notification(donation):
    """Send notification to nearby NGOs about new donation"""
    from ngos.models import NGOProfile
    
    # Get all NGOs (in a real app, you'd filter by location)
    ngos = NGOProfile.objects.filter(is_verified=True)
    
    for ngo in ngos:
        title = "New Donation Available!"
        message = f"A new donation of {donation.get_food_type_display()} is available in your area."
        
        notification = create_notification(
            recipient=ngo.user,
            notification_type='new_donation',
            title=title,
            message=message,
            related_donation=donation
        )
        
        # Send email notification
        email_subject = "New Donation Available in Your Area!"
        email_message = f"""
        Hello {ngo.organization_name},
        
        A new donation is available in your area:
        
        - Food Type: {donation.get_food_type_display()}
        - Quantity: {donation.quantity} {donation.unit}
        - Available until: {donation.available_until}
        - Description: {donation.description[:100]}...
        
        Login to FoodConnect to accept this donation!
        
        Best regards,
        FoodConnect Team
        """
        
        send_notification_email(ngo.user, email_subject, email_message)

def send_donation_completed_notification(donation_history):
    """Send notification when donation is completed"""
    donation = donation_history.donation
    donor = donation.donor
    ngo = donation_history.ngo
    
    # Create in-app notification
    title = "Donation Completed!"
    message = f"Your donation has been successfully completed by {ngo.organization_name}. Estimated meals served: {donation_history.estimated_meals}"
    
    notification = create_notification(
        recipient=donor,
        notification_type='donation_completed',
        title=title,
        message=message,
        related_donation=donation,
        related_donation_history=donation_history
    )
    
    # Send email notification
    email_subject = "Donation Successfully Completed!"
    email_message = f"""
    Hello {donor.username},
    
    Your donation has been successfully completed!
    
    Donation Details:
    - Food Type: {donation.get_food_type_display()}
    - Quantity: {donation.quantity} {donation.unit}
    - Completed by: {ngo.organization_name}
    - Estimated meals served: {donation_history.estimated_meals}
    
    Thank you for helping those in need!
    
    Best regards,
    FoodConnect Team
    """
    
    send_notification_email(donor, email_subject, email_message)
    
    return notification
