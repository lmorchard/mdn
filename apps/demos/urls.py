from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list

from tagging.views import tagged_object_list

from demos.models import Submission

from .feeds import RecentSubmissionsFeed, FeaturedSubmissionsFeed
from .feeds import TagSubmissionsFeed, ProfileSubmissionsFeed
from .feeds import SearchSubmissionsFeed

from utils import JingoTemplateLoader
template_loader = JingoTemplateLoader()


urlpatterns = patterns('demos.views',

    url(r'^$', 'home', name='demos'),
    url(r'^terms', 'terms', name='demos_terms'),
    url(r'^submit', 'submit', name='demos_submit'),
    url(r'^detail/(?P<slug>[^/]+)/?$', 'detail', name='demos_detail'),
    url(r'^detail/(?P<slug>[^/]+)/like$', 'like', name='demos_like'),
    url(r'^detail/(?P<slug>[^/]+)/unlike$', 'unlike', name='demos_unlike'),
    url(r'^detail/(?P<slug>[^/]+)/flag$', 'flag', name='demos_flag'),
    url(r'^detail/(?P<slug>[^/]+)/download$', 'download', name='demos_download'),
    url(r'^detail/(?P<slug>[^/]+)/launch$', 'launch', name='demos_launch'),
    url(r'^detail/(?P<slug>[^/]+)/edit$', 'edit', name='demos_edit'),
    url(r'^detail/(?P<slug>[^/]+)/delete$', 'delete', name='demos_delete'),
    url(r'^detail/(?P<slug>[^/]+)/comment/(?P<object_id>\d+)/delete/$', 
        'delete_comment', name='demos_delete_comment'),
    url(r'^detail/(?P<slug>[^/]+)/hide$', 'hideshow', dict( hide=True ), name='demos_hide'),
    url(r'^detail/(?P<slug>[^/]+)/show$', 'hideshow', dict( hide=False ), name='demos_show'),

    url(r'^search/$', 'search', name="demos_search"),
    url(r'^all/$', 'all', name='demos_all'),
    url(r'^tag/(?P<tag>[^/]+)/$', 'tag', name='demos_tag'),
    url(r'^profile/(?P<username>[^/]+)/?$', 'profile_detail', name="demos_profile_detail"),

    url(r'feeds/(?P<format>[^/]+)/all/', RecentSubmissionsFeed(), 
        name="demos_feed_recent"),
    url(r'feeds/(?P<format>[^/]+)/featured/', FeaturedSubmissionsFeed(), 
        name="demos_feed_featured"),
    url(r'feeds/(?P<format>[^/]+)/search/$', SearchSubmissionsFeed(), 
        name="demos_feed_search"),
    url(r'feeds/(?P<format>[^/]+)/tag/(?P<tag>[^/]+)/$', TagSubmissionsFeed(), 
        name="demos_feed_tag"),
    url(r'feeds/(?P<format>[^/]+)/profile/(?P<username>[^/]+)/?$', ProfileSubmissionsFeed(), 
        name="demos_feed_profile"),
    
)
urlpatterns += patterns('',
    (r'^comments/', include('threadedcomments.urls')),
)
