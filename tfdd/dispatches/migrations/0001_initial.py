# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Unit'
        db.create_table('dispatches_unit', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
        ))
        db.send_create_signal('dispatches', ['Unit'])

        # Adding model 'Dispatch'
        db.create_table('dispatches_dispatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('call_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('call_type_desc', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('dispatched', self.gf('django.db.models.fields.DateTimeField')()),
            ('map_page', self.gf('django.db.models.fields.IntegerField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('tf', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('dispatches', ['Dispatch'])

        # Adding M2M table for field units on 'Dispatch'
        db.create_table('dispatches_dispatch_units', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dispatch', models.ForeignKey(orm['dispatches.dispatch'], null=False)),
            ('unit', models.ForeignKey(orm['dispatches.unit'], null=False))
        ))
        db.create_unique('dispatches_dispatch_units', ['dispatch_id', 'unit_id'])

        # Adding model 'RawDispatch'
        db.create_table('dispatches_rawdispatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dispatch', self.gf('django.db.models.fields.related.OneToOneField')(related_name='raw', unique=True, to=orm['dispatches.Dispatch'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('received', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('dispatches', ['RawDispatch'])


    def backwards(self, orm):
        # Deleting model 'Unit'
        db.delete_table('dispatches_unit')

        # Deleting model 'Dispatch'
        db.delete_table('dispatches_dispatch')

        # Removing M2M table for field units on 'Dispatch'
        db.delete_table('dispatches_dispatch_units')

        # Deleting model 'RawDispatch'
        db.delete_table('dispatches_rawdispatch')


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
            'tf': ('django.db.models.fields.IntegerField', [], {}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'dispatches'", 'symmetrical': 'False', 'to': "orm['dispatches.Unit']"})
        },
        'dispatches.rawdispatch': {
            'Meta': {'object_name': 'RawDispatch'},
            'dispatch': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'raw'", 'unique': 'True', 'to': "orm['dispatches.Dispatch']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'dispatches.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'})
        }
    }

    complete_apps = ['dispatches']