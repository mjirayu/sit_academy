from django.db import models


class LiveEvent(models.Model):
    title = models.CharField(
        db_index=True,
        max_length=200,
    )
    live = models.BooleanField()
    iframe = models.CharField(db_index=True, max_length=255)
    short_description = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)

    def __unicode__(self):
        return self.title
