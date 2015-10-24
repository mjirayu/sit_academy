from edxmako.shortcuts import render_to_response
from django.http import HttpResponse


def index(request):
    return render_to_response('record_webrtc/record.html')
