from django.db import models
from django.conf import settings

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.subject
