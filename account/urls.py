from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path("signup/", views.createUser, name="signup"),
    # path('logout/', views.logoutView, name='logout'),
    # path("token/", views.token_send, name="token"),
    # path("success/", views.success, name="success"),
]