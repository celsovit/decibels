from django.urls import path

from .views import (
    MeasurementListView, 
    MeasurementCreateView, 
    MeasurementUpdateView, 
    MeasurementDeleteView,
    MeasurementImportView,
)

urlpatterns = [
    path('', MeasurementListView.as_view(), name='measurement_list'),
    path('new/', MeasurementCreateView.as_view(), name='measurement_new'),
    path('<int:pk>/edit/', MeasurementUpdateView.as_view(), name='measurement_edit'),
    path('<int:pk>/delete/', MeasurementDeleteView.as_view(), name='measurement_delete'),
    path('import/', MeasurementImportView.as_view(), name='measurement_import'),
]
