from django.db import models


class LinkAudit(models.Model):
    count = models.PositiveIntegerField(default=0)
