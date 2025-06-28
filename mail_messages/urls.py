from django.urls import path
from .views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView

urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('add/', MessageCreateView.as_view(), name='message_add'),
    path('<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]