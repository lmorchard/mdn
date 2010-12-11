from datetime import datetime
from time import strftime
from os import unlink, makedirs
from os.path import basename, dirname, isfile, isdir
import re

import logging

import zipfile
import tarfile

from django.conf import settings

from django.utils.encoding import smart_unicode, smart_str

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

import tagging
import tagging.fields
import tagging.models

from tagging.utils import parse_tag_input
from tagging.fields import TagField
from tagging.models import Tag


def get_licenses():
    return {
        "cc-by-sa": _("CC-BY-SA Creative Commons Attribution-ShareAlike 3.0 [DEFAULT]"),
        "cc-by": _("CC-BY Creative Commons Attribution 3.0"),
        "cc-by-no": _("CC-BY-NO Creative Commons Attribution-NonCommercial 3.0"),
        "cc-by-no-sa": _("CC-BY-NO-SA Createive Commons Attribution-NonCommercial-ShareAlike 3.0"),
        "mpl": _("MPL/GPL/LGPL"),
        "gpl": _("GPL"),
        "lgpl": _("LGPL"),
        "bsd": _("BSD"),
        "apache": _("Apache"),
        "agpl": _("AGPL"),
        "cc-by-nd": _("CC-BY-ND Creative Commons Attribution-NonCommercial-NoDervis"),
        "cc-by-no-nd": _("CC-BY-NO-ND Creative Commons Attribution-NoDervis"),
        "publicdomain": _("Public Domain"),
        "other": _("Other (N/A)"),
    }


def mk_upload_to(subpath):
    def upload_to(instance, filename):
        c_name = ( instance.creator and 
                instance.creator.username or '_anon_' )
        return 'uploads/%s/%s/%s/%s' % ( 
                strftime('%Y/%m'), c_name, subpath, filename )
    return upload_to


class TagDescription(models.Model):
    """Description of a tag"""
    tag_name = models.CharField(_('name'), 
            max_length=50, unique=True, db_index=True, primary_key=True)
    title = models.CharField(_("title"), 
            max_length=255, blank=False, unique=True)
    description = models.TextField(_("description"), 
            blank=True)


class ConstrainedTagField(tagging.fields.TagField):
    """Tag field constrained to described tags"""

    def __init__(self, *args, **kwargs):
        if 'max_tags' not in kwargs:
            self.max_tags = 5
        else:
            self.max_tags = kwargs['max_tags']
            del kwargs['max_tags']
        super(ConstrainedTagField, self).__init__(*args, **kwargs)

    def validate(self, value, instance):

        if not isinstance(value, (list, tuple)):
            value = parse_tag_input(value)

        if len(value) > self.max_tags:
            raise ValidationError(_('Maximum of %s tags allowed') % 
                    (self.max_tags))

        for tag_name in value:
            try:
                # TODO: Maybe do just an existence check, rather than a get?
                desc = TagDescription.objects.get(tag_name=tag_name)
            except TagDescription.DoesNotExist:
                raise ValidationError(
                    _('Tag "%s" is not in the set of described tags') % 
                        (tag_name))

    def formfield(self, **kwargs):
        from .forms import ConstrainedTagFormField
        defaults = {'form_class': ConstrainedTagFormField}
        defaults.update(kwargs)
        return super(ConstrainedTagField, self).formfield(**defaults)


