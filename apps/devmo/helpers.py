import cgi
import datetime
import re
import httplib, urllib, urlparse

from django.conf import settings
from django.core.cache import cache
from django.template import defaultfilters
from django.utils.html import strip_tags

from bleach import Bleach
from jingo import register
import jinja2
import pytz

import utils
from .urlresolvers import reverse


# Yanking filters from Django.
register.filter(strip_tags)
register.filter(defaultfilters.timesince)
register.filter(defaultfilters.truncatewords)

register.filter(utils.entity_decode)


bleach = Bleach()


@register.function
def page_title(title):
    return u'%s | Mozilla Developer Network' % title


@register.filter
def isotime(t):
    """Date/Time format according to ISO 8601"""
    if not hasattr(t, 'tzinfo'):
        return
    return _append_tz(t).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _append_tz(t):
    tz = pytz.timezone(settings.TIME_ZONE)
    return tz.localize(t)


@register.function
def thisyear():
    """The current year."""
    return jinja2.Markup(datetime.date.today().year)


@register.function
def url(viewname, *args, **kwargs):
    """Helper for Django's ``reverse`` in templates."""
    return reverse(viewname, args=args, kwargs=kwargs)


@register.filter
def urlparams(url_, hash=None, **query):
    """
Add a fragment and/or query paramaters to a URL.

New query params will be appended to exising parameters, except duplicate
names, which will be replaced.
"""
    url = urlparse.urlparse(url_)
    fragment = hash if hash is not None else url.fragment

    # Use dict(parse_qsl) so we don't get lists of values.
    q = url.query
    query_dict = dict(urlparse.parse_qsl(smart_str(q))) if q else {}
    query_dict.update((k, v) for k, v in query.items())

    query_string = _urlencode([(k, v) for k, v in query_dict.items()
                               if v is not None])
    new = urlparse.ParseResult(url.scheme, url.netloc, url.path, url.params,
                               query_string, fragment)
    return new.geturl()

def _urlencode(items):
    """A Unicode-safe URLencoder."""
    try:
        return urllib.urlencode(items)
    except UnicodeEncodeError:
        return urllib.urlencode([(k, smart_str(v)) for k, v in items])


@register.filter
def cleank(txt):
    """Clean and link some user-supplied text."""
    return jinja2.Markup(bleach.linkify(bleach.clean(txt)))

@register.filter
def urlencode(txt):
    """Url encode a path."""
    return urllib.quote_plus(txt)

@register.function
@jinja2.contextfunction
def devmo_url(context, path):
    """ Create a URL pointing to devmo.
        Look for a wiki page in the current locale first,
        then default to given path
    """
    current_locale = context['request'].locale
    locale_regexp = "/(?P<locale>\w+)/(?P<path>.*)"
    m = re.match(locale_regexp, path, re.IGNORECASE)
    if not m:
        return path
    devmo_url_dict = m.groupdict()
    devmo_locale, devmo_path = devmo_url_dict['locale'], devmo_url_dict['path']
    if current_locale != devmo_locale:
        devmo_local_path = '/' + settings.LANGUAGE_DEKI_MAP[current_locale] + '/' + devmo_path
        http_status_code = cache.get('devmo_local_path:%s' % devmo_local_path)
        if http_status_code is None:
            deki_tuple = urlparse.urlparse(settings.DEKIWIKI_ENDPOINT)
            conn = httplib.HTTPSConnection(deki_tuple.netloc)
            conn.request("GET", devmo_local_path)
            resp = conn.getresponse()
            http_status_code = resp.status
            cache.set('devmo_local_path:%s' % devmo_local_path, http_status_code)
            conn.close()
        if http_status_code == 200:
            path = devmo_local_path
    return path
