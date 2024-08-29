from urllib.parse import quote

from .models import Link

def increase_hit_by_one(link_audit_obj):
    link_audit_obj.hits += 1
    link_audit_obj.save()


def is_url_safe(string):
    return string == quote(string, safe=':/%')


def is_unique_short_url(short_url):
    try:
        Link.objects.get(short_url=short_url)
        return False
    except Link.DoesNotExist:
        return True
