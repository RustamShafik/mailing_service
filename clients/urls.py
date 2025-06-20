from django.urls import path
from .views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('add/', ClientCreateView.as_view(), name='client_add'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]