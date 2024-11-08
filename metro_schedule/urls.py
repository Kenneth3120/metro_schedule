from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schedules.urls')),  # Include URLs from the schedules app
]
