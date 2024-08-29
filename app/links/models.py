import qrcode

from io import BytesIO
from PIL import Image

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models

from common.db import models as common_models

User = get_user_model()


class Link(common_models.DateStampedModel):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    original_url = models.URLField(max_length=1000, blank=False, null=False)
    short_url = models.CharField(max_length=50)

    qr_img = models.ImageField(
        default=None, blank=True, null=True, upload_to="qrs"
    )

    link_audit = models.OneToOneField(
        "analytics.LinkAudit",
        blank=True,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        related_name="link"
    )

    def __str__(self) -> str:
        if len(self.original_url) > 25:
            return f"{self.original_url[:21]} ..."
        return self.original_url

    def save(self, *args, **kwargs):
        host = settings.MAIN_HOST
        full_url = host + self.short_url
        qr_image = qrcode.make(full_url)
        qr_offset = Image.new('RGB', (325, 325), 'white')
        qr_offset.paste(qr_image)
        file_name = f"{self.short_url}-qr.png"
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_img.save(file_name, File(stream), save=False)
        qr_offset.close()
        return super().save(*args, **kwargs)
