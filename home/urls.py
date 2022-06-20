from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home' ),
    # path('mail/', views.send_ticket_submmited_email, name='send_ticket_submmited_email' ),
]