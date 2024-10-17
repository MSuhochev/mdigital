from django import forms
from phonenumber_field.formfields import PhoneNumberField
from blog.models import CostCalculationRequest


class WebCalculationForm(forms.ModelForm):
    phone = PhoneNumberField(region="RU")

    class Meta:
        model = CostCalculationRequest
        fields = ['name', 'phone', 'niche', 'functionality']
