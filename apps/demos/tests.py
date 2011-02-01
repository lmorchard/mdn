import logging
import re
import urlparse
import time
import zipfile
from os import unlink
from os.path import basename, dirname, isfile, isdir
from shutil import rmtree

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
        """Exercise zip file validation by throwing through various invalid and valid zip files."""

        s = Submission(title='Hello world', slug='hello-world',
            description='This is a hello world demo',
            video_url='http://www.youtube.com/watch?v=dQw4w9WgXcQ',
            tags='hello,world,demo,play', creator=self.user)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(False, "There should be a validation exception")
        except ValidationError, e:
            ok_('ZIP file contains no acceptable files' in e.messages)

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('play/index.html', """<html> </html>""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(False, "There should be a validation exception")
        except ValidationError, e:
            ok_('HTML index not found in ZIP' in e.messages)

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('js/demo.js', """alert('hi')""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(False, "There should be a validation exception")
        except ValidationError, e:
            ok_('HTML index not found in ZIP' in e.messages)

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('/etc/passwd', """HAXXORED""")
        zf.writestr('../../../../etc/passwd', """HAXXORED""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(False, "There should be a validation exception")
        except ValidationError, e:
            ok_('ZIP file contains no acceptable files' in e.messages)

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('index.html', """<html> </html>""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(True, "This last one should be okay")
        except:
            ok_(False, "The last zip file should have been okay")

        unlink(s.demo_package.path)

        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('demo.html', """<html> </html>""")
        zf.close()
        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))

        try:
            s.clean()
            ok_(True, "This last one should be okay")
        except:
            ok_(False, "The last zip file should have been okay")

        unlink(s.demo_package.path)

    def test_process_demo_package(self):
        """Ensure that process_demo_package() results in a directory of demo files"""
        
        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')

        zf.writestr('index.html',
            """<html>
                <head>
                    <link rel="stylesheet" href="css/main.css" type="text/css" />
                </head>
                <body>
                    <h1>Hello world</h1>
                    <script type="text/javascript" src="js/main.js"></script>
                </body>
            </html>""")

        zf.writestr('css/main.css',
            'h1 { color: red }')
        
        zf.writestr('js/main.js',
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

        path = s.demo_package.path.replace('.zip', '')
        
        ok_(isdir(path))
        ok_(isfile('%s/index.html' % path))
        ok_(isfile('%s/css/main.css' % path))
        ok_(isfile('%s/js/main.js' % path))
        
        rmtree(path)

    def test_demo_html_normalized(self):
        """Ensure a demo.html in zip file is normalized to index.html when unpacked"""
        
        fout = StringIO()
        zf = zipfile.ZipFile(fout, 'w')
        zf.writestr('demo.html', """<html></html""")
        zf.writestr('css/main.css', 'h1 { color: red }')
        zf.writestr('js/main.js', 'alert("HELLO WORLD");')
        zf.close()

        s = Submission(title='Hello world', slug='hello-world',
            description='This is a hello world demo',
            tags='hello,world,demo,play', creator=self.user)

        s.demo_package.save('play_demo.zip', ContentFile(fout.getvalue()))
        s.demo_package.close()
        s.clean()
        s.save()

        s.process_demo_package()

        path = s.demo_package.path.replace('.zip', '')
        
        ok_(isdir(path))
        ok_(isfile('%s/index.html' % path))
        ok_(isfile('%s/css/main.css' % path))
        ok_(isfile('%s/js/main.js' % path))
        
        rmtree(path)
