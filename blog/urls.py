from django.urls import path, re_path
from . import views
from .views import PostSearchView, SubmitQuestionView, IncomingOrdersView, ContactFormSubmitView, Custom404View, \
    PrivacyPolicyView, ConsultationRequestView, CookieConsentView, \
    CostCalculationView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cookie-consent/', CookieConsentView.as_view(), name='cookie_consent'),
    path('search/', PostSearchView.as_view(), name='search'),
    path('submit-question/', SubmitQuestionView.as_view(), name='submit_question'),
    path('incoming-order/', IncomingOrdersView.as_view(), name='incoming_order'),
    path('calculate-cost/', CostCalculationView.as_view(), name='calculate_cost'),
    path('contact-form-submit/', ContactFormSubmitView.as_view(), name='contact_form_submit'),
    path('consultation/submit/', ConsultationRequestView.as_view(), name='consultation_submit'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('monetization/', views.MonetizationView.as_view(), name='monetization'),
    path('post_grid/', views.PostGridView.as_view(), name='post_grid'),
    path('tg_development/', views.TelegramDevelopmentView.as_view(), name='tg_development'),
    path('web_development/', views.WebDevelopmentView.as_view(), name='web_development'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('support/', views.SupportView.as_view(), name='support'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('post/<slug:slug>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_single'),
    path('posts/<slug:slug>/', views.PostListView.as_view(), name='post_list'),
]

handler404 = Custom404View.as_view()
