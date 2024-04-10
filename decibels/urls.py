from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('organization/', include('organization.urls')),
    path('location/', include('location.urls')),
    path('measurement/', include('measurement.urls')),
    path('signupcode/', include('signupcode.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('core.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)