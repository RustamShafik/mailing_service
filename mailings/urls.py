from django.urls import path
from .views import (
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    test_email,
    StatisticsView,
    AttemptListView,
    SendMailingView
)

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('test/', test_email, name='test_email'),
    path('attempts/', AttemptListView.as_view(), name='attempt_list'),
    path('<int:pk>/send/', SendMailingView.as_view(), name='send_mailing'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]
