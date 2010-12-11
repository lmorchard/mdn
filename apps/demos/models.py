from datetime import datetime
from time import strftime
from os import unlink, makedirs
from os.path import basename, dirname, isfile, isdir
from shutil import rmtree
import re

import logging

import zipfile
import tarfile

from django.conf import settings

from django.utils.encoding import smart_unicode, smart_str

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields.files import FieldFile, ImageFieldFile
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

from . import scale_image


try:
    from PIL import Image
except ImportError:
    import Image


THUMBNAIL_MAXW = getattr(settings, 'DEMO_THUMBNAIL_MAX_WIDTH', 133)
THUMBNAIL_MAXH = getattr(settings, 'DEMO_THUMBNAIL_MAX_HEIGHT', 100)

RESIZE_METHOD = getattr(settings, 'RESIZE_METHOD', Image.ANTIALIAS)


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


class OverwritingFieldFile(FieldFile):
    """The built-in FieldFile alters the filename when saving, if a file with
    that name already exists. This subclass deletes an existing file first so
    that an upload will replace it."""
    def save(self, name, content, save=True):
        name = self.field.generate_filename(self.instance, name)
        self.storage.delete(name)
        super(OverwritingFieldFile, self).save(name,content,save)
    

class OverwritingFileField(models.FileField):
    """This field causes an uploaded file to replace an existing one on disk."""
    attr_class = OverwritingFieldFile


class OverwritingImageFieldFile(ImageFieldFile):
    """The built-in FieldFile alters the filename when saving, if a file with
    that name already exists. This subclass deletes an existing file first so
    that an upload will replace it."""
    def save(self, name, content, save=True):
        name = self.field.generate_filename(self.instance, name)
        self.storage.delete(name)
        super(OverwritingImageFieldFile, self).save(name,content,save)
    

class OverwritingImageField(models.ImageField):
    """This field causes an uploaded file to replace an existing one on disk."""
    attr_class = OverwritingImageFieldFile


def mk_upload_to(field_fn):
     def upload_to(instance, filename):
         c_name = ( instance.creator and 
                 instance.creator.username or '_anon_' )
         return 'uploads/demos/%(h1)s/%(h2)s/%(username)s/%(slug)s/%(field_fn)s' % dict( 
             h1=c_name[0],
             h2=c_name[1],
             username=c_name,
             slug=instance.slug,
             field_fn=field_fn)
     return upload_to


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

    screenshot_1 = OverwritingImageField(
            _('Screenshot #1'),
            upload_to=mk_upload_to('screenshot_1.png'), blank=False)
    screenshot_2 = OverwritingImageField(
            _('Screenshot #2'),
            upload_to=mk_upload_to('screenshot_2.png'), blank=True)
    screenshot_3 = OverwritingImageField(
            _('Screenshot #3'),
            upload_to=mk_upload_to('screenshot_3.png'), blank=True)
    screenshot_4 = OverwritingImageField(
            _('Screenshot #4'),
            upload_to=mk_upload_to('screenshot_4.png'), blank=True)
    screenshot_5 = OverwritingImageField(
            _('Screenshot #5'),
            upload_to=mk_upload_to('screenshot_5.png'), blank=True)

    video_url = models.URLField(
            _("have a video of your demo in action? (optional)"),
            verify_exists=False, blank=True, null=True)

    demo_package = OverwritingFileField(
            _('select a ZIP file containing your demo'),
            upload_to=mk_upload_to('demo_package.zip'),
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

    def generate_thumbnails(self):

        for idx in range(1, 6):

            name = 'screenshot_%s' % idx
            field = getattr(self, name)
            if not field: continue

            try:
                thumb_name = field.name.replace('screenshot','screenshot_thumb')
                scaled_file = scale_image(field.file, (THUMBNAIL_MAXW, THUMBNAIL_MAXH))
                if scaled_file:
                    field.storage.delete(thumb_name)
                    field.storage.save(thumb_name, scaled_file)
            except:
                pass

    def process_demo_package(self):

        zf = zipfile.ZipFile(self.demo_package.file)
        root_dir = self.get_demo_package_root()

        # Derive a directory name from the zip filename, clean up any existing
        # directory before unpacking.
        new_root_dir = self.demo_package.path.replace('.zip','')
        if isdir(new_root_dir):
            rmtree(new_root_dir)

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

