"""
Defines the URL routes for this app.
"""

from .accounts.views import AccountView
from .preferences.views import PreferencesView, PreferencesDetailView
from .user_events.views import UserEventView, UserEventDetailView
from .reminder_notes.views import ReminderNoteView, ReminderNoteDetailView

from django.conf.urls import patterns, url

USERNAME_PATTERN = r'(?P<username>[\w.+-]+)'

urlpatterns = patterns(
    '',
    url(
        r'^v1/accounts/' + USERNAME_PATTERN + '$',
        AccountView.as_view(),
        name="accounts_api"
    ),
    url(
        r'^v1/preferences/' + USERNAME_PATTERN + '$',
        PreferencesView.as_view(),
        name="preferences_api"
    ),
    url(
        r'^v1/preferences/' + USERNAME_PATTERN + '/(?P<preference_key>[a-zA-Z0-9_]+)$',
        PreferencesDetailView.as_view(),
        name="preferences_detail_api"
    ),
    url(
        r'^v1/events/$',
        UserEventView.as_view(),
        name="user_event_api"
    ),
    url(
        r'^v1/events/(?P<pk>[0-9]+)$',
        UserEventDetailView.as_view(),
        name="user_event_detail_api"
    ),
    url(
        r'^v1/reminders/$',
        ReminderNoteView.as_view(),
        name="reminder_note_api"
    ),
    url(
        r'^v1/reminders/(?P<pk>[0-9]+)$',
        ReminderNoteDetailView.as_view(),
        name="reminder_note_detail_api"
    ),
)
