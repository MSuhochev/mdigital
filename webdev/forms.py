from django import forms
from blog.models import CostCalculationRequest


class WebCalculationForm(forms.ModelForm):
    class Meta:
        model = CostCalculationRequest
        fields = ['name', 'phone', 'niche', 'functionality']
