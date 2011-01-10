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
from django.template.defaultfilters import slugify

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


DEMO_LICENSES = getattr(settings, "DEMO_LICENSES", (
    ("cc-by-sa", _("CC-BY-SA Creative Commons Attribution-ShareAlike 3.0 [DEFAULT]")),
    ("cc-by", _("CC-BY Creative Commons Attribution 3.0")),
    ("cc-by-no", _("CC-BY-NO Creative Commons Attribution-NonCommercial 3.0")),
    ("cc-by-no-sa", _("CC-BY-NO-SA Createive Commons Attribution-NonCommercial-ShareAlike 3.0")),
    ("mpl", _("MPL/GPL/LGPL")),
    ("gpl", _("GPL")),
    ("lgpl", _("LGPL")),
    ("bsd", _("BSD")),
    ("apache", _("Apache")),
    ("agpl", _("AGPL")),
    ("cc-by-nd", _("CC-BY-ND Creative Commons Attribution-NonCommercial-NoDervis")),
    ("cc-by-no-nd", _("CC-BY-NO-ND Creative Commons Attribution-NoDervis")),
    ("publicdomain", _("Public Domain")),
    ("other", _("Other (N/A)")),
))


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


def get_root_for_submission(instance):
    c_name = instance.creator.username
    return 'uploads/demos/%(h1)s/%(h2)s/%(username)s/%(slug)s' % dict(
         h1=c_name[0], h2=c_name[1], username=c_name, slug=instance.slug,)

def mk_upload_to(field_fn):
     def upload_to(instance, filename):
         return '%(base)s/%(field_fn)s' % dict( 
             base=get_root_for_submission(instance), field_fn=field_fn)
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
    hidden = models.BooleanField()

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
            max_length=64, blank=False, choices=DEMO_LICENSES)

    creator = models.ForeignKey(User, blank=False, null=True)
    
    created = models.DateTimeField( _('date created'), 
            auto_now_add=True, blank=False)
    modified = models.DateTimeField( _('date last modified'), 
            auto_now=True, blank=False)

    def __unicode__(self):
        return 'Submission "%(title)s"' % dict(
            title=self.title )

    @models.permalink
    def get_absolute_url(self):
        return ('demos_detail', [self.slug]) 

    def save(self):
        """Save the submission, updating slug and screenshot thumbnails"""
        self.slug = slugify(self.title)
        super(Submission,self).save()
        self.update_thumbnails()

    def delete(self,using=None):
        root = '%s/%s' % (settings.MEDIA_ROOT, get_root_for_submission(self))
        if isdir(root): rmtree(root)
        super(Submission,self).delete(using)

    def clean(self):
        if self.demo_package:
            Submission.validate_demo_zipfile(self.demo_package)

    @classmethod
    def allows_listing_hidden_by(cls, user):
        if user.is_staff or user.is_superuser:
            return True
        return False

    def allows_hiding_by(self, user):
        if user.is_staff or user.is_superuser:
            return True
        return False

    def allows_viewing_by(self, user):
        if user.is_staff or user.is_superuser:
            return True
        if user == self.creator:
            return True
        if not self.hidden:
            return True
        return False

    def allows_editing_by(self, user):
        if user.is_staff or user.is_superuser:
            return True
        if user == self.creator:
            return True
        return False

    def allows_deletion_by(self, user):
        if user.is_staff or user.is_superuser:
            return True
        if user == self.creator:
            return True
        return False

    def update_thumbnails(self):
        """Update thumbnails to accompany full-size screenshots"""
        for idx in range(1, 6):

            name = 'screenshot_%s' % idx
            field = getattr(self, name)
            if not field: continue

            try:
                # TODO: Only update thumbnail if source image has changed / is newer
                thumb_name = field.name.replace('screenshot','screenshot_thumb')
                scaled_file = scale_image(field.file, (THUMBNAIL_MAXW, THUMBNAIL_MAXH))
                if scaled_file:
                    field.storage.delete(thumb_name)
                    field.storage.save(thumb_name, scaled_file)
            except:
                # TODO: Had some exceptions here related to scaling that
                # nonetheless resulted in an updated thumbnail. Investigate further.
                pass

    @classmethod
    def get_valid_demo_zipfile_entries(cls, zf):
        """Filter a zip file's entries for only accepted entries"""
        # TODO: Should we restrict to a certain set of {css,js,html,wot} extensions?
        return [ x for x in zf.infolist() if 
            not (x.filename.startswith('/') or '/..' in x.filename) and
            not (basename(x.filename).startswith('.')) and
            x.file_size > 0 ]

    @classmethod
    def validate_demo_zipfile(cls, file):
        """Ensure a given file is a valid ZIP file without disallowed file
        entries and with an HTML index."""
        try:
            zf = zipfile.ZipFile(file)
        except:
            raise ValidationError(_('Valid ZIP file is required'))

        if zf.testzip():
            raise ValidationError(_('ZIP file corrupted'))
        
        valid_entries = Submission.get_valid_demo_zipfile_entries(zf) 
        if len(valid_entries) == 0:
            raise ValidationError(_('ZIP file contains no acceptable files'))

        index_found = False
        for zi in valid_entries:
            name = zi.filename
            # HACK: We're accepting {index,demo}.html as the root index and
            # normalizing on unpack
            if 'index.html' == name or 'demo.html' == name:
                index_found = True
        
        if not index_found:
            raise ValidationError(_('HTML index not found in ZIP'))

    def process_demo_package(self):
        """Unpack the demo zipfile into the appropriate directory, filtering
        out any invalid file entries and normalizing demo.html to index.html if
        present."""

        # Derive a directory name from the zip filename, clean up any existing
        # directory before unpacking.
        new_root_dir = self.demo_package.path.replace('.zip','')
        if isdir(new_root_dir):
            rmtree(new_root_dir)

        # Load up the zip file and extract the valid entries
        zf = zipfile.ZipFile(self.demo_package.file)
        valid_entries = Submission.get_valid_demo_zipfile_entries(zf) 

        for zi in valid_entries:

            # HACK: Normalize demo.html to index.html
            if zi.filename == 'demo.html':
                zi.filename = 'index.html'

            # Relocate all files from detected root dir to a directory named
            # for the zip file in storage
            out_fn = '%s/%s' % ( new_root_dir, zi.filename )
            out_dir = dirname(out_fn)

            # Create parent directories where necessary.
            if not isdir(out_dir):
                makedirs(out_dir, 0775)

            # Extract the file from the zip into the desired location.
            open(out_fn, 'w').write(zf.read(zi))
