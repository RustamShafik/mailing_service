from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Message
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mail_messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mail_messages/message_form.html'
    success_url = reverse_lazy('message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mail_messages/message_form.html'
    success_url = reverse_lazy('message_list')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mail_messages/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)
