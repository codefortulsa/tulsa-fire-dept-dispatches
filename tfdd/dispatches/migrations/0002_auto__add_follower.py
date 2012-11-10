# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Follower'
        db.create_table('dispatches_follower', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone_number', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('dispatches', ['Follower'])

        # Adding M2M table for field units on 'Follower'
        db.create_table('dispatches_follower_units', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('follower', models.ForeignKey(orm['dispatches.follower'], null=False)),
            ('unit', models.ForeignKey(orm['dispatches.unit'], null=False))
        ))
        db.create_unique('dispatches_follower_units', ['follower_id', 'unit_id'])


    def backwards(self, orm):
        # Deleting model 'Follower'
        db.delete_table('dispatches_follower')

        # Removing M2M table for field units on 'Follower'
        db.delete_table('dispatches_follower_units')


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
        'dispatches.follower': {
            'Meta': {'object_name': 'Follower'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.TextField', [], {}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dispatches.Unit']", 'symmetrical': 'False'})
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