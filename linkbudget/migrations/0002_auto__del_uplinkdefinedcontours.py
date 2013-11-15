# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UplinkDefinedContours'
        db.delete_table(u'linkbudget_uplinkdefinedcontours')


    def backwards(self, orm):
        # Adding model 'UplinkDefinedContours'
        db.create_table(u'linkbudget_uplinkdefinedcontours', (
            ('beam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.UplinkBeam'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['UplinkDefinedContours'])


    models = {
        u'linkbudget.uplinkbeam': {
            'Meta': {'object_name': 'UplinkBeam'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'peak_gt': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['linkbudget']