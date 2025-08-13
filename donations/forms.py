from django import forms
from .models import FoodDonation, DonationHistory

class FoodDonationForm(forms.ModelForm):
    class Meta:
        model = FoodDonation
        fields = ['food_type', 'quantity', 'unit', 'description', 'pickup_option', 'drop_off_address', 'available_until', 'image']
        widgets = {
            'available_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'drop_off_address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

class DonationHistoryForm(forms.ModelForm):
    class Meta:
        model = DonationHistory
        fields = ['status', 'notes', 'estimated_meals']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
