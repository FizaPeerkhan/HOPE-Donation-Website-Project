from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/ngo_dashboard/', views.ngo_dashboard, name='ngo_dashboard'),
    path('login/', views.login_page, name='login-page'),
    path('register/donor-register/', views.register, name='register'),
    path('register/ngo-register/', views.ngo_register, name='ngo-register'),
]