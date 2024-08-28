from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import redirect_short_url, AboutView, AccountView, CreateView, FAQView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about", AboutView.as_view(), name="about"),
    path("account", AccountView.as_view(), name="account"),
    path("create", CreateView.as_view(), name="create"),
    path("faq", FAQView.as_view(), name="faq"),
    path("<str:url>", redirect_short_url, name="redirect_short_url"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
