from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post_grid/', views.PostGridView.as_view(), name='post_grid'),
    path('<slug:slug>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_single'),
    path('<slug:slug>/', views.PostListView.as_view(), name='post_list'),
]
