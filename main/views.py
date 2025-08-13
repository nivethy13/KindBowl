from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from donations.models import FoodDonation, DonationHistory
from ngos.models import NGOProfile

# Create your views here.

def home(request):
    """Home page view"""
    recent_donations = FoodDonation.objects.filter(status='available').order_by('-created_at')[:6]
    total_donations = FoodDonation.objects.count()
    total_ngos = NGOProfile.objects.filter(is_verified=True).count()
    
    context = {
        'recent_donations': recent_donations,
        'total_donations': total_donations,
        'total_ngos': total_ngos,
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """User dashboard with statistics"""
    if request.user.user_type == 'donor':
        # Donor dashboard
        my_donations = FoodDonation.objects.filter(donor=request.user)
        total_donations = my_donations.count()
        completed_donations = my_donations.filter(status='completed').count()
        total_meals = DonationHistory.objects.filter(
            donation__donor=request.user,
            status='completed'
        ).aggregate(total=Sum('estimated_meals'))['total'] or 0
        
        context = {
            'total_donations': total_donations,
            'completed_donations': completed_donations,
            'total_meals': total_meals,
            'recent_donations': my_donations[:5],
        }
        template = 'dashboard/donor_dashboard.html'
        
    elif request.user.user_type == 'ngo':
        # NGO dashboard
        try:
            ngo_profile = NGOProfile.objects.get(user=request.user)
            accepted_donations = DonationHistory.objects.filter(ngo=ngo_profile)
            total_accepted = accepted_donations.count()
            completed_donations = accepted_donations.filter(status='completed').count()
            total_meals = accepted_donations.aggregate(total=Sum('estimated_meals'))['total'] or 0
            
            context = {
                'ngo_profile': ngo_profile,
                'total_accepted': total_accepted,
                'completed_donations': completed_donations,
                'total_meals': total_meals,
                'recent_donations': accepted_donations[:5],
            }
            template = 'dashboard/ngo_dashboard.html'
        except NGOProfile.DoesNotExist:
            context = {'needs_profile': True}
            template = 'dashboard/ngo_dashboard.html'
    
    else:
        # Admin dashboard
        total_donations = FoodDonation.objects.count()
        total_ngos = NGOProfile.objects.count()
        total_users = request.user.__class__.objects.count()
        
        context = {
            'total_donations': total_donations,
            'total_ngos': total_ngos,
            'total_users': total_users,
        }
        template = 'dashboard/admin_dashboard.html'
    
    return render(request, template, context)

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')
