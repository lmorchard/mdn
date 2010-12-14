"""Models for activity counters"""

import logging

from django.db import models
from django.conf import settings
from django.db.models import F

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from django.utils.translation import ugettext_lazy as _

from .utils import get_ip, get_unique


class ActionManager(models.Manager):
    """Manager for actions"""

    _action_cache = dict()

    def __getitem__(self, key):
        """Simplified accessor for actions.

        eg. Actions.objects['like'].increment(...)
        """
        if key not in self._action_cache:
            action, created = Action.objects.get_or_create(name=key, 
                    defaults=dict( max_per_unique=1 ))
            self._action_cache[key] = action
        return self._action_cache[key]


class Action(models.Model):
    """Action counted for objects"""
    objects = ActionManager()

    name = models.CharField(
            _('name of the action'),
            max_length=64, db_index=True, blank=False)
    max_per_unique = models.IntegerField( default=1 )

    def __unicode__(self):
        return "Action(%s)" % ( self.name )

    def get_counter(self, object, create=True):
        content_type = ContentType.objects.get_for_model(object)
        if create:
            return ActionCounter.objects.get_or_create(action=self,
                    content_type=content_type, object_pk=object.pk)
        else:
            try:
                return ( ActionCounter.objects.get(action=self,
                        content_type=content_type, object_pk=object.pk), False )
            except ActionCounter.DoesNotExist:
                return ( None, False )

    def increment(self, request, object):
        counter, created = self.get_counter(object)
        return counter.increment(request)

    def get_total(self, object):
        counter, created = self.get_counter(object, False)
        return counter and counter.total or 0

    def get_total_for_request(self, object, request):
        counter, created = self.get_counter(object, False)
        return counter and counter.get_total_for_request(request) or 0


class ActionCounterManager(models.Manager):
    """Manager for action counters"""
    pass


class ActionCounter(models.Model):
    """Count of actions taken on an object"""
    objects = ActionCounterManager()

    action = models.ForeignKey(Action, editable=False)
    total = models.PositiveIntegerField(default=0)
    content_type = models.ForeignKey(
            ContentType,
            verbose_name="content cype",
            related_name="content_type_set_for_%(class)s",)
    object_pk = models.TextField(
            _('object ID'))
    content_object = generic.GenericForeignKey(
            'content_type', 'object_pk')
    modified = models.DateTimeField( 
            _('date last modified'), 
            auto_now=True, blank=False)

    def __unicode__(self):
        return "ActionCounter(%s / %s)" % ( self.action, self.content_object )

    def get_hit(self, request, create=True):
        user, ip, user_agent, session_key = get_unique(request)
        if create:
            return ActionHit.objects.get_or_create(
                    counter=self, ip=ip, user_agent=user_agent, user=user,
                    session_key=session_key,
                    defaults=dict( total=0 ))
        else:
            try:
                return ( ActionHit.objects.get(
                        counter=self, ip=ip, user_agent=user_agent, user=user,
                        session_key=session_key), False )
            except ActionHit.DoesNotExist:
                return ( None, False )

    def increment(self, request):
        hit, created = self.get_hit(request)

        if (hit.total + 1) > self.action.max_per_unique:
            return False
        hit.increment()

        self.total = F('total') + 1
        self.save()

        return ( self.total, hit.total, )

    def get_total_for_request(self, request):
        hit, created = self.get_hit(request, False)
        return hit and hit.total or 0


class ActionHitManager(models.Manager):
    """Manager for action hits"""


class ActionHit(models.Model):
    """Record of an action having been taken on an object"""
    objects = ActionHitManager()

    counter = models.ForeignKey(ActionCounter, editable=False)
    total = models.IntegerField()

    ip = models.CharField(max_length=40, editable=False, blank=True, null=True)
    session_key = models.CharField(max_length=40, editable=False, blank=True, null=True)
    user_agent = models.CharField(max_length=255, editable=False, blank=True, null=True)
    user = models.ForeignKey(User, editable=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=False, editable=False)

    class Meta:
        ordering = ( '-created', )
        get_latest_by = 'created'

    def __unicode__(self):
        return u'Hit: %s' % self.pk

    def increment(self):
        self.total = F('total') + 1
        self.save()
        
