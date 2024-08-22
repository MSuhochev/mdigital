from django.urls import path
from .views import CaseDetailView, CaseListView, CaseGridView, CaseSearchView

urlpatterns = [
    path('search/', CaseSearchView.as_view(), name='search'),
    path('category/<slug:category_slug>/', CaseListView.as_view(), name='case_list'),
    path('case/<slug:category_slug>/<slug:case_slug>/', CaseDetailView.as_view(), name='case_detail'),
    path('', CaseGridView.as_view(), name='case_grid'),
]
