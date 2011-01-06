import datetime
from django.utils.translation import ungettext, ugettext
import jinja2
from jinja2 import evalcontextfilter, Markup, escape
from jingo import register, env
#from tower import ugettext as _
from django.core import urlresolvers

from django.core.urlresolvers import reverse as django_reverse
from devmo.urlresolvers import reverse

from tagging.models import Tag, TaggedItem
from tagging.utils import LINEAR, LOGARITHMIC

from .models import TagDescription

from threadedcomments.models import ThreadedComment, FreeThreadedComment
from threadedcomments.forms import ThreadedCommentForm, FreeThreadedCommentForm
from threadedcomments.templatetags import threadedcommentstags

# Monkeypatch threadedcomments URL reverse() to use devmo's
from devmo.urlresolvers import reverse
threadedcommentstags.reverse = reverse

def new_context(context, **kw):
    c = dict(context.items())
    c.update(kw)
    return c

@register.inclusion_tag('demos/elements/submission_creator.html')
@jinja2.contextfunction
def submission_creator(context, submission):
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

@register.filter
def date_diff(timestamp, to=None):
    if not timestamp:
        return ""

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

# TODO: Maybe just register the template tag functions in the jingo environment
# directly, rather than building adapter functions?

@register.function
def get_threaded_comment_tree(content_object, tree_root=0):
    return ThreadedComment.public.get_tree(content_object, root=tree_root)

@register.function
def get_comment_url(content_object, parent=None):
    return threadedcommentstags.get_comment_url(content_object, parent)

@register.function
def get_comment_count(content_object):
    return ThreadedComment.public.all_for_object(content_object).count() 

@register.function
def get_threaded_comment_form():
    return ThreadedCommentForm()

@register.function
def auto_transform_markup(comment):
    return threadedcommentstags.auto_transform_markup(comment)

