from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from analytics.models import LinkAudit

from .forms import CustomSignUpForm
from .models import Link
from .utils import increase_hit_by_one

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


class HomeView(TemplateView):
    template_name = "link/home.html"


class AboutView(TemplateView):
    template_name = "link/about.html"


class CreateView(LoginRequiredMixin, TemplateView):
    template_name = "link/create.html"


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
