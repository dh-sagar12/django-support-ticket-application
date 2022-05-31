import datetime
import imp
from django.shortcuts import redirect, render
from django.db.models import   Q
from django.urls import reverse
from tickets.forms import TicketForm
from tickets.models import Ticket

# Create your views here.


def get_users_recent_ticket(request):
    users_recent_ticket = Ticket.objects.filter(issued_by=  request.user.id).order_by('-created_on')[:6]
    return users_recent_ticket


def get_customer_monthly_summary(request):
    time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)

    total_submitted_ticket = Ticket.objects.filter(Q(issued_by= request.user.id) & Q(created_on__gt=time_threshold))

    total_closed_ticket = Ticket.objects.filter(Q(issued_by= request.user.id) & Q(is_closed=True) & Q(closed_by__isnull= False) & Q(created_on__gt=time_threshold) )

    total_pending_ticket = Ticket.objects.filter(Q(issued_by= request.user.id) & Q(is_opened=False) | Q(opened_by__isnull= True) & Q(created_on__gt=time_threshold) )

    total_progressing_ticket = Ticket.objects.filter(Q(issued_by= request.user.id) & Q(is_opened=True) & Q(opened_by__isnull= False) &Q(closed_by__isnull= True) &  Q(created_on__gt=time_threshold) )

    return {
        'total_submitted_ticket': {'title': 'Total Submitted Ticket', 'desc': 'tickets submitted by you..', 'qty': total_submitted_ticket},

        'total_closed_ticket': {'title': 'Total Closed Ticket', 'desc': 'tickets have been solved', 'qty': total_closed_ticket},

        'total_pending_ticket': {'title': 'Total Pending Ticket', 'desc': 'tickets are on pending',  'qty': total_pending_ticket},

        'total_progressing_ticket': {'title': 'Total Progressing Ticket', 'desc': 'tickets are being solved', 'qty': total_progressing_ticket}
    }

def add_new_ticket(request):
    if request.user.is_authenticated:
        form = TicketForm()
        return {
            'form': form
        }
    else:
        return redirect(reverse('login'))



def get_my_tickets(request):
    my_tickets =  Ticket.objects.filter(issued_by= request.user.id).order_by('-created_on')
    params = {
        'my_tickets': my_tickets
    }
    return render(request, 'tickets/mytickets.html', params)
