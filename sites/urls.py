from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.website_list, name='website_list'),
    path('create/', views.create_website, name='create'),
    path('<str:user_site_name>/<path:routes_on_original_site>', views.proxy_view, name='proxy'),
]
