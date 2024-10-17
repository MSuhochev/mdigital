from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Subscriber, ConsultationRequest, CostCalculationRequest, MonetizationQuestionsRequest


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
    phone = forms.CharField(required=True)

    agree_to_privacy_policy = forms.BooleanField(
        required=True,
        label="Оставляя заявку, вы соглашаетесь с правилами обработки персональных данных"
    )

    class Meta:
        model = ConsultationRequest
        fields = ['name', 'phone', 'preferred_time']


class MonetizationQuestionForm(forms.ModelForm):
    agree_to_privacy_policy = forms.BooleanField(
        required=True,
        label="Оставляя заявку, вы соглашаетесь с правилами обработки персональных данных"
    )

    class Meta:
        model = MonetizationQuestionsRequest
        fields = ['name', 'phone', 'question']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон', 'id': 'phone'}),
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вопрос'}),
        }


class CostCalculationForm(forms.ModelForm):
    phone = PhoneNumberField(region="RU")
    FUNCTIONALITY_CHOICES = [
        ('feature1', 'Функция 1'),
        ('feature2', 'Функция 2'),
        ('feature3', 'Функция 3'),
        ('feature4', 'Функция 4'),
    ]

    functionality = forms.MultipleChoiceField(
        choices=FUNCTIONALITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,  # это поле может быть необязательным
    )

    class Meta:
        model = CostCalculationRequest
        fields = ['name', 'phone', 'niche', 'functionality']


class FeedbackForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',  # Добавляем placeholder
        })
    )
    message = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Место для сообщения, с которого начнётся отличное сотрудничество',  # Placeholder
            'rows': 4  # Количество строк для textarea
        })
    )
    attachment = forms.FileField(
        label='Прикрепить файл',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
        })
    )
