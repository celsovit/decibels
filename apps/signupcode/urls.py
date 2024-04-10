from django.urls import path

from .views import (
    SignupCodeListView, 
    SignupCodeCreateView, 
    SignupCodeUpdateView, 
    SignupCodeDeleteView,
)

urlpatterns = [
    path('', SignupCodeListView.as_view(), name='signupcode_list'),
    path('new/', SignupCodeCreateView.as_view(), name='signupcode_new'),
    path('<int:pk>/edit/', SignupCodeUpdateView.as_view(), name='signupcode_edit'),
    path('<int:pk>/delete/', SignupCodeDeleteView.as_view(), name='signupcode_delete'),
]