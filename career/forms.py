from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['first_name', 'last_name', 'email', 'resume_file']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
            'resume_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }