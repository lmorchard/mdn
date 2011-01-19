import datetime
import urllib
import logging
import functools

from django.core.cache import cache
from django.utils.translation import ungettext, ugettext

from django.conf import settings

import jingo
import jinja2
from jinja2 import evalcontextfilter, Markup, escape
from jingo import register, env
#from tower import ugettext as _
from django.core import urlresolvers

from django.core.urlresolvers import reverse as django_reverse
from devmo.urlresolvers import reverse

from tagging.models import Tag, TaggedItem
from tagging.utils import LINEAR, LOGARITHMIC

from .models import Submission, TAG_DESCRIPTIONS

from threadedcomments.models import ThreadedComment, FreeThreadedComment
from threadedcomments.forms import ThreadedCommentForm, FreeThreadedCommentForm
from threadedcomments.templatetags import threadedcommentstags

# Monkeypatch threadedcomments URL reverse() to use devmo's
from devmo.urlresolvers import reverse
threadedcommentstags.reverse = reverse


TEMPLATE_INCLUDE_CACHE_EXPIRES = getattr(settings, 'TEMPLATE_INCLUDE_CACHE_EXPIRES', 300)


def new_context(context, **kw):
    c = dict(context.items())
    c.update(kw)
    return c

# TODO:liberate ?
def register_cached_inclusion_tag(template, key_fn=None, expires=TEMPLATE_INCLUDE_CACHE_EXPIRES):
    """Decorator for inclusion tags with output caching. 
    
    Accepts a string or function to generate a cache key based on the incoming
    parameters, along with an expiration time configurable as
    INCLUDE_CACHE_EXPIRES or an explicit parameter"""

    if key_fn is None:
        key_fn = template

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kw):

            if type(key_fn) is str:
                cache_key = key_fn
            else:
                cache_key = key_fn(*args, **kw)
            
            out = cache.get(cache_key)
            if out is None:
                context = f(*args, **kw)
                t = jingo.env.get_template(template).render(context)
                out = jinja2.Markup(t)
                cache.set(cache_key, out, expires)
            return out

        return register.function(wrapper)
    return decorator
   
def submission_key(prefix):
    """Produce a cache key function with a prefix, which generates the rest of
    the key based on a submission ID and last-modified timestamp."""
    def k(*args, **kw):
        submission = args[0]
        return 'submission:%s:%s:%s' % ( prefix, submission.id, submission.modified )
    return k

# TOOO: All of these inclusion tags could probably be generated & registered
# from a dict of function names and inclusion tag args, since the method bodies
# are all identical. Might be astronaut architecture, though.

@register_cached_inclusion_tag('demos/elements/submission_creator.html', submission_key('creator'))
def submission_creator(submission): return locals()

@register.inclusion_tag('demos/elements/submission_thumb.html')
def submission_thumb(submission,extra_class=None): return locals()

@register.inclusion_tag('demos/elements/submission_listing.html')
def submission_listing(submission_list,is_paginated,paginator,page_obj,feed_title,feed_url): return locals()

@register_cached_inclusion_tag('demos/elements/tags_list.html', 'demos_tags_list')
def tags_list(): return locals()

# Not cached, because it's small and changes based on current search query string
@register.inclusion_tag('demos/elements/search_form.html')
@jinja2.contextfunction
def search_form(context):
    return new_context(**locals())


@register.function
def urlencode(args):
    """URL encode a query string from a given dict"""
    return urllib.urlencode(args)

bitly_api = None
def _get_bitly_api():
    """Get an instance of the bit.ly API class"""
    global bitly_api
    if bitly_api is None:
        import bitly
        login = getattr(settings, 'BITLY_USERNAME', '')
        apikey = getattr(settings, 'BITLY_API_KEY', '')
        bitly_api = bitly.Api(login, apikey)
    return bitly_api

@register.filter
def bitly_shorten(url):
    """Attempt to shorten a given URL through bit.ly / mzl.la"""
    try:
        # TODO:caching
        return _get_bitly_api().shorten(url)
    except:
        # Just in case the bit.ly service fails or the API key isn't
        # configured, fall back to using the original URL.
        return url

@register.function
def tag_title(tag):
    if tag.name in TAG_DESCRIPTIONS:
        return TAG_DESCRIPTIONS[tag.name]['title']
    else:
        return tag.name

@register.function
def tag_description(tag):
    if tag.name in TAG_DESCRIPTIONS:
        return TAG_DESCRIPTIONS[tag.name]['description']
    else:
        return tag.name

@register.function
def tag_learn_more(tag):
    if tag.name in TAG_DESCRIPTIONS and 'learn_more' in TAG_DESCRIPTIONS[tag.name]:
        return TAG_DESCRIPTIONS[tag.name]['learn_more']
    else:
        return []

@register.function
def tags_for_object(obj):
    tags = Tag.objects.get_for_object(obj)
    return tags

@register.function
def tags_used_for_submissions():
    return Tag.objects.usage_for_model(Submission, counts=True, min_count=1)

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
def get_threaded_comment_form():
    return ThreadedCommentForm()

@register.function
def auto_transform_markup(comment):
    return threadedcommentstags.auto_transform_markup(comment)

