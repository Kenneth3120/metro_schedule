from django import forms
from .models import Profile
from .models import Feedback

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth', 'name', 'address']  # Ensure 'name' and 'address' are included

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'feedback']