from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.stat.urls')),
    path('', include('apps.user.urls')),
]
