from hashlib import md5

from django import forms

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

from demos.models import Submission


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from PIL import Image
except ImportError:
    import Image


SCREENSHOT_MAX_WIDTH  = getattr(settings, 'DEMO_SCREENSHOT_MAX_WIDTH', 320)
SCREENSHOT_MAX_HEIGHT = getattr(settings, 'DEMO_SCREENSHOT_MAX_HEIGHT', 240)

THUMBNAIL_MAX_WIDTH  = getattr(settings, 'DEMO_THUMBNAIL_MAX_WIDTH', 100)
THUMBNAIL_MAX_HEIGHT = getattr(settings, 'DEMO_THUMBNAIL_MAX_HEIGHT', 100)

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
        return

    img_upload = files[img_name]

    img = Image.open(img_upload.file)

    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = img_max_size
    dst_ratio = float(dst_width) / float(dst_height)

    if dst_ratio < src_ratio:
        crop_height = src_height
        crop_width = crop_height * dst_ratio
        x_offset = float(src_width - crop_width) / 2
        y_offset = 0
    else:
        crop_width = src_width
        crop_height = crop_width / dst_ratio
        x_offset = 0
        y_offset = float(src_height - crop_height) / 3

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


class SubmissionForm(MyModelForm):

    class Meta:
        model = Submission
        fields = (
            'title', 'description', 'tags',
            'demo_package', 'screenshot', 'thumbnail',
            'launch_url', 'more_info_url', 'source_code_url',
        )

    def clean(self):

        cleaned_data = super(SubmissionForm, self).clean()

        if 'screenshot' in self.files and 'thumbnail' not in self.files:
            sf = self.files['screenshot']
            self.files['thumbnail'] = InMemoryUploadedFile(
                ContentFile(sf.file.getvalue()), 'thumbnail',
                sf.name, sf.content_type, sf.size, sf.charset)
            self.cleaned_data['thumbnail'] = self.files['thumbnail']

        if 'screenshot' in self.files:
            scale_image(self.files, 'screenshot',
                ( SCREENSHOT_MAX_WIDTH, SCREENSHOT_MAX_HEIGHT ) )

        if 'thumbnail' in self.files:
            scale_image(self.files, 'thumbnail',
                ( THUMBNAIL_MAX_WIDTH, THUMBNAIL_MAX_HEIGHT ) )

        return cleaned_data

