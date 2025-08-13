from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import FoodDonation, DonationHistory
from .forms import FoodDonationForm, DonationHistoryForm
from ngos.models import NGOProfile
from notifications.services import send_donation_accepted_notification, send_new_donation_notification, send_donation_completed_notification

@login_required
def create_donation(request):
    if request.method == 'POST':
        form = FoodDonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            
            # Send notifications to nearby NGOs
            send_new_donation_notification(donation)
            
            messages.success(request, 'Donation created successfully! NGOs in your area have been notified.')
            return redirect('donations:detail', pk=donation.pk)
    else:
        form = FoodDonationForm()
    
    return render(request, 'donations/create_donation.html', {'form': form})

def donation_list(request):
    donations = FoodDonation.objects.filter(status='available').order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        donations = donations.filter(
            Q(food_type__icontains=query) |
            Q(description__icontains=query) |
            Q(donor__username__icontains=query)
        )
    
    # Filter by food type
    food_type = request.GET.get('food_type')
    if food_type:
        donations = donations.filter(food_type=food_type)
    
    paginator = Paginator(donations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'food_types': FoodDonation.FOOD_TYPES,
    }
    return render(request, 'donations/list.html', context)

def donation_detail(request, pk):
    donation = get_object_or_404(FoodDonation, pk=pk)
    return render(request, 'donations/donation_detail.html', {'donation': donation})

@login_required
def my_donations(request):
    donations = FoodDonation.objects.filter(donor=request.user).order_by('-created_at')
    return render(request, 'donations/my_donations.html', {'donations': donations})

@login_required
def accept_donation(request, pk):
    donation = get_object_or_404(FoodDonation, pk=pk, status='available')
    
    if request.user.user_type != 'ngo':
        messages.error(request, 'Only NGOs can accept donations.')
        return redirect('donations:detail', pk=pk)
    
    try:
        ngo_profile = NGOProfile.objects.get(user=request.user)
    except NGOProfile.DoesNotExist:
        messages.error(request, 'Please complete your NGO profile first.')
        return redirect('ngos:profile')
    
    if request.method == 'POST':
        form = DonationHistoryForm(request.POST)
        if form.is_valid():
            donation_history = form.save(commit=False)
            donation_history.donation = donation
            donation_history.ngo = ngo_profile
            donation_history.save()
            
            donation.status = 'accepted'
            donation.save()
            
            # Send notification to donor
            send_donation_accepted_notification(donation_history)
            
            messages.success(request, 'Donation accepted successfully! The donor has been notified.')
            return redirect('donations:detail', pk=pk)
    else:
        form = DonationHistoryForm()
    
    return render(request, 'donations/accept_donation.html', {
        'form': form,
        'donation': donation
    })

@login_required
def ngo_donations(request):
    if request.user.user_type != 'ngo':
        messages.error(request, 'Access denied.')
        return redirect('main:home')
    
    try:
        ngo_profile = NGOProfile.objects.get(user=request.user)
        accepted_donations = DonationHistory.objects.filter(ngo=ngo_profile).order_by('-accepted_at')
    except NGOProfile.DoesNotExist:
        messages.error(request, 'Please complete your NGO profile first.')
        return redirect('ngos:profile')
    
    return render(request, 'donations/ngo_donations.html', {'accepted_donations': accepted_donations})
