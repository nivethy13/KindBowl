from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import User
from ngos.models import NGOProfile
from .models import FoodDonation, DonationHistory
from decimal import Decimal

class DonationModelTest(TestCase):
    def setUp(self):
        self.donor = User.objects.create_user(
            username='donor',
            email='donor@example.com',
            password='testpass123',
            user_type='donor'
        )
        
        self.ngo_user = User.objects.create_user(
            username='ngo',
            email='ngo@example.com',
            password='testpass123',
            user_type='ngo'
        )
        
        self.ngo_profile = NGOProfile.objects.create(
            user=self.ngo_user,
            organization_name='Test NGO',
            capacity=100
        )
    
    def test_create_donation(self):
        donation = FoodDonation.objects.create(
            donor=self.donor,
            food_type='cooked',
            quantity=Decimal('5.0'),
            unit='kg',
            description='Test donation',
            available_until='2025-12-31 23:59:59',
            status='available'
        )
        self.assertEqual(donation.donor, self.donor)
        self.assertEqual(donation.food_type, 'cooked')
        self.assertEqual(donation.status, 'available')
    
    def test_donation_str(self):
        donation = FoodDonation.objects.create(
            donor=self.donor,
            food_type='cooked',
            quantity=Decimal('5.0'),
            unit='kg',
            description='Test donation',
            available_until='2025-12-31 23:59:59'
        )
        self.assertIn('cooked', str(donation))

class DonationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.donor = User.objects.create_user(
            username='donor',
            email='donor@example.com',
            password='testpass123',
            user_type='donor'
        )
        
        self.ngo_user = User.objects.create_user(
            username='ngo',
            email='ngo@example.com',
            password='testpass123',
            user_type='ngo'
        )
        
        self.ngo_profile = NGOProfile.objects.create(
            user=self.ngo_user,
            organization_name='Test NGO',
            capacity=100
        )
        
        self.donation = FoodDonation.objects.create(
            donor=self.donor,
            food_type='cooked',
            quantity=Decimal('5.0'),
            unit='kg',
            description='Test donation',
            available_until='2025-12-31 23:59:59',
            status='available'
        )
    
    def test_donation_list_view(self):
        response = self.client.get(reverse('donations:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/list.html')
    
    def test_donation_detail_view(self):
        response = self.client.get(reverse('donations:detail', args=[self.donation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/donation_detail.html')
    
    def test_create_donation_authenticated(self):
        self.client.login(username='donor', password='testpass123')
        response = self.client.get(reverse('donations:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/create_donation.html')
    
    def test_create_donation_unauthenticated(self):
        response = self.client.get(reverse('donations:create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_accept_donation_ngo(self):
        self.client.login(username='ngo', password='testpass123')
        response = self.client.get(reverse('donations:accept', args=[self.donation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/accept_donation.html')
    
    def test_accept_donation_donor(self):
        self.client.login(username='donor', password='testpass123')
        response = self.client.get(reverse('donations:accept', args=[self.donation.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect due to permission denied
