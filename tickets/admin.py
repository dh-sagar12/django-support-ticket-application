from django.contrib import admin

from tickets.models import Comment, Ticket, TicketPriority

# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'issued_by', 'opened_by', 'is_opened', 'is_closed')

admin.site.register(TicketPriority)
admin.site.register(Comment)
