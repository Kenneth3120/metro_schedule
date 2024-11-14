# # schedules/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('login/', views.user_login, name='login'),
#     path('signup/', views.user_signup, name='signup'),
#     path('profile/', views.profile, name='profile'),  # Add profile URL
# ]


# schedules/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.user_login, name='login'),  # Default route to login
#     path('home/', views.home, name='home'),
#     path('login/', views.user_login, name='login'),
#     path('signup/', views.user_signup, name='signup'),
#     path('profile/', views.profile, name='profile'),  # Profile page
#     path('profile/', views.profile, name='profile'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),  # Default route to login
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),  # Add logout route
]
