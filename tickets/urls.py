from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
        path('mytickets/', views.get_my_tickets, name='myTickets' ),
]