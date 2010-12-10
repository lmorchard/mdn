from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list

from tagging.views import tagged_object_list

from demos.models import Submission
from voting.views import vote_on_object

from utils import JingoTemplateLoader
template_loader = JingoTemplateLoader()

urlpatterns = patterns('demos.views',

    url(r'^$', 'home', 
        name='demos'),

    url(r'^submit', 'submit', 
        name='demos_submit'),

    url(r'^detail/(?P<slug>[^/]+)/?$', 'detail',
        name='demos_detail'),

    url(r'^detail/(?P<slug>[^/]+)/like$', 'like',
        name='demos_like'),

    url(r'^detail/(?P<slug>[^/]+)/download$', 'download',
        name='demos_download'),

    url(r'^detail/(?P<slug>[^/]+)/launch$', 'launch',
        name='demos_launch'),
    
    url(r'^detail/(?P<slug>[^/]+)/edit$', 'edit',
        name='demos_edit'),

    url(r'^all/$', object_list, 
        dict(queryset=Submission.objects.all(), 
            paginate_by=25, allow_empty=True,
            template_loader=template_loader,
            template_object_name='submission',
            template_name='demos/listing.html'), 
        name='demos_all'),

    url(r'^tag/(?P<tag>[^/]+)/$', tagged_object_list,
        dict(queryset_or_model=Submission,
             paginate_by=25, allow_empty=True, related_tags=True,
             template_loader=template_loader,
             template_object_name='submission',
             template_name='demos/listing.html'),
        name='demos_tag'),

    url(r'^profile/(?P<username>[^/]+)/?$', 'profile_detail',
        name="demos_profile_detail"),

)

urlpatterns += patterns('django.contrib.auth.views',

    url(r'^login$', 'login',
        dict( template_name="demos/login.html" ),
        name="demos_login"),
    
    url(r'^logout$', 'logout',
        name="demos_logout"),

)
