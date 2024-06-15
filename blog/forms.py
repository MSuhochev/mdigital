from django import forms
from .models import Subscriber, ConsultationRequest


class SubscriberForm(forms.ModelForm):
    agree_to_privacy_policy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'agree_to_privacy_policy'})
    )

    class Meta:
        model = Subscriber
        fields = ['email']

    def clean_agree_to_privacy_policy(self):
        agree = self.cleaned_data.get('agree_to_privacy_policy')
        if not agree:
            raise forms.ValidationError("Вы должны согласиться с правилами обработки персональных данных.")
        return agree


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['name', 'phone', 'preferred_time']