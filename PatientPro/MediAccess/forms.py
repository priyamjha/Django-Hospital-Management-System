from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Department, PatientRecord
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)
    full_name = forms.CharField(max_length=255, label='Full Name')

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'password1', 'password2', 'user_type']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if a user with the same username exists, regardless of user_type
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(_('Username already taken.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(_('Email already in use.'))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise ValidationError(_('Passwords do not match.'))

        # Custom password validation if needed (Django's built-in validators are recommended)
        if len(password1) < 8:
            raise ValidationError(_('Password must be at least 8 characters long and must contain number, alphabet & special character'))

        if not any(char.isdigit() for char in password1):
            raise ValidationError(_('Password must contain at least one number.'))

        if not any(char.isalpha() for char in password1):
            raise ValidationError(_('Password must contain at least one alphabet.'))

        if not any(char in '!@#$%^&*()-_+=' for char in password1):
            raise ValidationError(_('Password must contain at least one special character.'))

        return password2
    
    
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        user = authenticate(self.request, username=username, password=password)
        
        if not CustomUser.objects.filter(username=username).exists():
            raise ValidationError(_('Username does not exist.'))

        if user is None:
            if CustomUser.objects.filter(username=username).exists():
                raise ValidationError(_('Password is incorrect.'))

        return self.cleaned_data
    

class DoctorUpdateForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'address', 'professional_license_number', 'years_of_experience', 'department']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
        }
    


class PatientRecordForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='doctor').exclude(is_superuser=True),
        required=False,
        empty_label='Select a doctor'
    )

    class Meta:
        model = PatientRecord
        fields = ['diagnostics', 'observations', 'treatments', 'department', 'misc', 'doctor']
        widgets = {
            'diagnostics': forms.Textarea(attrs={'rows': 4}),
            'observations': forms.Textarea(attrs={'rows': 4}),
            'treatments': forms.Textarea(attrs={'rows': 4}),
            'misc': forms.Textarea(attrs={'rows': 4}),
        }


class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone_number', 'address']


class UserTypeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_type', 'full_name']
        widgets = {
            'user_type': forms.RadioSelect(choices=CustomUser.USER_TYPE_CHOICES),
        }