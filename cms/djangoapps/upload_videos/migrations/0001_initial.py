# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UploadVideo'
        db.create_table('upload_videos_uploadvideo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('course_id', self.gf('xmodule_django.models.CourseKeyField')(max_length=255, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_index=True, blank=True)),
            ('video', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
        ))
        db.send_create_signal('upload_videos', ['UploadVideo'])


    def backwards(self, orm):
        # Deleting model 'UploadVideo'
        db.delete_table('upload_videos_uploadvideo')


    models = {
        'upload_videos.uploadvideo': {
            'Meta': {'object_name': 'UploadVideo'},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['upload_videos']
