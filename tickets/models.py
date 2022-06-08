from doctest import BLANKLINE_MARKER
from statistics import mode
from urllib import request
from django.conf import settings
from django.db import models
from account.models import User

# Create your models here.

class TicketPriority(models.Model):
    id =  models.AutoField(primary_key=True)
    name =  models.CharField(max_length=30, null=False)
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'ticket_priority'


class Ticket(models.Model):
    def avatar_directory_path(instance, filename):
        return '{2}/{1}'.format(instance.id, filename, 'attachments')
        
    id = models.AutoField(primary_key=True)
    title =  models.CharField(max_length=200, null=False )
    description = models.TextField(null=False)
    attachment = models.ImageField(upload_to=avatar_directory_path,  blank=True)
    issued_by  =models.ForeignKey(settings.AUTH_USER_MODEL, default=User,  related_name='issued_by',  on_delete=models.DO_NOTHING)
    opened_by  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='opened_by',  on_delete=models.DO_NOTHING)
    assigned_to =  models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='assigned_to', on_delete=models.DO_NOTHING)
    priority_id = models.ForeignKey(TicketPriority, on_delete=models.DO_NOTHING)
    is_opened =  models.BooleanField(null=True, default=False)
    is_closed =  models.BooleanField(null=True, default=False)
    closed_by =  models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='closed_by', on_delete=models.DO_NOTHING)
    opened_at =  models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_on  = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    class Meta:
        db_table = "ticket"


class Comment(models.Model):
    def avatar_directory_path(instance, filename):
        return '{2}/{1}'.format(instance.id, filename, 'attachments')

    id = models.AutoField(primary_key=True)
    ticket_id =  models.ForeignKey(Ticket,  on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.DO_NOTHING)
    comment =  models.TextField(null=False)
    created_on =  models.DateTimeField(auto_now_add=True)
    attachment = models.ImageField(upload_to=avatar_directory_path,  blank=True, null=True)


    def __str__(self):
        return self.comment

    class Meta:
        db_table = "comments"

