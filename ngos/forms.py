from django import forms
from .models import NGOProfile

class NGOProfileForm(forms.ModelForm):
    class Meta:
        model = NGOProfile
        fields = ['organization_name', 'registration_number', 'description', 'working_hours', 'capacity', 'specializations', 'latitude', 'longitude']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'working_hours': forms.Textarea(attrs={'rows': 3}),
            'specializations': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
