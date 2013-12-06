# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Antenna.vendor' to match new field type.
        db.rename_column(u'linkbudget_antenna', 'vendor', 'vendor_id')
        # Changing field 'Antenna.vendor'
        # db.alter_column(u'linkbudget_antenna', 'vendor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.AntennaVendor'], null=True))
        # Adding index on 'Antenna', fields ['vendor']
        db.create_index(u'linkbudget_antenna', ['vendor_id'])


    def backwards(self, orm):
        # Removing index on 'Antenna', fields ['vendor']
        db.delete_index(u'linkbudget_antenna', ['vendor_id'])


        # User chose to not deal with backwards NULL issues for 'Antenna.vendor'
        raise RuntimeError("Cannot reverse this migration. 'Antenna.vendor' and its values cannot be restored.")

    models = {
        u'linkbudget.alcfullloadbackoff': {
            'Meta': {'object_name': 'AlcFullLoadBackoff'},
            'contract_output_backoff': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operating_output_backoff': ('django.db.models.fields.FloatField', [], {}),
            'transponder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Transponder']", 'null': 'True'})
        },
        u'linkbudget.antenna': {
            'Meta': {'object_name': 'Antenna'},
            'diameter': ('django.db.models.fields.FloatField', [], {}),
            'has_tracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_elevation': ('django.db.models.fields.FloatField', [], {}),
            'minimum_elevation': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.AntennaVendor']", 'null': 'True'})
        },
        u'linkbudget.antennagain': {
            'Meta': {'object_name': 'AntennaGain'},
            'antenna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Antenna']", 'null': 'True'}),
            'frequency': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.antennagt': {
            'Meta': {'object_name': 'AntennaGT'},
            'antenna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Antenna']", 'null': 'True'}),
            'elevation_angle': ('django.db.models.fields.FloatField', [], {}),
            'frequency': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.antennavendor': {
            'Meta': {'object_name': 'AntennaVendor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'linkbudget.availablesymbolrate': {
            'Meta': {'object_name': 'AvailableSymbolRate'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.ModemApplication']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.channel': {
            'Meta': {'object_name': 'Channel'},
            'bandwidth': ('django.db.models.fields.FloatField', [], {}),
            'downlink_beam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.DownlinkBeam']", 'null': 'True'}),
            'downlink_center_frequency': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'sfd_max_atten_alc': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sfd_max_atten_fgm': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'transponder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Transponder']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uplink_beam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.UplinkBeam']", 'null': 'True'}),
            'uplink_center_frequency': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.downlinkbeam': {
            'Meta': {'object_name': 'DownlinkBeam'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'peak_sat_eirp': ('django.db.models.fields.FloatField', [], {}),
            'satellite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Satellite']", 'null': 'True'})
        },
        u'linkbudget.downlinkdefinedcontour': {
            'Meta': {'object_name': 'DownlinkDefinedContour'},
            'beam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.DownlinkBeam']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.frequencyband': {
            'Meta': {'ordering': "['start']", 'object_name': 'FrequencyBand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start': ('django.db.models.fields.FloatField', [], {}),
            'stop': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.gateway': {
            'Meta': {'object_name': 'Gateway'},
            'antenna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Antenna']", 'null': 'True'}),
            'diversity_gateway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Gateway']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Location']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'linkbudget.hpa': {
            'Meta': {'object_name': 'Hpa'},
            'c_im3': ('django.db.models.fields.FloatField', [], {'default': '50'}),
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['linkbudget.Channel']", 'symmetrical': 'False'}),
            'gateway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Gateway']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifl': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'npr': ('django.db.models.fields.FloatField', [], {'default': '50'}),
            'output_backoff': ('django.db.models.fields.FloatField', [], {}),
            'output_power': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'upc': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'})
        },
        u'linkbudget.mcg': {
            'Meta': {'object_name': 'MCG'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.ModemApplication']", 'null': 'True'}),
            'cn_threshold': ('django.db.models.fields.FloatField', [], {}),
            'cn_threshold_from_test': ('django.db.models.fields.FloatField', [], {}),
            'efficiency': ('django.db.models.fields.FloatField', [], {}),
            'efficiency_from_test': ('django.db.models.fields.FloatField', [], {}),
            'fec': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'linkbudget.modem': {
            'Meta': {'object_name': 'Modem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.ModemVendor']", 'null': 'True'})
        },
        u'linkbudget.modemapplication': {
            'Meta': {'object_name': 'ModemApplication'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_margin': ('django.db.models.fields.FloatField', [], {}),
            'maximum_symbol_rate': ('django.db.models.fields.FloatField', [], {}),
            'minimum_symbol_rate': ('django.db.models.fields.FloatField', [], {}),
            'modem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Modem']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'rolloff_factor': ('django.db.models.fields.FloatField', [], {}),
            'rolloff_factor_from_test': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.modemvendor': {
            'Meta': {'object_name': 'ModemVendor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'linkbudget.receiveband': {
            'Meta': {'object_name': 'ReceiveBand'},
            'antenna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Antenna']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polarization': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_frequency': ('django.db.models.fields.FloatField', [], {}),
            'stop_frequency': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.satellite': {
            'Meta': {'object_name': 'Satellite'},
            'frequency_bands': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['linkbudget.FrequencyBand']", 'symmetrical': 'False'}),
            'half_station_keeping_box': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launch_date': ('django.db.models.fields.DateField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'orbital_slot': ('django.db.models.fields.FloatField', [], {}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'linkbudget.station': {
            'Meta': {'object_name': 'Station'},
            'antenna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Antenna']", 'null': 'True'}),
            'hpa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Hpa']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'linkbudget.transmitband': {
            'Meta': {'object_name': 'TransmitBand'},
            'antenna': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Antenna']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polarization': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_frequency': ('django.db.models.fields.FloatField', [], {}),
            'stop_frequency': ('django.db.models.fields.FloatField', [], {})
        },
        u'linkbudget.transponder': {
            'Meta': {'object_name': 'Transponder'},
            'dynamic_range': ('django.db.models.fields.FloatField', [], {}),
            'hpa_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'hpa_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linearizer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'primary_mode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'satellite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Satellite']", 'null': 'True'}),
            'secondary_mode': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '10'})
        },
        u'linkbudget.transpondercharacteristic': {
            'Meta': {'object_name': 'TransponderCharacteristic'},
            'c_3im': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_backoff': ('django.db.models.fields.FloatField', [], {}),
            'npr': ('django.db.models.fields.FloatField', [], {}),
            'output_backoff': ('django.db.models.fields.FloatField', [], {}),
            'transponder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Transponder']", 'null': 'True'})
        },
        u'linkbudget.uplinkbeam': {
            'Meta': {'object_name': 'UplinkBeam'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'peak_gt': ('django.db.models.fields.FloatField', [], {}),
            'polarization': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'satellite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Satellite']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'linkbudget.uplinkdefinedcontour': {
            'Meta': {'object_name': 'UplinkDefinedContour'},
            'beam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.UplinkBeam']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['linkbudget']