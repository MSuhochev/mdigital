from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['first_name', 'last_name', 'email', 'resume_file', 'cover_letter']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'resume_file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'cover_letter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Сопроводительное письмо'}),
        }
