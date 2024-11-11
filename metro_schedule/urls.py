# metro_schedule/urls.py
from django.urls import path
from schedules import views  # Adjust the import path as needed

urlpatterns = [
    path('', views.user_login, name='login'),  # Set login as the default page
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
]
