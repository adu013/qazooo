from django.shortcuts import redirect, render
from .models import Link


def redirect_short_url(request, url):
    link_queryset = Link.objects.filter(short_url=url)

    # Since, we do not want to hit db again
    # so, use len instead of count()
    if (len(link_queryset) == 0):
        return render(request, "page_not_found.html")

    link_obj = link_queryset.first()

    return redirect(link_obj.original_url)
