from django.urls import path
from .views import ClientListView, ClientCreateView

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('add/', ClientCreateView.as_view(), name='client_add'),
]