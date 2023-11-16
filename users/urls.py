from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.custom_logout, name='logout'),
]
