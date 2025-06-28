from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Client
from django.views.generic import ListView
from .models import Client
from django.views.generic.edit import UpdateView, DeleteView

class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.all()
        return Client.objects.filter(user=user)

class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.none()  # менеджер не может редактировать или удалять
        return Client.objects.filter(user=user)

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Client.objects.none()  # менеджер не может редактировать или удалять
        return Client.objects.filter(user=user)
