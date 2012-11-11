# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from emailusernames.utils import migrate_usernames

class Migration(DataMigration):

    def forwards(self, orm):
        migrate_usernames()

    def backwards(self, orm):
        pass

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
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
    symmetrical = True
