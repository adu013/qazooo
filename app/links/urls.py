from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import redirect_short_url

urlpatterns = [
    path("<str:url>", redirect_short_url, name="redirect_short_url"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
