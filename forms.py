from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Donor_Registers, Ngo_Registers, CustomUser

class CustomUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class DonorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Donor_Registers
        fields = ['name', 'age', 'dob', 'contact', 'address', 'designation', 'pan']

class NgoRegistrationForm(forms.ModelForm):
    class Meta:
        model = Ngo_Registers
        fields = ['name', 'registration_date', 'certified_status', 'causes', 'address', 'contact', 'description', 'bank_details']
