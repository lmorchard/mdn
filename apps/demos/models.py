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

from devmo.urlresolvers import reverse

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

import caching.base

from django.contrib.sites.models import Site
from django.contrib.auth.models import User

import tagging
import tagging.fields
import tagging.models

from tagging.utils import parse_tag_input
from tagging.fields import TagField
from tagging.models import Tag

from threadedcomments.models import ThreadedComment, FreeThreadedComment

from actioncounters.fields import ActionCounterField

from . import scale_image


try:
    from PIL import Image
except ImportError:
    import Image


THUMBNAIL_MAXW = getattr(settings, 'DEMO_THUMBNAIL_MAX_WIDTH', 200)
THUMBNAIL_MAXH = getattr(settings, 'DEMO_THUMBNAIL_MAX_HEIGHT', 150)

RESIZE_METHOD = getattr(settings, 'RESIZE_METHOD', Image.ANTIALIAS)

# HACK: For easier L10N, define tag descriptions in code instead of as a DB model
TAG_DESCRIPTIONS = dict( (x['tag_name'], x) for x in getattr(settings, 'TAG_DESCRIPTIONS', (
    { 
        "tag_name": "audio", 
        "title": _("Audio"), 
        "description": _("Mozilla's Audio Data API extends the current HTML5 API and allows web developers to read and write raw audio data."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/Introducing_the_Audio_API_Extension')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/HTML5_audio')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/html5/video.html#audio')),
        ),
    },
    { 
        "tag_name": "canvas", 
        "title": _("Canvas"),
        "description": _("The HTML5 canvas element allows to display scriptable renderings of 2D shapes and bitmap images."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/HTML/Canvas')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Canvas_element')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/html5/the-canvas-element.html')),
        ),
    },
    { 
        "tag_name": "css3", 
        "title": _("CSS3"), 
        "description": _("Cascading Style Sheets level 3 (CSS3) provide serveral new features and properties to enhance the formatting and look of documents written in different kinds of markup languages like HTML or XML."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/CSS')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Cascading_Style_Sheets')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/css3-roadmap/')),
        ),
    },
    { 
        "tag_name": "device", 
        "title": _("Device"), 
        "description": _("Media queries and orientation events let authors adjust their layout on hand-held devices such as mobile phones."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/Detecting_device_orientation')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/css3-mediaqueries/')),
        ),
    },
    { 
        "tag_name": "files", 
        "title": _("Files"), 
        "description": _("The File API allows web developers to use file objects in web applications, as well as selecting and accessing their data."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/using_files_from_web_applications')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/FileAPI/')),
        ),
    },
    { 
        "tag_name": "fonts", 
        "title": _("Fonts & Type"), 
        "description": _("The CSS3-Font specification contains enhanced features for fonts and typography like  embedding own fonts via @font-face or controlling OpenType font features directly via CSS."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/css/@font-face')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Web_typography')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/css3-fonts/')),
        ),
    },
    { 
        "tag_name": "forms", 
        "title": _("Forms"), 
        "description": _("Form elements and attributes in HTML5 provide a greater degree of semantic mark-up than HTML4 and remove a great deal of the need for tedious scripting and styling that was required in HTML4."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/HTML/HTML5/Forms_in_HTML5')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/HTML_forms')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/html5/forms.html')),
        ),
    },
    { 
        "tag_name": "geolocation", 
        "title": _("Geolocation"), 
        "description": _("The Geolocation API allows web applications to access the user's geographical location."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/En/Using_geolocation')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/W3C_Geolocation_API')),
            (_('W3C Spec'),          _('http://dev.w3.org/geo/api/spec-source.html')),
        ),
    },
    { 
        "tag_name": "javascript",
        "title": _("Javascript"), 
        "description": _("JavaScript is a lightweight, object-oriented programming language, commonly used for scripting interactive behavior on web pages and in web applications."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/javascript')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/JavaScript')),
            (_('ECMA Spec'),         _('http://www.ecma-international.org/publications/standards/Ecma-262.htm')),
        ),
    },
    { 
        "tag_name": "html5",
        "title": _("HTML5"), 
        "description": _("HTML5 is the newest version of the HTML standard, currently under development."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/HTML/HTML5')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Html5')),
            (_('W3C Spec'),          _('http://dev.w3.org/html5/spec/Overview.html')),
        ),
    },
    { 
        "tag_name": "indexeddb", 
        "title": _("IndexedDB"), 
        "description": _("IndexedDB is an API for client-side storage of significant amounts of structured data and for high performance searches on this data using indexes. "),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/IndexedDB')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/IndexedDB')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/IndexedDB/')),
        ),
    },
    { 
        "tag_name": "dragndrop", 
        "title": _("Drag and Drop"), 
        "description": _("Drag and Drop features allow the user to move elements on the screen using the mouse pointer."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/DragDrop/Drag_and_Drop')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Drag-and-drop')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/html5/dnd.html')),
        ),
    },
    { 
        "tag_name": "mobile",
        "title": _("Mobile"), 
        "description": _("Firefox Mobile brings the true Web experience to mobile phones and other non-PC devices."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/En/Mobile')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Mobile_web')),
            (_('W3C Spec'),          _('http://www.w3.org/Mobile/')),
        ),
    },
    { 
        "tag_name": "offlinesupport", 
        "title": _("Offline Support"), 
        "description": _("Offline caching of web applications' resources using the application cache and local storage."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/dom/storage#localStorage')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Web_Storage')),
            (_('W3C Spec'),          _('http://dev.w3.org/html5/webstorage/')),
        ),
    },
    { 
        "tag_name": "svg", 
        "title": _("SVG"), 
        "description": _("Scalable Vector Graphics (SVG) is an XML based language for describing two-dimensional vector graphics."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/SVG')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Scalable_Vector_Graphics')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/SVG11/')),
        ),
    },
    { 
        "tag_name": "video", 
        "title": _("Video"), 
        "description": _("The HTML5 video element provides integrated support for playing video media without requiring plug-ins."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/En/Using_audio_and_video_in_Firefox')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/HTML5_video')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/html5/video.html')),
        ),
    },
    { 
        "tag_name": "webgl", 
        "title": _("WebGL"), 
        "description": _("In the context of the HTML canvas element WebGL provides an API for 3D graphics in the browser."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/WebGL')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/WebGL')),
            (_('Khronos Spec'),      _('http://www.khronos.org/webgl/')),
        ),
    },
    { 
        "tag_name": "websockets", 
        "title": _("WebSockets"), 
        "description": _("WebSockets is a technology that makes it possible to open an interactive  communication session between the user's browser and a server."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/WebSockets')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Web_Sockets')),
            (_('W3C Spec'),          _('http://dev.w3.org/html5/websockets/')),
        ),
    },
    { 
        "tag_name": "webworkers", 
        "title": _("Web Workers"), 
        "description": _("Web Workers provide a simple means for web content to run scripts in background threads."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/En/Using_web_workers')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Web_Workers')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/workers/')),
        ),
    },
    { 
        "tag_name": "xhr", 
        "title": _("XMLHttpRequest"), 
        "description": _("XMLHttpRequest (XHR) is used to send HTTP requests directly to a webserver and load the response data directly back into the script."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/En/XMLHttpRequest/Using_XMLHttpRequest')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/XMLHttpRequest')),
            (_('W3C Spec'),          _('http://www.w3.org/TR/XMLHttpRequest/')),
        ),
    },
    { 
        "tag_name": "multitouch", 
        "title": _("Multi-touch"), 
        "description": _("Track the movement of the user's finger on a touch screen, monitoring the raw touch events generated by the system."),
        "learn_more": (
            (_('MDN Documentation'), _('https://developer.mozilla.org/en/DOM/Touch_events')),
            (_('Wikipedia Article'), _('http://en.wikipedia.org/wiki/Multi-touch')),
            (_('W3C Spec'),          _('http://www.w3.org/2010/webevents/charter/')),
        ),
    },
)))

