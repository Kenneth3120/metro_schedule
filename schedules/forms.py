from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth', 'name', 'address']  # Ensure 'name' and 'address' are included