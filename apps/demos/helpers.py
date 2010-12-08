import datetime
from django.utils.translation import ungettext, ugettext
import jinja2
from jingo import register, env
#from tower import ugettext as _
from django.core import urlresolvers

from tagging.models import Tag, TaggedItem
from tagging.utils import LINEAR, LOGARITHMIC

from voting.models import Vote

from .models import TagDescription


@register.inclusion_tag('demos/elements/submissions_list.html')
@jinja2.contextfunction
def submissions_list(context, submissions):
    return new_context(**locals())

@register.inclusion_tag('demos/elements/submission_thumb.html')
@jinja2.contextfunction
def submission_thumb(context, submission):
    return new_context(**locals())

@register.function
def tag_title(tag):
    try:
        desc = TagDescription.objects.get(tag_name=tag.name)
        return desc.title
    except TagDescription.DoesNotExist:
        return tag.name

@register.function
def tag_description(tag):
    try:
        desc = TagDescription.objects.get(tag_name=tag.name)
        return desc.description
    except TagDescription.DoesNotExist:
        return ''

@register.function
def tags_for_object(obj):
    tags = Tag.objects.get_for_object(obj)
    return tags

@register.function
def vote_by_user_for_object(user, obj):
    return Vote.objects.get_for_user(obj, user)

@register.function
def vote_score_for_object(obj):
    return Vote.objects.get_score(obj)

@register.filter
def date_diff(timestamp, to=None):
    if not timestamp:
        return ""

    #return type(timestamp)
    
    compare_with = to or datetime.date.today()
    delta = timestamp - compare_with
    
    if delta.days == 0: return u"today"
    elif delta.days == -1: return u"yesterday"
    elif delta.days == 1: return u"tomorrow"
    
    chunks = (
        (365.0, lambda n: ungettext('year', 'years', n)),
        (30.0, lambda n: ungettext('month', 'months', n)),
        (7.0, lambda n : ungettext('week', 'weeks', n)),
        (1.0, lambda n : ungettext('day', 'days', n)),
    )
    
    for i, (chunk, name) in enumerate(chunks):
        if abs(delta.days) >= chunk:
            count = abs(round(delta.days / chunk, 0))
            break

    date_str = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}
    
    if delta.days > 0: return "in " + date_str
    else: return date_str + " ago"

def new_context(context, **kw):
    c = dict(context.items())
    c.update(kw)
    return c


