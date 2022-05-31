from cProfile import label
from dataclasses import fields
from django.forms import ModelForm
from django import forms as f
from .models import Ticket

class TicketForm(ModelForm):
    title = f.CharField(min_length=10, widget=
        f.TextInput(attrs= {'placeholder': 'Enter your title ', 'class': 'block w-full px-4 py-2 mt-2 text-pink-600 bg-white border rounded-md focus:border-pink-400 focus:ring-pink-300 focus:outline-none focus:ring focus:ring-opacity-40', } )
    )
    description = f.CharField(min_length=10, widget=
        f.Textarea(attrs= {'placeholder': 'Description', 'class': 'block w-full px-4 py-2 mt-2 text-pink-600 bg-white border rounded-md focus:border-pink-400 focus:ring-pink-300 focus:outline-none focus:ring focus:ring-opacity-40', 'rows': 5})
    )
    class Meta:
        model = Ticket 
        fields = ('title', 'description', 'attachment', 'priority_id' )
        required_fields = ('title', 'description', 'priority_id')
        widgets = {
            'priority_id': f.Select(attrs={'class':'form-select appearance-none block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding bg-no-repeat border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'}),
            'attachment': f.FileInput(attrs={'class': 'h-full w-full opacity-0 cursor-pointer'})
        }