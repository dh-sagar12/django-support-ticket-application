from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
        path('ticket/', views.get_my_tickets, name='ticket' ),
        path('ticket/<int:pk>/', views.view_detailed_ticket, name='detail_ticket' ),
        path('ticket/post-comment/', views.post_ticket_comment, name='post_comment'),
        path('ticket/update/', views.get_ticket_close, name='close_ticket'),
        path('ticket/mts-chart/', views.get_monthly_ticket_and_solved_ticket_chart, name='get_monthly_ticket_and_solved_ticket_chart')


]