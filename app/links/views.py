import random

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from analytics.models import LinkAudit
from common.utils import get_encoded_str

from .forms import CustomSignUpForm
from .models import Link
from .utils import increase_hit_by_one, is_url_safe, is_unique_short_url

User = get_user_model()

def redirect_short_url(request, url):
    link_queryset = Link.objects.filter(short_url=url)

    # Since, we do not want to hit db again
    # so, use len instead of count()
    if (len(link_queryset) == 0):
        return render(request, "page_not_found.html")

    link_obj = link_queryset.first()
    # link_audit_obj, _ = LinkAudit.objects.get_or_create(link=link_obj)
    try:
        link_audit_obj = LinkAudit.objects.get(link=link_obj)
    except LinkAudit.DoesNotExist:
        link_audit_obj = LinkAudit.objects.create(hits=0)
        link_obj.link_audit = link_audit_obj
        link_obj.save()

    increase_hit_by_one(link_audit_obj)

    return redirect(link_obj.original_url)


def signup_view(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data["email"]
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = CustomSignUpForm()

    return render(request, "registration/signup.html", {"form": form})


def create_short_url_view(request):
    if request.method == "POST":
        context = {}
        # Get data from POST request
        data = request.POST.get("link")

        # Validation
        if not is_url_safe(data):
            context = {
                "error": "Please enter a valid URL. \
                URL must starts with either http:// or https://"
            }
            return render(request, "link/create.html", context)

        if not data.startswith(('http://', 'https://')):
            context = {
                "error": "URL must starts with either http:// or https://"
            }
            return render(request, "link/create.html", context)

        # Create short URL
        start_position = random.randint(0,15)
        short_url = get_encoded_str(
            data, start_position=start_position, length=8
        )

        # Validate Short URL
        # Keep creating until calidation is successful
        # limit = 25 times
        limit = 0
        while not is_unique_short_url(short_url) and limit < 25:
            short_url = get_encoded_str(data, start_position=0, length=8)
            limit += 1

        # Save
        link = Link.objects.create(
            created_by=request.user,
            original_url=data,
            short_url=short_url
        )

        return redirect(reverse_lazy("link_detail", kwargs={'pk':link.pk}))
    else:
        return render(request, "link/create.html")


class HomeView(TemplateView):
    template_name = "link/home.html"


class AboutView(TemplateView):
    template_name = "link/about.html"

class FAQView(TemplateView):
    template_name = "link/faq.html"


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "link/account.html"


class ComapreView(TemplateView):
    template_name = "link/compare.html"


class DashboardView(LoginRequiredMixin, ListView):
    model = Link
    context_object_name = "links"
    template_name = "link/dashboard.html"

    def get_queryset(self):
        return Link.objects.filter(created_by=self.request.user)


class LinkDetailView(LoginRequiredMixin, DetailView):
    model = Link
    template_name = "link/link_detail.html"

    def get_queryset(self):
        queryset = Link.objects.filter(created_by=self.request.user)
        return queryset


class LinkDeleteView(LoginRequiredMixin, DetailView):

    model = Link
    template_name = "link/delete_link.html"

    def get_queryset(self):
        queryset = Link.objects.filter(created_by=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return redirect(reverse_lazy('dashboard'))
