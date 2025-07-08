from django import forms
from django.forms import ModelForm
from SearchApp.models import Reg,LostItem,FoundItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'my-2'}),
            'last_name': forms.TextInput(attrs={'class': 'my-2'}),
            'username': forms.TextInput(attrs={'class': 'my-2'}),
            'email': forms.EmailInput(attrs={'class': 'my-2'}),
        }



class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['item_name', 'description', 'found_location', 'found_date', 'image']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': ' fs-5 my-2'}),
            'description': forms.Textarea(attrs={'class': ' fs-5 my-2', 'rows': 3}),
            'date_lost': forms.DateInput(attrs={'type': 'date', 'class': 'fs-5 my-2'}),
            'found_location': forms.TextInput(attrs={'class':'fs-5 my-2'}),
            'image': forms.ClearableFileInput(attrs={'class': 'custom-image-input fs-5 my-2'}),
            'found_date': forms.DateInput(attrs={'type': 'date'}),
        }


class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['item_name', 'description', 'date_lost', 'location', 'image']
        widgets = {
			 'item_name': forms.TextInput(attrs={'class': ' fs-5 my-2'}),
            'description': forms.Textarea(attrs={'class': ' fs-5 my-2', 'rows': 3}),
            'date_lost': forms.DateInput(attrs={'type': 'date', 'class': 'fs-5 my-2'}),
            'location': forms.TextInput(attrs={'class':'fs-5 my-2'}),
            'image': forms.ClearableFileInput(attrs={'class': 'custom-image-input fs-5 my-2'}),
            
        }
