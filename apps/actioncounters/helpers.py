"""jingo helpers for actioncounters"""

import jinja2
from jingo import register, env
from .models import Action

@register.function
def action_count_for_object(action_name, object):
    return Action.objects[action_name].get_total(object=object)

@register.function
def action_count_for_object_by_request(action_name, request, object):
    return Action.objects[action_name].get_total_for_request(
            object=object, request=request)
