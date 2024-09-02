from django.urls import path
from webdev.views import WebdevView, WebCalculationView

urlpatterns = [
    path('webdev/', WebdevView.as_view(), name='webdev'),
    path('calculate-web-cost/', WebCalculationView.as_view(), name='calculate_web_cost'),
]
