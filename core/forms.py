from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, AdmissionApplication, ContactMessage


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')


class ParentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['student_name', 'parent_email', 'grade_applied', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
