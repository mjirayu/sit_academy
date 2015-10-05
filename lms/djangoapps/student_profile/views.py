""" Views for a student's profile information. """
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_countries import countries

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.http import require_http_methods

from branding.views import get_course_enrollments
from edxmako.shortcuts import render_to_response
from openedx.core.djangoapps.user_api.accounts.api import get_account_settings
from openedx.core.djangoapps.user_api.accounts.serializers import PROFILE_IMAGE_KEY_PREFIX
from openedx.core.djangoapps.user_api.errors import UserNotFound, UserNotAuthorized
from openedx.core.djangoapps.user_api.preferences.api import get_user_preferences
from student.models import User, UserSyncCourse, UserProfile, UserEvent
from microsite_configuration import microsite
from xmodule.modulestore.django import modulestore


@login_required
@require_http_methods(['GET'])
def learner_profile(request, username):
    """Render the profile page for the specified username.

    Args:
        request (HttpRequest)
        username (str): username of user whose profile is requested.

    Returns:
        HttpResponse: 200 if the page was sent successfully
        HttpResponse: 302 if not logged in (redirect to login page)
        HttpResponse: 405 if using an unsupported HTTP method
    Raises:
        Http404: 404 if the specified user is not authorized or does not exist

    Example usage:
        GET /account/profile
    """

    user_sync = UserSyncCourse.objects.get(user=request.user.id)
    course_list = []

    if user_sync.sync:
        list_enroll = get_course_enrollments(request.user.id)

        for enroll_course in list_enroll:
            course = modulestore().get_course(enroll_course.course_id)
            course_list.append(course)

        add_event_when_sync(course_list, request.user.id)

    try:
        return render_to_response(
            'student_profile/learner_profile.html',
            learner_profile_context(request.user, username, request.user.is_staff, request.build_absolute_uri)
        )
    except (UserNotAuthorized, UserNotFound, ObjectDoesNotExist):
        raise Http404


def learner_profile_context(logged_in_user, profile_username, user_is_staff, build_absolute_uri_func):
    """Context for the learner profile page.

    Args:
        logged_in_user (object): Logged In user.
        profile_username (str): username of user whose profile is requested.
        user_is_staff (bool): Logged In user has staff access.
        build_absolute_uri_func ():

    Returns:
        dict

    Raises:
        ObjectDoesNotExist: the specified profile_username does not exist.
    """
    profile_user = User.objects.get(username=profile_username)

    own_profile = (logged_in_user.username == profile_username)

    account_settings_data = get_account_settings(logged_in_user, profile_username)
    # Account for possibly relative URLs.
    for key, value in account_settings_data['profile_image'].items():
        if key.startswith(PROFILE_IMAGE_KEY_PREFIX):
            account_settings_data['profile_image'][key] = build_absolute_uri_func(value)

    preferences_data = get_user_preferences(profile_user, profile_username)

    sync_course = UserSyncCourse.objects.get(user=logged_in_user.id)

    context = {
        'data': {
            'profile_username': profile_user.username,
            'profile_user_id': profile_user.id,
            'default_public_account_fields': settings.ACCOUNT_VISIBILITY_CONFIGURATION['public_fields'],
            'default_visibility': settings.ACCOUNT_VISIBILITY_CONFIGURATION['default_visibility'],
            'accounts_api_url': reverse("accounts_api", kwargs={'username': profile_username}),
            'preferences_api_url': reverse('preferences_api', kwargs={'username': profile_username}),
            'preferences_data': preferences_data,
            'account_settings_data': account_settings_data,
            'profile_image_upload_url': reverse('profile_image_upload', kwargs={'username': profile_username}),
            'profile_image_remove_url': reverse('profile_image_remove', kwargs={'username': profile_username}),
            'profile_image_max_bytes': settings.PROFILE_IMAGE_MAX_BYTES,
            'profile_image_min_bytes': settings.PROFILE_IMAGE_MIN_BYTES,
            'account_settings_page_url': reverse('account_settings'),
            'has_preferences_access': (logged_in_user.username == profile_username or user_is_staff),
            'own_profile': own_profile,
            'country_options': list(countries),
            'language_options': settings.ALL_LANGUAGES,
            'platform_name': microsite.get_value('platform_name', settings.PLATFORM_NAME),
        },
        'disable_courseware_js': True,
        'sync_course': sync_course.sync,
    }
    return context


def sync_course(request, username):
    user = User.objects.get(
        username=username
    )
    user_profile = UserProfile.objects.get(
        user=user.id
    )

    user_sync = UserSyncCourse.objects.get(
        user=user_profile.id
    )

    user_sync.sync = int(request.POST.get('sync'))
    user_sync.save()

    return HttpResponseRedirect('/')


def add_event_when_sync(course_list, user_id):
    for course in course_list:
        for chapter in course.get_children():
            for section in chapter.get_children():
                if section.format and section.due:
                    user_profile = UserProfile.objects.get(
                        user=user_id
                    )
                    all_events = UserEvent.objects.filter(
                        user=user_profile
                    )
                    if all_events:
                        for event in all_events:
                            if event.title != course.id.course + ' ' + section.format:
                                UserEvent.objects.create(
                                    user=user_profile,
                                    title=course.id.course + ' ' + section.format,
                                    start=section.due,
                                    end=section.due
                                )
                    else:
                        UserEvent.objects.create(
                            user=user_profile,
                            title=course.id.course + ' ' + section.format,
                            start=section.due,
                            end=section.due
                        )
