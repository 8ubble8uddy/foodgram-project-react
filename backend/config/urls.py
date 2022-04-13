from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('api.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
]
