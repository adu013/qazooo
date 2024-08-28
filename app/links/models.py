from django.contrib.auth import get_user_model
from django.db import models

from common.db import models as common_models

User = get_user_model()


class Link(common_models.DateStampedModel):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    original_url = models.URLField(max_length=1000, blank=False, null=False)
    short_url = models.CharField(max_length=50)

    qr_img = models.ImageField(default=None, blank=True, null=True)

    def __str__(self) -> str:
        if len(self.original_url) > 25:
            return f"{self.original_url[:21]} ..."
        return self.original_url
