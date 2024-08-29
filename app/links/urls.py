from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import (
    create_short_url_view, redirect_short_url, signup_view,  AboutView, AccountView, ComapreView, CreateView,
    DashboardView, FAQView, HomeView, LinkDeleteView)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about", AboutView.as_view(), name="about"),
    path("account", AccountView.as_view(), name="account"),
    path("account/signup", signup_view, name="signup"),
    path("account/", include("django.contrib.auth.urls")),
    path("compare", ComapreView.as_view(), name="compare"),
    path("create", create_short_url_view, name="create"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("faq", FAQView.as_view(), name="faq"),
    path("link/<int:pk>/delete", LinkDeleteView.as_view(), name="delete_link"),
    path("<str:url>", redirect_short_url, name="redirect_short_url"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
