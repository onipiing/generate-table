from django.db import models
import uuid

# Create your models here.
class TableRow(models.Model):
    title = models.CharField(max_length=255, default="", blank=True, null=True)
    body = models.TextField(default="", blank=True, null=True)
    guid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)