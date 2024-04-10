from django.urls import path

from .views import (
    LocationListView, 
    LocationCreateView, 
    LocationUpdateView, 
    LocationDeleteView,
)

urlpatterns = [
    path('', LocationListView.as_view(), name='location_list'),
    path('new/', LocationCreateView.as_view(), name='location_new'),
    path('<int:pk>/edit/', LocationUpdateView.as_view(), name='location_edit'),
    path('<int:pk>/delete/', LocationDeleteView.as_view(), name='location_delete'),
]