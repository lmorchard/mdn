"""Feeds for submissions"""
import datetime
import validate_jsonp

import jingo

from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import SyndicationFeed, Rss201rev2Feed, Atom1Feed, get_tag_uri
import django.utils.simplejson as json
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext as _

from django.contrib.auth.models import User
from django.conf import settings

from devmo.urlresolvers import reverse

from tagging.utils import parse_tag_input
from tagging.models import Tag, TaggedItem
from .models import Submission, TAG_DESCRIPTIONS


MAX_FEED_ITEMS = getattr(settings, 'MAX_FEED_ITEMS', 15)


class SubmissionsFeed(Feed):
    title     = _('MDN demos')
    subtitle  = _('Demos submitted by MDN users')
    link      = '/'

    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super(SubmissionsFeed, self).__call__(request, *args, **kwargs)

    def feed_extra_kwargs(self, obj):
        return { 'request': self.request }

    def get_object(self, request, format):
        if format == 'json':
            self.feed_type = Atom1Feed
        elif format == 'rss':
            self.feed_type = Rss201rev2Feed
        else:
            self.feed_type = Atom1Feed

    def item_pubdate(self, submission):
        return submission.modified

    def item_title(self, submission):
        return submission.title

    def item_description(self, submission):
        return jingo.render_to_string(self.request, 
            'demos/feed_item_description.html', dict(
                request=self.request, submission=submission
            )
        )

    def item_author_name(self, submission):
        return '%s' % submission.creator

    def item_author_link(self, submission):
        return self.request.build_absolute_uri(
            reverse('demos.views.profile_detail', 
            args=(submission.creator.username,)))

    def item_link(self, submission):
        return self.request.build_absolute_uri(
            reverse('demos.views.detail', 
            args=(submission.slug,)))

    def item_categories(self, submission):
        return parse_tag_input(submission.tags)

    def item_copyright(self, submission):
        # TODO: Translate license name to something meaningful in the feed
        return submission.license_name

    def item_enclosure_url(self, submission):
        return self.request.build_absolute_uri(submission.demo_package.url)

    def item_enclosure_length(self, submission):
        return submission.demo_package.size
            
    def item_enclosure_mime_type(self, submission):
        return 'application/zip'


class RecentSubmissionsFeed(SubmissionsFeed):

    title    = _('MDN recent demos')
    subtitle = _('Demos recently submitted to MDN')

    def items(self):
        submissions = Submission.objects\
            .exclude(hidden=True)\
            .order_by('-modified').all()[:MAX_FEED_ITEMS]
        return submissions


class FeaturedSubmissionsFeed(SubmissionsFeed):

    title    = _('MDN featured demos')
    subtitle = _('Demos featured on MDN')

    def items(self):
        submissions = Submission.objects.filter(featured=True)\
            .exclude(hidden=True)\
            .order_by('-modified').all()[:MAX_FEED_ITEMS]
        return submissions


class TagSubmissionsFeed(SubmissionsFeed):

    def get_object(self, request, format, tag):
        super(TagSubmissionsFeed, self).get_object(request, format)
        if tag in TAG_DESCRIPTIONS:
            self.title    = _('MDN demos tagged %s') % TAG_DESCRIPTIONS[tag]['title']
            self.subtitle = TAG_DESCRIPTIONS[tag]['description']
        else:
            self.title    = _('MDN demos tagged "%s"') % tag
            self.subtitle = None
        return tag

    def items(self, tag):
        qs = Submission.objects.exclude(hidden=True)
        submissions = TaggedItem.objects.get_by_model(qs, [tag])
        return submissions.order_by('-modified').all()[:MAX_FEED_ITEMS]


class ProfileSubmissionsFeed(SubmissionsFeed):

    def get_object(self, request, format, username):
        super(ProfileSubmissionsFeed, self).get_object(request, format)
        user = get_object_or_404(User, username=username)
        self.title = _("%s's MDN demos") % user.username
        return user

    def items(self, user):
        submissions = Submission.objects.filter(creator=user)\
            .exclude(hidden=True)\
            .order_by('-modified').all()[:MAX_FEED_ITEMS]
        return submissions


class SearchSubmissionsFeed(SubmissionsFeed):

    def get_object(self, request, format, query_string):
        super(SearchSubmissionsFeed, self).get_object(request, format)
        self.title = _('MDN demo search for "%s"') % query_string
        self.subtitle = _('Search results for demo submissions matching "%s"') % query_string
        return query_string

    def items(self, query_string):
        submissions = Submission.objects.search(query_string)\
            .exclude(hidden=True)\
            .order_by('-modified').all()[:MAX_FEED_ITEMS]
        return submissions
