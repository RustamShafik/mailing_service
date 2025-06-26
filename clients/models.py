from django.db import models
from django.conf import settings

class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name='Владелец'
    )

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
