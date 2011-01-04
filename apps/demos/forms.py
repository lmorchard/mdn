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

from . import scale_image
from .models import Submission, DEMO_LICENSES

from captcha.fields import ReCaptchaField

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
        if not isinstance(value, (list, tuple)):
            return value
        else:
            return ','.join('"%s"' % x for x in value)


class SubmissionEditForm(MyModelForm):
    """Form accepting demo submissions"""

    class Meta:
        model = Submission
        fields = (
            'title', 'summary', 'description', 'tags',
            'screenshot_1', 'screenshot_2', 'screenshot_3', 
            'screenshot_4', 'screenshot_5', 
            'video_url', 
            'demo_package', 'source_code_url', 'license_name',
        )

    def clean(self):
        cleaned_data = super(SubmissionEditForm, self).clean()

        if 'demo_package' in self.files:
            try:
                demo_package = self.files['demo_package']
                Submission.validate_demo_zipfile(demo_package)
            except ValidationError, e:
                self._errors['demo_package'] = self.error_class(e.messages)

        # TODO: Should this be moved to model class?
        for idx in range(1, 6):
            name = 'screenshot_%s' % idx
            if name in self.files:
                scaled_file = scale_image(self.files[name].file,
                        (SCREENSHOT_MAXW, SCREENSHOT_MAXH))
                if not scaled_file:
                    self._errors[name] = self.error_class([_('Cannot process image')])
                else:
                    self.files[name].file = scaled_file

        return cleaned_data


class SubmissionNewForm(SubmissionEditForm):

    class Meta(SubmissionEditForm.Meta):
        fields = SubmissionEditForm.Meta.fields + ( 'captcha', 'accept_terms', )

    captcha = ReCaptchaField(label=_('Are you human?')) 
    accept_terms = forms.BooleanField(initial=False, required=True)


