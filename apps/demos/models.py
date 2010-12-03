from datetime import datetime
from time import strftime
from os import unlink
from os.path import dirname, isfile

from django.conf import settings

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

import tagging
from tagging.fields import TagField
from tagging.models import Tag

#from threadedcomments.models import ThreadedComment

def mk_upload_to(subpath):
    def upload_to(instance, filename):
        c_name = ( instance.creator and 
                instance.creator.username or '_anon_' )
        return 'uploads/%s/%s/%s/%s' % ( 
                subpath, strftime('%Y/%m'), c_name, filename )
    return upload_to

class Submission(models.Model):

    title = models.CharField(_("title"), 
            max_length=255, blank=False, unique=True)
    slug = models.SlugField(_("slug"), 
            blank=False, unique=True)
    description = models.TextField(_("description"), 
            blank=True)

    featured = models.BooleanField()

    tags = TagField()

    demo_package = models.ImageField(_('demo package (zip or tar.gz)'),
            upload_to=mk_upload_to('demo_package'),
            blank=False)
    screenshot = models.ImageField(_('screenshot'),
            upload_to=mk_upload_to('screenshot'),
            blank=False)
    thumbnail = models.ImageField(_('thumbnail'),
            upload_to=mk_upload_to('thumbnail'),
            blank=True)

    launch_url = models.URLField(_("launch demo URL"),
            verify_exists=False, blank=False)
    more_info_url = models.URLField(_("more information URL"),
            verify_exists=False, blank=True, null=True)
    source_code_url = models.URLField(_("source code URL"),
            verify_exists=False, blank=True, null=True)

    creator = models.ForeignKey(User, blank=False)
    
    created = models.DateTimeField( _('date created'), 
            auto_now_add=True, blank=False)
    modified = models.DateTimeField( _('date last modified'), 
            auto_now=True, blank=False)

    @models.permalink
    def get_absolute_url(self):
        return ('demos_detail', [self.slug]) 

    def save(self):

        super(Submission, self).save()

