# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dispatch'
        db.create_table('dispatches_dispatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('call_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('call_type_desc', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dispatched', self.gf('django.db.models.fields.DateTimeField')()),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('map_page', self.gf('django.db.models.fields.IntegerField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('tf', self.gf('django.db.models.fields.IntegerField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('dispatches', ['Dispatch'])


    def backwards(self, orm):
        # Deleting model 'Dispatch'
        db.delete_table('dispatches_dispatch')


    models = {
        'dispatches.dispatch': {
            'Meta': {'object_name': 'Dispatch'},
            'call_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'call_type_desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'dispatched': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'map_page': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'tf': ('django.db.models.fields.IntegerField', [], {}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['dispatches']