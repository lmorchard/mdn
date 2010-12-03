import logging
import re
import urlparse
import time
import zipfile
from os import unlink
from os.path import basename, dirname, isfile

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.core.files.base import ContentFile

from nose.tools import assert_equal, with_setup, assert_false, eq_, ok_
from nose.plugins.attrib import attr

from demos.models import Submission

class DemoPackageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('tester', 'tester@tester.com', 'tester')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_demo_package_validation(self):
        """Exercise demo zip file validation by throwing through various
        invalid and valid zip files."""

        s = Submission(title='Hello world', slug='hello-world',
            description='This is a hello world demo',
            tags='hello,world,demo,play', creator=self.user)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(False, "There should be a validation exception")
        except ValidationError, e:
            ok_('Demo package is not a valid zip file' in e.messages)

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('play_demo/demo.js', """alert('hi')""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(False, "There should be a validation exception")
        except ValidationError, e:
            ok_('Demo package does not contain demo.html' in e.messages)

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('play_demo/demo.html', """alert('hi')""")
        zf.writestr('/etc/passwd', """HAXXORED""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(False, "There should be a validation exception")
        except ValidationError, e:
            ok_('Demo package contains invalid file entries' in e.messages)

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('play_demo/demo.html', """alert('hi')""")
        zf.writestr('play_demo/../../../../etc/passwd', """HAXXORED""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(False, "There should be a validation exception")
        except ValidationError, e:
            ok_('Demo package contains invalid file entries' in e.messages)

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('play_demo/demo.html',
            """<html> </html>""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(True, "This last one should be okay")
        except:
            ok_(False, "The last zip file should have been okay")

        unlink(s.demo_package.path)


    def test_process_demo_package(self):
        
        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')

        zf.writestr('play_demo/demo.html',
            """<html>
                <head>
                    <link rel="stylesheet" href="css/main.css" type="text/css" />
                </head>
                <body>
                    <h1>Hello world</h1>
                    <script type="text/javascript" src="js/main.js"></script>
                </body>
            </html>""")

        zf.writestr('play_demo/css/main.css',
            'h1 { color: red }')
        
        zf.writestr('play_demo/js/main.js',
            'alert("HELLO WORLD");')
        
        zf.close()

        s = Submission(title='Hello world', slug='hello-world',
            description='This is a hello world demo',
            tags='hello,world,demo,play', creator=self.user)

        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))
        s.demo_package.close()
        s.clean()
        s.save()

        s.process_demo_package()

        ok_(False)

