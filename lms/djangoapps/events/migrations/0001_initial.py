# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LiveEvent'
        db.create_table('events_liveevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('iframe', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, db_index=True, blank=True)),
        ))
        db.send_create_signal('events', ['LiveEvent'])


    def backwards(self, orm):
        # Deleting model 'LiveEvent'
        db.delete_table('events_liveevent')


    models = {
        'events.liveevent': {
            'Meta': {'object_name': 'LiveEvent'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iframe': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_description': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['events']