from django.views.generic import ListView, CreateView
from .models import Message
from django.urls import reverse_lazy

class MessageListView(ListView):
    model = Message
    template_name = 'mail_messages/message_list.html'
    context_object_name = 'messages'

class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mail_messages/message_form.html'
    success_url = reverse_lazy('message_list')
