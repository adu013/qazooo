from django.db import models


class LinkAudit(models.Model):
    hits = models.PositiveIntegerField(default=0)
