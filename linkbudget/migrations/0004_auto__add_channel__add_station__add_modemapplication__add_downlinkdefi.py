# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Channel'
        db.create_table(u'linkbudget_channel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('uplink_beam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.UplinkBeam'], null=True)),
            ('downlink_beam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.DownlinkBeam'], null=True)),
            ('transponder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Transponder'], null=True)),
            ('bandwidth', self.gf('django.db.models.fields.FloatField')()),
            ('center_frequency', self.gf('django.db.models.fields.FloatField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'linkbudget', ['Channel'])

        # Adding model 'Station'
        db.create_table(u'linkbudget_station', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('antenna', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Antenna'], null=True)),
            ('hpa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Hpa'], null=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Location'])),
        ))
        db.send_create_signal(u'linkbudget', ['Station'])

        # Adding model 'ModemApplication'
        db.create_table(u'linkbudget_modemapplication', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('modem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Modem'], null=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('minimum_symbol_rate', self.gf('django.db.models.fields.FloatField')()),
            ('maximum_symbol_rate', self.gf('django.db.models.fields.FloatField')()),
            ('rolloff_factor', self.gf('django.db.models.fields.FloatField')()),
            ('rolloff_factor_from_test', self.gf('django.db.models.fields.FloatField')()),
            ('link_margin', self.gf('django.db.models.fields.FloatField')()),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'linkbudget', ['ModemApplication'])

        # Adding model 'DownlinkDefinedContour'
        db.create_table(u'linkbudget_downlinkdefinedcontour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.DownlinkBeam'], null=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['DownlinkDefinedContour'])

        # Adding model 'TransmitBand'
        db.create_table(u'linkbudget_transmitband', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('antenna', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Antenna'], null=True)),
            ('start_frequency', self.gf('django.db.models.fields.FloatField')()),
            ('stop_frequency', self.gf('django.db.models.fields.FloatField')()),
            ('polarization', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'linkbudget', ['TransmitBand'])

        # Adding model 'AntennaVendor'
        db.create_table(u'linkbudget_antennavendor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'linkbudget', ['AntennaVendor'])

        # Adding model 'Transponder'
        db.create_table(u'linkbudget_transponder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('satellite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Satellite'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('hpa_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('hpa_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('linearizer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dynamic_range', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['Transponder'])

        # Adding model 'TransponderCharacteristic'
        db.create_table(u'linkbudget_transpondercharacteristic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transponder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Transponder'], null=True)),
            ('input_backoff', self.gf('django.db.models.fields.FloatField')()),
            ('output_backoff', self.gf('django.db.models.fields.FloatField')()),
            ('c_3im', self.gf('django.db.models.fields.FloatField')()),
            ('npr', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['TransponderCharacteristic'])

        # Adding model 'Gateway'
        db.create_table(u'linkbudget_gateway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('antenna', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Antenna'], null=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Location'], null=True)),
            ('diversity_gateway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Gateway'])),
        ))
        db.send_create_signal(u'linkbudget', ['Gateway'])

        # Adding model 'AntennaGain'
        db.create_table(u'linkbudget_antennagain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('antenna', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Antenna'], null=True)),
            ('frequency', self.gf('django.db.models.fields.FloatField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['AntennaGain'])

        # Adding model 'MCG'
        db.create_table(u'linkbudget_mcg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.ModemApplication'], null=True)),
            ('fec', self.gf('django.db.models.fields.FloatField')()),
            ('modulation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('efficiency', self.gf('django.db.models.fields.FloatField')()),
            ('efficiency_from_test', self.gf('django.db.models.fields.FloatField')()),
            ('cn_threshold', self.gf('django.db.models.fields.FloatField')()),
            ('cn_threshold_from_test', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['MCG'])

        # Adding model 'FrequencyBand'
        db.create_table(u'linkbudget_frequencyband', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start', self.gf('django.db.models.fields.FloatField')()),
            ('stop', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['FrequencyBand'])

        # Adding model 'Modem'
        db.create_table(u'linkbudget_modem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.ModemVendor'], null=True)),
        ))
        db.send_create_signal(u'linkbudget', ['Modem'])

        # Adding model 'AvailableSymbolRate'
        db.create_table(u'linkbudget_availablesymbolrate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.ModemApplication'], null=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['AvailableSymbolRate'])

        # Adding model 'AntennaGT'
        db.create_table(u'linkbudget_antennagt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('antenna', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Antenna'], null=True)),
            ('frequency', self.gf('django.db.models.fields.FloatField')()),
            ('elevation_angle', self.gf('django.db.models.fields.FloatField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['AntennaGT'])

        # Adding model 'ModemVendor'
        db.create_table(u'linkbudget_modemvendor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'linkbudget', ['ModemVendor'])

        # Adding model 'AlcFullLoadBackoff'
        db.create_table(u'linkbudget_alcfullloadbackoff', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transponder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Transponder'], null=True)),
            ('operating_output_backoff', self.gf('django.db.models.fields.FloatField')()),
            ('contract_output_backoff', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['AlcFullLoadBackoff'])

        # Adding model 'Satellite'
        db.create_table(u'linkbudget_satellite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('orbital_slot', self.gf('django.db.models.fields.FloatField')()),
            ('half_station_keeping_box', self.gf('django.db.models.fields.FloatField')()),
            ('launch_date', self.gf('django.db.models.fields.DateField')()),
            ('service_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'linkbudget', ['Satellite'])

        # Adding M2M table for field frequency_bands on 'Satellite'
        m2m_table_name = db.shorten_name(u'linkbudget_satellite_frequency_bands')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('satellite', models.ForeignKey(orm[u'linkbudget.satellite'], null=False)),
            ('frequencyband', models.ForeignKey(orm[u'linkbudget.frequencyband'], null=False))
        ))
        db.create_unique(m2m_table_name, ['satellite_id', 'frequencyband_id'])

        # Adding model 'Location'
        db.create_table(u'linkbudget_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal(u'linkbudget', ['Location'])

        # Adding model 'Hpa'
        db.create_table(u'linkbudget_hpa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('output_power', self.gf('django.db.models.fields.FloatField')()),
            ('output_backoff', self.gf('django.db.models.fields.FloatField')()),
            ('c_im3', self.gf('django.db.models.fields.FloatField')(default=50)),
            ('npr', self.gf('django.db.models.fields.FloatField')(default=50)),
            ('upc', self.gf('django.db.models.fields.FloatField')()),
            ('ifl', self.gf('django.db.models.fields.FloatField')()),
            ('gateway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Gateway'], null=True)),
        ))
        db.send_create_signal(u'linkbudget', ['Hpa'])

        # Adding M2M table for field channels on 'Hpa'
        m2m_table_name = db.shorten_name(u'linkbudget_hpa_channels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hpa', models.ForeignKey(orm[u'linkbudget.hpa'], null=False)),
            ('channel', models.ForeignKey(orm[u'linkbudget.channel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hpa_id', 'channel_id'])

        # Adding model 'ReceiveBand'
        db.create_table(u'linkbudget_receiveband', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('antenna', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Antenna'], null=True)),
            ('start_frequency', self.gf('django.db.models.fields.FloatField')()),
            ('stop_frequency', self.gf('django.db.models.fields.FloatField')()),
            ('polarization', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'linkbudget', ['ReceiveBand'])

        # Adding model 'DownlinkBeam'
        db.create_table(u'linkbudget_downlinkbeam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('satellite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Satellite'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('peak_sat_eirp', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'linkbudget', ['DownlinkBeam'])

        # Adding model 'Antenna'
        db.create_table(u'linkbudget_antenna', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('diameter', self.gf('django.db.models.fields.FloatField')()),
            ('minimum_elevation', self.gf('django.db.models.fields.FloatField')()),
            ('maximum_elevation', self.gf('django.db.models.fields.FloatField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('has_tracking', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'linkbudget', ['Antenna'])

        # Adding field 'UplinkBeam.satellite'
        db.add_column(u'linkbudget_uplinkbeam', 'satellite',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.Satellite'], null=True),
                      keep_default=False)

        # Adding field 'UplinkBeam.polarization'
        db.add_column(u'linkbudget_uplinkbeam', 'polarization',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True),
                      keep_default=False)

        # Adding field 'UplinkBeam.sfd_max_atten'
        db.add_column(u'linkbudget_uplinkbeam', 'sfd_max_atten',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'UplinkBeam.type'
        db.add_column(u'linkbudget_uplinkbeam', 'type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)


        # Changing field 'UplinkDefinedContour.beam'
        db.alter_column(u'linkbudget_uplinkdefinedcontour', 'beam_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['linkbudget.UplinkBeam'], null=True))

    def backwards(self, orm):
        # Deleting model 'Channel'
        db.delete_table(u'linkbudget_channel')

        # Deleting model 'Station'
        db.delete_table(u'linkbudget_station')

        # Deleting model 'ModemApplication'
        db.delete_table(u'linkbudget_modemapplication')

        # Deleting model 'DownlinkDefinedContour'
        db.delete_table(u'linkbudget_downlinkdefinedcontour')

        # Deleting model 'TransmitBand'
        db.delete_table(u'linkbudget_transmitband')

        # Deleting model 'AntennaVendor'
        db.delete_table(u'linkbudget_antennavendor')

        # Deleting model 'Transponder'
        db.delete_table(u'linkbudget_transponder')

        # Deleting model 'TransponderCharacteristic'
        db.delete_table(u'linkbudget_transpondercharacteristic')

        # Deleting model 'Gateway'
        db.delete_table(u'linkbudget_gateway')

        # Deleting model 'AntennaGain'
        db.delete_table(u'linkbudget_antennagain')

        # Deleting model 'MCG'
        db.delete_table(u'linkbudget_mcg')

        # Deleting model 'FrequencyBand'
        db.delete_table(u'linkbudget_frequencyband')

        # Deleting model 'Modem'
        db.delete_table(u'linkbudget_modem')

        # Deleting model 'AvailableSymbolRate'
        db.delete_table(u'linkbudget_availablesymbolrate')

        # Deleting model 'AntennaGT'
        db.delete_table(u'linkbudget_antennagt')

        # Deleting model 'ModemVendor'
        db.delete_table(u'linkbudget_modemvendor')

        # Deleting model 'AlcFullLoadBackoff'
        db.delete_table(u'linkbudget_alcfullloadbackoff')

        # Deleting model 'Satellite'
        db.delete_table(u'linkbudget_satellite')

        # Removing M2M table for field frequency_bands on 'Satellite'
        db.delete_table(db.shorten_name(u'linkbudget_satellite_frequency_bands'))

        # Deleting model 'Location'
        db.delete_table(u'linkbudget_location')

        # Deleting model 'Hpa'
        db.delete_table(u'linkbudget_hpa')

        # Removing M2M table for field channels on 'Hpa'
        db.delete_table(db.shorten_name(u'linkbudget_hpa_channels'))

        # Deleting model 'ReceiveBand'
        db.delete_table(u'linkbudget_receiveband')

        # Deleting model 'DownlinkBeam'
        db.delete_table(u'linkbudget_downlinkbeam')

        # Deleting model 'Antenna'
        db.delete_table(u'linkbudget_antenna')

        # Deleting field 'UplinkBeam.satellite'
        db.delete_column(u'linkbudget_uplinkbeam', 'satellite_id')

        # Deleting field 'UplinkBeam.polarization'
        db.delete_column(u'linkbudget_uplinkbeam', 'polarization')

        # Deleting field 'UplinkBeam.sfd_max_atten'
        db.delete_column(u'linkbudget_uplinkbeam', 'sfd_max_atten')

        # Deleting field 'UplinkBeam.type'
        db.delete_column(u'linkbudget_uplinkbeam', 'type')


        # Changing field 'UplinkDefinedContour.beam'
        db.alter_column(u'linkbudget_uplinkdefinedcontour', 'beam_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['linkbudget.UplinkBeam']))

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
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'center_frequency': ('django.db.models.fields.FloatField', [], {}),
            'downlink_beam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.DownlinkBeam']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transponder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Transponder']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uplink_beam': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.UplinkBeam']", 'null': 'True'})
        },
        u'linkbudget.downlinkbeam': {
            'Meta': {'object_name': 'DownlinkBeam'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
            'Meta': {'object_name': 'FrequencyBand'},
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
            'satellite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Satellite']", 'null': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'peak_gt': ('django.db.models.fields.FloatField', [], {}),
            'polarization': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'satellite': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['linkbudget.Satellite']", 'null': 'True'}),
            'sfd_max_atten': ('django.db.models.fields.FloatField', [], {'default': '0'}),
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