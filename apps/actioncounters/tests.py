import logging
import time

from django.conf import settings
from django.db import connection

from django.contrib.auth.models import AnonymousUser

from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from nose.tools import assert_equal, with_setup, assert_false, eq_, ok_
from nose.plugins.attrib import attr

from .models import Action, ActionCounter, ActionHit

class DemoPackageTest(TestCase):

    def setUp(self):
        settings.DEBUG = True

        self.user1 = User.objects.create_user('tester1', 
                'tester2@tester.com', 'tester1')
        self.user1.save()

        self.user2 = User.objects.create_user('tester2', 
                'tester2@tester.com', 'tester2')
        self.user2.save()

    def tearDown(self):
        #for sql in connection.queries:
        #    logging.debug("SQL %s" % sql)
        pass

    def mk_request(self, user=None, session_key=None, ip='192.168.123.123', 
            user_agent='FakeBrowser 1.0'):
        request = HttpRequest()
        request.user = user and user or AnonymousUser()
        if session_key:
            request.session = Session()
            request.session.session_key = session_key
        request.method = 'GET'
        request.META['REMOTE_ADDR'] = ip
        request.META['HTTP_USER_AGENT'] = user_agent
        return request

    def test_basic_action_increment(self):
        """Action attempted with several different kinds of unique identifiers"""

        # get an action for "like" using the __getitem__ interface
        action = Action.objects['like']

        # set up request for anonymous user #1
        request = self.mk_request()

        # anonymous user #1 likes user2
        action.increment(request=request, object=self.user2)
        eq_(1, action.get_total(object=self.user2))

        # anonymous user #1 likes user2, again
        action.increment(request=request, object=self.user2)
        eq_(1, action.get_total(object=self.user2))

        # set up request for anonymous user #2
        request = self.mk_request(ip='192.168.123.1')

        # anonymous user #2 likes user2
        action.increment(request=request, object=self.user2)
        eq_(2, action.get_total(object=self.user2))

        # anonymous user #2 likes user2, again
        action.increment(request=request, object=self.user2)
        eq_(2, action.get_total(object=self.user2))

        # set up request for authenticated user1
        request = self.mk_request(user=self.user1)

        # authenticated user1 likes user2
        action.increment(request=request, object=self.user2)
        eq_(3, action.get_total(object=self.user2))

        # authenticated user1 likes user2, again
        action.increment(request=request, object=self.user2)
        eq_(3, action.get_total(object=self.user2))

        # authenticated user1 likes user2, again, from another IP
        request.META['REMOTE_ADDR'] = '192.168.123.50'
        action.increment(request=request, object=self.user2)
        eq_(3, action.get_total(object=self.user2))

        # set up request for user agent Mozilla 1.0
        request = self.mk_request(ip='192.168.123.50', user_agent='Mozilla 1.0')
        Action.objects['like'].increment(request=request, object=self.user2)
        eq_(4, action.get_total(object=self.user2))

        # set up request for user agent Safari 1.0
        request = self.mk_request(ip='192.168.123.50', user_agent='Safari 1.0')
        Action.objects['like'].increment(request=request, object=self.user2)
        eq_(5, action.get_total(object=self.user2))


    def test_action_with_max(self):
        """Action with a max_per_unique greater than 1"""
        MAX = 5

        # get an action for "rate"
        action, created = Action.objects.get_or_create(name='rate', 
                defaults=dict( max_per_unique=MAX ))

        request = self.mk_request(ip='192.168.123.123')
        for x in range(1, MAX+1):
            action.increment(request=request, object=self.user2)
            eq_(x, action.get_total(object=self.user2))

        action.increment(request=request, object=self.user2)
        eq_(MAX, action.get_total(object=self.user2))

        action.increment(request=request, object=self.user2)
        eq_(MAX, action.get_total(object=self.user2))

    def test_action_count_per_unique(self):
        """Exercise action counts per unique and ensure overall total works"""
        MAX = 5
        UNIQUES = ( 
            dict(user=self.user1),
            dict(user=self.user2),
            dict(ip='192.168.123.123'), 
            dict(ip='192.168.123.150', user_agent="Safari 1.0"), 
            dict(ip='192.168.123.150', user_agent="Mozilla 1.0"), 
            dict(ip='192.168.123.160'), 
        )

        action, created = Action.objects.get_or_create(name='view', 
                defaults=dict( max_per_unique=MAX ))

        for unique in UNIQUES:
            request = self.mk_request(**unique)

            for x in range(1, MAX+1):
                action.increment(request=request, object=self.user2)
                eq_(x, action.get_total_for_request(object=self.user2, request=request))

            action.increment(request=request, object=self.user2)
            action.increment(request=request, object=self.user2)
            eq_(MAX, action.get_total_for_request(object=self.user2, request=request))

        eq_(MAX * len(UNIQUES), action.get_total(object=self.user2))

    def test_count_starts_at_zero(self):
        """Make sure initial count is zero.

        Sounds dumb, but it was a bug at one point."""
        action = Action.objects['like']
        request = self.mk_request()
        eq_(0, action.get_total_for_request(object=self.user2, request=request))

