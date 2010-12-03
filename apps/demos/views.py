import jingo

from django.conf import settings

from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden

from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from django.contrib.auth.views import AuthenticationForm 

from devmo import (SECTION_USAGE, SECTION_ADDONS, SECTION_APPS, SECTION_MOBILE,
                   SECTION_WEB)
from feeder.models import Bundle, Feed

from tagging.models import Tag, TaggedItem
from tagging.utils import LINEAR, LOGARITHMIC

from voting.models import Vote

from demos.models import Submission
from demos.forms import SubmissionForm

def _get_tweets():
    tweets = []
    for section in SECTION_USAGE:
        tweets += Bundle.objects.recent_entries(section.twitter)[:2]
    tweets.sort(key=lambda t: t.last_published, reverse=True)
    return tweets

def home(request):
    """Home page."""
    
    top_list = Vote.objects.get_top(Submission, 25)
    submissions = [ x[0] for x in top_list ]
    scores = [ x[1] for x in top_list ]
    
    login_form = AuthenticationForm()

    return jingo.render(request, 'demos/home.html', {
        'login_form': login_form,
        'tweets': _get_tweets(), 
        'submission_list': submissions })

def detail(request, slug):
    """Detail page for a submission"""
    submission = get_object_or_404(Submission, slug=slug)
    
    return jingo.render(request, 'demos/detail.html', {
        'tweets': _get_tweets(), 'submission': submission })

def submit(request):
    """Accept submission of a demo"""

    if request.method != "POST":
        form = SubmissionForm()
    else:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            new_sub = form.save(commit=False)
            new_sub.creator = request.user
            new_sub.slug = slugify(new_sub.title)
            new_sub.save()
            # TODO: Process in a cronjob
            new_sub.process_demo_package()
            return HttpResponseRedirect(reverse(
                'demos.views.detail', args=(new_sub.slug,)))

    return jingo.render(request, 'demos/submit.html', { 'form': form })

def edit(request, slug):
    submission = get_object_or_404(Submission, slug=slug)

    if request.method != "POST":
        form = SubmissionForm(instance=submission)
    else:
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.slug = slugify(sub.title)
            sub.save()
            # TODO: Process in a cronjob
            sub.process_demo_package()
            return HttpResponseRedirect(reverse(
                'demos.views.detail', args=(sub.slug,)))

    return jingo.render(request, 'demos/edit.html', { 'form': form })

