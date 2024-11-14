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


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.user_login, name='login'),  # Default route to login
#     path('home/', views.home, name='home'),
#     path('login/', views.user_login, name='login'),
#     path('signup/', views.user_signup, name='signup'),
#     path('profile/', views.profile, name='profile'),
#     path('logout/', views.user_logout, name='logout'),  # Add logout route
# ]


# update 3

from django.urls import path
from . import views

# urls.py

from django.urls import path
from .views import feedback, edit_feedback, delete_feedback

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('feedback/', feedback, name='feedback'),
    path('feedback/edit/<int:feedback_id>/', edit_feedback, name='edit_feedback'),  # Edit feedback
    path('feedback/delete/<int:feedback_id>/', delete_feedback, name='delete_feedback'),  # Delete feedback
]