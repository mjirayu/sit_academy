from django import shortcuts
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from edxmako.shortcuts import render_to_response
from .models import LiveEvent


def event_list(request):
    live_events = LiveEvent.objects.filter(
        live=1
    )

    record_events = LiveEvent.objects.filter(
        live=0
    )
    paginator = Paginator(record_events, 10)
    
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render_to_response('events/index.html', {
        'live_events': live_events,
        'record_events': contacts,
        'site_name': settings.SITE_NAME
    })

def detail(request, slug):
    single_event = LiveEvent.objects.get(
        slug=slug
    )

    return render_to_response('events/detail.html', {
        'single_event': single_event
    })
