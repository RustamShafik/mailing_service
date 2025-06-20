from django.views.generic import ListView
from .models import Message

class MessageListView(ListView):
    model = Message
    template_name = 'mail_messages/message_list.html'
    context_object_name = 'messages'
