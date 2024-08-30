from django.urls import path
from career.views import CareerView

urlpatterns = [
    path('career/', CareerView.as_view(), name='career'),
]