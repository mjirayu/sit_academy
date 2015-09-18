import re

from django.db import models
from django.core.validators import RegexValidator

from xmodule_django.models import CourseKeyField

RE_PACKAGE_NAME = re.compile(r'^[-a-zA-Z0-9_() .]+$')


class UploadVideo(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=200,
        validators=[RegexValidator(RE_PACKAGE_NAME, 'Use ASCII characters only')]
    )
    course_id = CourseKeyField(max_length=255, db_index=True)
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    video = models.FileField(
        verbose_name='video',
        upload_to='upload_videos',
        max_length=512,
    )
