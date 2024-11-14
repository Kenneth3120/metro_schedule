# # metro_schedule/urls.py
# from django.urls import path, include

# urlpatterns = [
#     path('', include('schedules.urls')),  # Directs all URLs to the `schedules` app
#     path('home/', include('schedules.urls')),  # In case `/home/` is directly accessed
# ]


# metro_schedule/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('schedules.urls')),  # Includes all paths from schedules/urls.py
]
