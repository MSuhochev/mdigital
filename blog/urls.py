from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
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
