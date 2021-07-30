from django.urls import path
from user import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns=[
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]