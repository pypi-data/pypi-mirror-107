from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mikoa/', include('mikoa.urls', namespace='mikoa'))
]