# HACK: For easier L10N, define license in code instead of as a DB model
DEMO_LICENSES = dict( (x['name'], x) for x in getattr(settings, 'DEMO_LICENSES', (
    { 'name': "cc-by-sa", 
        'title': _("CC-BY-SA Creative Commons Attribution-ShareAlike 3.0 [DEFAULT]") },
    { 'name': "cc-by", 
        'title': _("CC-BY Creative Commons Attribution 3.0") },
    { 'name': "cc-by-no", 
        'title': _("CC-BY-NO Creative Commons Attribution-NonCommercial 3.0") },
    { 'name': "cc-by-no-sa", 
        'title': _("CC-BY-NO-SA Createive Commons Attribution-NonCommercial-ShareAlike 3.0") },
    { 'name': "mpl", 
        'title': _("MPL/GPL/LGPL") },
    { 'name': "gpl", 
        'title': _("GPL") },
    { 'name': "lgpl", 
        'title': _("LGPL") },
    { 'name': "bsd", 
        'title': _("BSD") },
    { 'name': "apache", 
        'title': _("Apache") },
    { 'name': "agpl", 
        'title': _("AGPL") },
    { 'name': "cc-by-nd", 
        'title': _("CC-BY-ND Creative Commons Attribution-NonCommercial-NoDervis") },
    { 'name': "cc-by-no-nd", 
        'title': _("CC-BY-NO-ND Creative Commons Attribution-NoDervis") },
    { 'name': "publicdomain", 
        'title': _("Public Domain") },
    { 'name': "other", 
        'title': _("Other (N/A)") },
)))


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
            if not tag_name in TAG_DESCRIPTIONS:
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


