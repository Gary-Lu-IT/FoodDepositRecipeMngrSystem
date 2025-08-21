from django.db import models
from core.models import HexIdModel


class Notification(HexIdModel):
    channel = models.CharField(max_length=20) # email/line/telegram
    subject = models.CharField(max_length=120)
    body = models.TextField()
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
