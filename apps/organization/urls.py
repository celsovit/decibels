from django.urls import path

from .views import (
    OrganizationListView, 
    OrganizationCreateView, 
    OrganizationUpdateView, 
    OrganizationDeleteView,
)

urlpatterns = [
    path('', OrganizationListView.as_view(), name='organization_list'),
    path('new/', OrganizationCreateView.as_view(), name='organization_new'),
    path('<int:pk>/edit/', OrganizationUpdateView.as_view(), name='organization_edit'),
    path('<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization_delete'),
]