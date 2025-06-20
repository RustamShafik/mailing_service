from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Client
from django.views.generic import ListView
from .models import Client

class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')