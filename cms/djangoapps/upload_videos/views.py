from edxmako.shortcuts import render_to_response

from django import http
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.decorators.http import require_http_methods

from xmodule.modulestore.django import modulestore
from opaque_keys.edx.keys import CourseKey

from .models import UploadVideo
from .forms import UploadVideoForm


def video_list(request, course_key_string=None):
    course_key = CourseKey.from_string(course_key_string)
    course_module = modulestore().get_course(course_key)

    upload_videos = UploadVideo.objects.all()

    return render_to_response('video_upload/video_list.html', {
        'context_course': course_module,
        'course_key': course_key_string,
        'upload_videos': upload_videos,
        'site_name': settings.SITE_NAME,
    })


def video_upload(request, course_key_string, instance=None):
    course_key = CourseKey.from_string(course_key_string)
    course_module = modulestore().get_course(course_key)

    status = 200
    if request.method == 'POST':
        form = UploadVideoForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save()
            return http.HttpResponseRedirect(
                reverse('video_list', kwargs={'course_key_string': course_key_string})
            )
        else:
            status = 422
    else:
        form = UploadVideoForm(instance=instance)

    return render_to_response('video_upload/video_form.html', {
        'context_course': course_module,
        'course_key': course_key_string,
        'form': form,
    })
