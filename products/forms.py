from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# Form for updating user profile information
class UserProfileForm(forms.ModelForm):
    # Additional fields that are part of the Profile model
    phone_number = forms.CharField(max_length=15, required=False, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Address")
    image = forms.ImageField(required=False, label="Profile Image")

    class Meta:
        # Use the User model for fields common to both User and Profile
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Fields from User model

    def __init__(self, *args, **kwargs):
        # Extract 'profile_instance' from kwargs to prepopulate Profile fields
        profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs)

        # Prepopulate fields from the Profile model if 'profile_instance' is provided
        if profile_instance:
            self.fields['phone_number'].initial = profile_instance.phone_number
            self.fields['address'].initial = profile_instance.address
            self.fields['image'].initial = profile_instance.image

    def save(self, commit=True):
        # Save the User instance first
        user = super().save(commit=commit)
    # Get or create the Profile instance associated with the user
        profile, created = Profile.objects.get_or_create(user=user)

    # Update Profile fields from the form data
        profile.phone_number = self.cleaned_data.get('phone_number')
        profile.address = self.cleaned_data.get('address')
        if self.cleaned_data.get('image'):
           profile.image = self.cleaned_data.get('image')  # Only update if a new image is uploaded

        if commit:
            profile.save()  # Save the Profile instance if commit is True

        return user  # Return the User instance

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


# Form for user registration
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    image = forms.ImageField(required=False, label="Profile Image")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        # Save User instance first without committing
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()  # Save User to create the user instance

            # Get or create Profile instance for the user
            profile, created = Profile.objects.get_or_create(user=user)

            # Update Profile fields if needed
            profile.image = self.cleaned_data.get('image')
            profile.save()  # Save Profile instance

        return user
