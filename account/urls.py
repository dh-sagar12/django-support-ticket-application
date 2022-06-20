from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path("signup/", views.createUser, name="signup"),
    path('password/', views.forgotPassword, name='forgotPassword'),
    path("password/set/<token>", views.setPassword, name="setPassword"),
    path("password/verification/", views.savePassword, name="savePassword"), 

]