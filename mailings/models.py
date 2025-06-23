from django.db import models
from clients.models import Client
from mail_messages.models import Message
from django.conf import settings

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('FINISHED', 'Завершена'),
    ]

    start_time = models.DateTimeField("Начало рассылки")
    end_time = models.DateTimeField("Окончание рассылки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CREATED')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Client)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name="Пользователь"
    )

    def __str__(self):
        return f"Рассылка {self.pk} ({self.status})"

class Attempt(models.Model):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='attempts')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Успешно', 'Успешно'), ('Не успешно', 'Не успешно')])
    server_response = models.TextField()

    def __str__(self):
        return f"{self.timestamp} — {self.status}"