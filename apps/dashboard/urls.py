from django.urls import path

from . import views

urlpatterns = [
    path("", views.statistics_view, name="dashboard"),
    path("filter-options/", views.get_filter_options, name="chart-filter-options"),
    path('monthly-average/<int:year>/', views.get_monthly_average, name='chart-monthly-average'),
    path('top-peak-times/<int:year>/', views.get_top_peak_times, name='chart-top-peak-times'),
    path('locations-average/<int:year>/', views.get_locations_average, name='chart-locations-average'),
    path('top-peak-weekdays/<int:year>/', views.get_top_peak_weekdays, name='chart-top-peak-weekdays'),
    path('export/<int:year>/', views.save_as_excel, name='save_as_excel'),
]
