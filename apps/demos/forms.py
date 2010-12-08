from hashlib import md5

import zipfile
import tarfile

from django import forms

from django.utils.encoding import smart_unicode, smart_str

from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators
from django.core.exceptions import ValidationError
#from uni_form.helpers import FormHelper, Submit, Reset
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Submission

import django.forms.fields
from django.forms.widgets import CheckboxSelectMultiple

import tagging.forms
from tagging.utils import parse_tag_input

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from PIL import Image
except ImportError:
    import Image


SCREENSHOT_MAXW  = getattr(settings, 'DEMO_SCREENSHOT_MAX_WIDTH', 320)
SCREENSHOT_MAXH = getattr(settings, 'DEMO_SCREENSHOT_MAX_HEIGHT', 240)

THUMBNAIL_MAXW = getattr(settings, 'DEMO_THUMBNAIL_MAX_WIDTH', 100)
THUMBNAIL_MAXH = getattr(settings, 'DEMO_THUMBNAIL_MAX_HEIGHT', 100)

RESIZE_METHOD = getattr(settings, 'RESIZE_METHOD', Image.ANTIALIAS)


class MyModelForm(forms.ModelForm):
    def as_ul(self):
        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            normal_row = u'<li%(html_class_attr)s>%(label)s %(field)s%(help_text)s%(errors)s</li>',
            error_row = u'<li>%s</li>',
            row_ender = '</li>',
            help_text_html = u' <p class="help">%s</p>',
            errors_on_separate_row = False)


class MyForm(forms.Form):
    def as_ul(self):
        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            normal_row = u'<li%(html_class_attr)s>%(label)s %(field)s%(help_text)s%(errors)s</li>',
            error_row = u'<li>%s</li>',
            row_ender = '</li>',
            help_text_html = u' <p class="help">%s</p>',
            errors_on_separate_row = False)


def scale_image(files, img_name, img_max_size):
    """Crop and scale an image in-place in form upload, normalize filename."""
    if img_name not in files:
        return True

    img_upload = files[img_name]
    if not img_upload.file:
        return True

    try:
        img = Image.open(img_upload.file)
    except IOError:
        return False

    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = img_max_size
    dst_ratio = float(dst_width) / float(dst_height)

    if dst_ratio < src_ratio:
        crop_height = src_height
        crop_width = crop_height * dst_ratio
        x_offset = int(float(src_width - crop_width) / 2)
        y_offset = 0
    else:
        crop_width = src_width
        crop_height = crop_width / dst_ratio
        x_offset = 0
        y_offset = int(float(src_height - crop_height) / 3)

    img = img.crop((x_offset, y_offset, 
        x_offset+int(crop_width), y_offset+int(crop_height)))
    img = img.resize((dst_width, dst_height), Image.ANTIALIAS)

    if img.mode != "RGB":
        img = img.convert("RGB")
    new_img = StringIO()
    img.save(new_img, "PNG")
    img_data = new_img.getvalue()

    img_upload.file = ContentFile(img_data)
    img_upload.name = '%s.png' % (md5(img_data).hexdigest())

    return True


class ConstrainedTagWidget(CheckboxSelectMultiple):
    """Checkbox select widget for set of TagDescription objects"""

    def __init__(self, attrs=None, choices=()):
        super(ConstrainedTagWidget, self).__init__(attrs)

        if not choices:
            from .models import TagDescription
            choices = ( (x.tag_name, x.title) 
                    for x in TagDescription.objects.all() )

        self.choices = list(choices)

    def render(self, name, value, attrs=None, choices=()):
        if not isinstance(value, (list, tuple)):
            value = parse_tag_input(value)
        return super(ConstrainedTagWidget, self).render(
                name, value, attrs, choices)


class ConstrainedTagFormField(tagging.forms.TagField):
    """Tag field that constrains its input to the set of available
    TagDescription objects."""

    widget = ConstrainedTagWidget

    def clean(self, value):
        # Concatenate the checkboxes into a string usable by the superclass,
        # but skip superclass' clean() because we'll assume that TagDescription
        # tag names don't exceed the intended MAX_TAG_LENGTH
        return ','.join('"%s"' % x for x in value)


class SubmissionForm(MyModelForm):
    """Form accepting demo submissions"""

    class Meta:
        model = Submission
        fields = (
            'title', 'description', 'tags',
            'demo_package', 'screenshot', 'thumbnail',
            'more_info_url', 'source_code_url',
        )

    def clean(self):
        cleaned_data = super(SubmissionForm, self).clean()

        # TODO: Should this be moved to model class?
        # If so, how to use screenshot for thumbnail if thumbnail not uploaded?

        if 'screenshot' in self.files and 'thumbnail' not in self.files:
            sf = self.files['screenshot']
            self.files['thumbnail'] = InMemoryUploadedFile(
                ContentFile(sf.file.getvalue()), 'thumbnail',
                sf.name, sf.content_type, sf.size, sf.charset)
            self.cleaned_data['thumbnail'] = self.files['thumbnail']

        if 'screenshot' in self.files:
            if not scale_image(self.files, 'screenshot',
                    ( SCREENSHOT_MAXW, SCREENSHOT_MAXH ) ):
                self._errors['screenshot'] = self.error_class(
                        [_('Cannot process screenshot image')])

        if 'thumbnail' in self.files:
            if not scale_image(self.files, 'thumbnail',
                    ( THUMBNAIL_MAXW, THUMBNAIL_MAXH ) ):
                self._errors['thumbnail'] = self.error_class(
                        [_('Cannot process thumbnail image')])

        return cleaned_data
