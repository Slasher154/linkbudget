# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UplinkDefinedContour'
        db.create_table(u'linkbudget_uplinkdefinedcontour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.UplinkBeam'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['UplinkDefinedContour'])


    def backwards(self, orm):
        # Deleting model 'UplinkDefinedContour'
        db.delete_table(u'linkbudget_uplinkdefinedcontour')


    models = {
        u'linkbudget.uplinkbeam': {
            'Meta': {'object_name': 'UplinkBeam'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'peak_gt': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.uplinkdefinedcontour': {
            'Meta': {'object_name': 'UplinkDefinedContour'},
            'beam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.UplinkBeam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['linkbudget']