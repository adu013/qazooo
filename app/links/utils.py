
def increase_hit_by_one(link_audit_obj):
    link_audit_obj.hits += 1
    link_audit_obj.save()
