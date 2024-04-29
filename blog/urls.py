from django.urls import path
from . import views
from .views import PostSearchView, SubmitQuestionView, IncomingOrdersView, ContactFormSubmitView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', PostSearchView.as_view(), name='search'),
    path('submit-question/', SubmitQuestionView.as_view(), name='submit_question'),
    path('incoming-order/', IncomingOrdersView.as_view(), name='incoming_order'),
    path('contact-form-submit/', ContactFormSubmitView.as_view(), name='contact_form_submit'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('monetization/', views.MonetizationView.as_view(), name='monetization'),
    path('post_grid/', views.PostGridView.as_view(), name='post_grid'),
    path('tg_development/', views.TelegramDevelopmentView.as_view(), name='tg_development'),
    path('web_development/', views.WebDevelopmentView.as_view(), name='web_development'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('support/', views.SupportView.as_view(), name='support'),
    path('projects/', views.ProjectsGridView.as_view(), name='projects'),
    path('career/', views.CareerView.as_view(), name='career'),
    path('<slug:slug>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_single'),
    path('<slug:slug>/', views.PostListView.as_view(), name='post_list'),
]