class Submission(models.Model):
    """Representation of a demo submission"""

    title = models.CharField(
            _("what is your demo's name?"), 
            max_length=255, blank=False, unique=True)
    slug = models.SlugField(_("slug"), 
            blank=False, unique=True)
    summary = models.CharField(
            _("describe your demo in one line"),
            max_length=255, blank=False)
    description = models.TextField(
            _("describe your demo in more detail (optional)"), 
            blank=True)

    featured = models.BooleanField()

    tags = ConstrainedTagField(
            _('select up to 5 tags that describe your demo'),
            max_tags=5)

    screenshot_1 = models.ImageField(
            _('Screenshot #1'),
            upload_to=mk_upload_to('screenshot_1'), blank=False)
    screenshot_2 = models.ImageField(
            _('Screenshot #2'),
            upload_to=mk_upload_to('screenshot_2'), blank=True)
    screenshot_3 = models.ImageField(
            _('Screenshot #3'),
            upload_to=mk_upload_to('screenshot_3'), blank=True)
    screenshot_4 = models.ImageField(
            _('Screenshot #4'),
            upload_to=mk_upload_to('screenshot_4'), blank=True)
    screenshot_5 = models.ImageField(
            _('Screenshot #5'),
            upload_to=mk_upload_to('screenshot_5'), blank=True)

    video_url = models.URLField(
            _("have a video of your demo in action? (optional)"),
            verify_exists=False, blank=True, null=True)

    demo_package = models.FileField(
            _('select a ZIP file containing your demo'),
            upload_to=mk_upload_to('demo_package'),
            blank=False)
    source_code_url = models.URLField(
            _("is your source code hosted online? (optional)"),
            verify_exists=False, blank=True, null=True)
    license_name = models.CharField(
            _("select a license for your source code"),
            max_length=64, blank=False, choices=get_licenses().items())

    creator = models.ForeignKey(User, blank=False)
    
    creator_name = models.CharField(
            _('what is your name?'),
            max_length=255, blank=True)
    creator_email = models.EmailField(
            _('what is your email address?'),
            max_length=255, blank=True)
    creator_location = models.CharField(
            _('where are you from?'),
            max_length=255, blank=True)
    creator_url = models.URLField(
            _("what is the URL of your home page?"),
            verify_exists=False, blank=True, null=True)
    
    created = models.DateTimeField( _('date created'), 
            auto_now_add=True, blank=False)
    modified = models.DateTimeField( _('date last modified'), 
            auto_now=True, blank=False)

    def __unicode__(self):
        return "<Submission %(title)s %(fn)s>" % dict(
            title=self.title, fn=self.demo_package )

    @models.permalink
    def get_absolute_url(self):
        return ('demos_detail', [self.slug]) 

    def clean(self):

        if self.demo_package:
            try:
                zf = zipfile.ZipFile(self.demo_package.file)
            except:
                raise ValidationError(
                    _('Demo package is not a valid zip file'))

            bad_file = zf.testzip()
            if bad_file:
                raise ValidationError(
                    _('Demo package is corrupt'))

            root_dir = self.get_demo_package_root()
            if not root_dir:
                raise ValidationError(
                    _('Demo package does not contain demo.html'))

            for name in zf.namelist():
                if name.startswith('/') or '/..' in name:
                    raise ValidationError(
                        _('Demo package contains invalid file entries'))


    def get_demo_package_root(self):
        zf = zipfile.ZipFile(self.demo_package.file)
        root_dir = None
        root_re = re.compile(r'(?P<root_dir>[^/]+)/demo.html')
        for name in zf.namelist():
            m = root_re.match(name)
            if m:
                root_dir = m.group('root_dir')
                break
        return root_dir

    def process_demo_package(self):

        zf = zipfile.ZipFile(self.demo_package.file)
        root_dir = self.get_demo_package_root()
        new_root_dir = self.demo_package.path.replace('.zip','')

        # Only accept non-empty files under the detected root directory that
        # don't start with "."
        valid_entries = [ x for x in zf.infolist() if 
                x.filename.startswith('%s/' % root_dir) and 
                not basename(x.filename).startswith('.') and
                x.file_size > 0 ]

        for zi in valid_entries:

            # Relocate all files from detected root dir to a directory named
            # for the zip file in storage
            out_fn = zi.filename.replace('%s/'%root_dir, '%s/'%new_root_dir)
            out_dir = dirname(out_fn)

            # Create parent directories where necessary.
            if not isdir(out_dir):
                makedirs(out_dir, 0775)

            # Extract the file from the zip into the desired location.
            open(out_fn, 'w').write(zf.read(zi))

