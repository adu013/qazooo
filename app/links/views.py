from django.shortcuts import redirect, render
from analytics.models import LinkAudit

from .models import Link
from .utils import increase_hit_by_one


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
