from django.urls import path

from .views import (
    LocationListView, 
    LocationCreateView, 
    LocationUpdateView, 
    LocationDeleteView,
    LocationGraphicView,
    LocationFilterOptionsView,
)

urlpatterns = [
    path('', LocationListView.as_view(), name='location_list'),
    path('new/', LocationCreateView.as_view(), name='location_new'),
    path('<int:pk>/edit/', LocationUpdateView.as_view(), name='location_edit'),
    path('<int:pk>/delete/', LocationDeleteView.as_view(), name='location_delete'),
    path('<int:pk>/graphic/<int:year>/', LocationGraphicView.as_view(), name='location_graphic'),
    path('<int:pk>/graphic/filter-options/', LocationFilterOptionsView.as_view(), name='filter_options'),
]