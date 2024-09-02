from django.urls import path
from career.views import CareerView, ResumeView

urlpatterns = [
    path('career/', CareerView.as_view(), name='career'),
    path('submit_resume/', ResumeView.as_view(), name='submit_resume'),
]
