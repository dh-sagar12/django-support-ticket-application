from time import timezone
from django.shortcuts import render

# Create your views here.
import uuid
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from account.models import User
from tickets.models import Ticket
from tickets.views import get_customer_monthly_summary, get_users_recent_ticket

# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.user.is_staff or request.user.is_admin:
        return render(request, 'home/dashboard.html')

    elif request.user.is_active:
        users_recent_ticket = get_users_recent_ticket(request)
        customer_monthly_summary = get_customer_monthly_summary(request)

        params =  {
            'users_recent_ticket': {'title': 'your recent tickets' , 'tickets':users_recent_ticket},
            'customer_monthly_summary': {
                'heading': 'Your monthly summary',
                'end': date.today() ,
                'starts_from': date.today().replace(day=1) - timedelta(days=30),
                'summary':customer_monthly_summary,

                }
            }
        return render(request, 'home/home.html', params)



def addTicket(request):
    if request.user.is_active:
        return render(request, 'home/home.html')
