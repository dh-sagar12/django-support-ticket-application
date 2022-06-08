import datetime
from datetime import datetime as dt
from django.contrib import messages
from django.http import  HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.db.models import   Q
from django.urls import reverse
from account.models import User
from tickets.forms import TicketForm
from tickets.models import Comment, Ticket
from django.db import connection



# Create your views here.


def get_users_recent_ticket(request):
    users_recent_ticket = Ticket.objects.filter(issued_by=  request.user.id).order_by('-created_on')[:6]
    return users_recent_ticket


def get_customer_monthly_summary(request):
    time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)

    total_submitted_ticket = Ticket.objects.filter(Q(issued_by= request.user.id) & Q(created_on__gt=time_threshold))

    total_closed_ticket = Ticket.objects.filter(Q(issued_by= request.user.id) & Q(is_closed=True) & Q(closed_by__isnull= False) & Q(created_on__gt=time_threshold) )

    total_pending_ticket = Ticket.objects.filter(Q(issued_by= request.user.id) & Q(is_opened=False) & Q(opened_by__isnull= True) & Q(created_on__gt=time_threshold) )

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


def view_detailed_ticket(request, pk):
    ticket = Ticket.objects.get(id= pk, issued_by = request.user)
    if ticket.is_opened and ticket.opened_by is not None and not ticket.is_closed:
        status = 'Progressing'
    elif ticket.is_closed or ticket.closed_by is not None :
        status = 'Closed'
    elif ticket.assigned_to is not None and not ticket.is_opened :
        status = 'Assigned'
    elif ticket.opened_by is None and ticket.closed_by is None:
        status = 'Pending'
    comments = Comment.objects.filter(ticket_id_id= ticket.id)
    params = {'ticket': ticket, 'comments': comments, 'status': status}
    return render(request, 'tickets/ticket_detail.html',params)


def post_ticket_comment(request):
    if request.method == 'POST':
        id = request.POST.get('ticket_id')
        comment = request.POST.get('comment')
        attachment = request.FILES.get('attachment')
        if attachment is not None:
            temp_comment = Comment(ticket_id_id =  id, user_id = request.user, comment=comment, attachment= attachment)
            temp_comment.save()
            messages.success(request, 'Comment has been Posted!')
        else:
            temp_comment =  Comment(ticket_id_id =  id, user_id = request.user, comment=comment) 
            temp_comment.save()
            messages.success(request, 'Comment has been Posted!')
        return HttpResponseRedirect(reverse('detail_ticket', args=id))
        # return redirect(reverse('detail_ticket', args=id))
    return  redirect(reverse('ticket'))
    

def get_ticket_close(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        ticket = Ticket.objects.get(id = id)
        if ticket.is_opened == False:
            # message = messages.warning(request, 'Cannot Closed Unopned Tickets')
            return JsonResponse({'status': 'closed', 'res': 'Cannot Closed Unopned Tickets' })
        else:
            ticket.is_closed = True
            ticket.closed_by = request.user
            ticket.closed_at =  datetime.datetime.now()
            ticket.save()
            return JsonResponse({'status': 'opened', 'res': 'Ticket has been closed' })
            # return HttpResponse('Ticket has been closed')


def get_ticket_details_for_admin_panel(request):
    time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)
    day = dt.today().day
    total_ticket = Ticket.objects.all().count()
    total_user =  User.objects.filter(Q(is_superuser = False) & Q(is_staff = False) & Q(is_admin = False)).count()
    new_user = User.objects.filter (Q(is_superuser = False) & Q(is_staff = False) & Q(is_admin = False) & Q(date_joined__gt = time_threshold)).count()
    to_do_task = Ticket.objects.filter(Q(assigned_to = request.user) & Q(opened_by = request.user) & Q(is_closed = False) ).count()
    todays_ticket =  Ticket.objects.filter(created_on__day=day).count()
    total_solved_ticket  =  Ticket.objects.filter( Q(is_closed =  True) & Q(closed_by = request.user) ).count()

    params = {
        'total_ticket': total_ticket,
        'total_user': total_user,
        'new_user': new_user,
        'to_do_task': to_do_task,
        'todays_ticket': todays_ticket,
        'total_solved_ticket': total_solved_ticket
    }

    return params

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_monthly_ticket_and_solved_ticket_chart(request):
    cursor = connection.cursor()
    # data = cursor.execute('''select * from ticket ''')
    monthly_ticket_count =  cursor.execute('''
            with total as (
            select date_part('month', t.created_on) month_id, count(t.id) as total_ticket from ticket t
            where  date_part('month', created_on) >  date_part('month', CURRENT_TIMESTAMP) -6
            group by month_id
        ), 
        solved as (
            select date_part('month', t.created_on) month_id, count(t.id) as solved_ticket from ticket t
            where  date_part('month', created_on) >  date_part('month', CURRENT_TIMESTAMP) -6 and
            t.is_closed 
            group by month_id
        )
        select m.month_name, total.total_ticket, COALESCE(solved.solved_ticket, 0) solved_ticket from total  
        left join solved on total.month_id  = solved.month_id 
        join months m  on total.month_id = m.month_id
    ''')

    row = dictfetchall(cursor)
    return JsonResponse(row, safe=False)
    