class SubmissionManager(caching.base.CachingManager):
    """Manager for Submission objects"""

    # TODO: Make these search functions into a mixin?

    # See: http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/
    def _normalize_query(self, query_string,
                        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                        normspace=re.compile(r'\s{2,}').sub):
        ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
            and grouping quoted words together.
            Example:
            
            >>> normalize_query('  some random  words "with   quotes  " and   spaces')
            ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
        
        '''
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

    # See: http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/
    def _get_query(self, query_string, search_fields):
        ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.
        
        '''
        query = None # Query to search for every search term        
        terms = self._normalize_query(query_string)
        for term in terms:
            or_query = None # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    def search(self, query_string, sort):
        """Quick and dirty keyword search on submissions"""
        # TODO: Someday, replace this with something like Sphinx or another real search engine
        strip_qs = query_string.strip()
        if not strip_qs:
            return self.all_sorted(sort).order_by('-modified')
        else:
            query = self._get_query(strip_qs, ['title', 'summary', 'description',])
            return self.all_sorted(sort).filter(query).order_by('-modified')

    def all_sorted(self, sort=None):
        """Apply to .all() one of the sort orders supported for views"""
        queryset = self.all()
        if sort == 'launches':
            return queryset.order_by('-launches_total')
        elif sort == 'likes':
            return queryset.order_by('-likes_total')
        elif sort == 'upandcoming':
            return queryset.order_by('-launches_recent','-likes_recent')
        else:
            return queryset.order_by('-created')
        

class Submission(caching.base.CachingMixin, models.Model):
    """Representation of a demo submission"""
    objects = SubmissionManager()

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

    comments_total = models.PositiveIntegerField(default=0)

    launches = ActionCounterField()
    likes = ActionCounterField()

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
            max_length=64, blank=False, 
            choices=( (x['name'], x['title']) for x in DEMO_LICENSES.values() ))

    creator = models.ForeignKey(User, blank=False, null=True)
    
    created = models.DateTimeField( _('date created'), 
            auto_now_add=True, blank=False)
    modified = models.DateTimeField( _('date last modified'), 
            auto_now=True, blank=False)

    def __unicode__(self):
        return 'Submission "%(title)s"' % dict(
            title=self.title )

    def get_absolute_url(self):
        return reverse('demos.views.detail', kwargs={'slug':self.slug})

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
            raise ValidationError(_('ZIP file contains no acceptable files'))

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

def update_submission_comment_count(sender, instance, **kwargs):
    """Update the denormalized count of comments for a submission on comment save/delete"""
    obj = instance.content_object
    if isinstance(obj, Submission):
        new_total = ThreadedComment.public.all_for_object(obj).count()  
        Submission.objects.filter(pk=obj.pk).update(comments_total=new_total)
        Submission.objects.invalidate(obj)

models.signals.post_save.connect(update_submission_comment_count, sender=ThreadedComment)
models.signals.post_delete.connect(update_submission_comment_count, sender=ThreadedComment)
