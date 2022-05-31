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
from tickets.forms import TicketForm
from tickets.models import Ticket
from tickets.views import add_new_ticket, get_customer_monthly_summary, get_users_recent_ticket

# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.user.is_staff or request.user.is_admin:
        return render(request, 'home/dashboard.html')

    elif request.user.is_active:
        users_recent_ticket = get_users_recent_ticket(request)
        customer_monthly_summary = get_customer_monthly_summary(request)
        get_add_new_ticket = add_new_ticket(request)
        # print(get_add_new_ticket)

        params =  {
            'users_recent_ticket': {'title': 'your recent tickets' , 'tickets':users_recent_ticket},
            'customer_monthly_summary': {
                'heading': 'Your monthly summary',
                'end': date.today() ,
                'starts_from': date.today().replace(day=1) - timedelta(days=30),
                'summary':customer_monthly_summary,

                },
            'get_add_new_ticket': get_add_new_ticket
            }
        if request.method =='POST':
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.issued_by = request.user
                ticket.save()
                return redirect(reverse('home'), kwargs= {'message': {'msg': 'TIcket Has been Submitted successfully!!', 'type': 'success'}})
            return render(request, 'home/home.html', params)

        return render(request, 'home/home.html', params)



def addTicket(request):
    if request.user.is_active:
        return render(request, 'home/home.html')
