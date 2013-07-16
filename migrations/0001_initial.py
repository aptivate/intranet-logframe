# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RiskRating'
        db.create_table(u'logframe_riskrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'logframe', ['RiskRating'])

        # Adding model 'Output'
        db.create_table(u'logframe_output', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('impact_weighting', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('assumptions', self.gf('django.db.models.fields.TextField')()),
            ('risk_rating', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.RiskRating'])),
        ))
        db.send_create_signal(u'logframe', ['Output'])

        # Adding model 'Source'
        db.create_table(u'logframe_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'logframe', ['Source'])

        # Adding model 'Indicator'
        db.create_table(u'logframe_indicator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Source'])),
            ('output', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Output'], null=True)),
        ))
        db.send_create_signal(u'logframe', ['Indicator'])

        # Adding model 'Donor'
        db.create_table(u'logframe_donor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'logframe', ['Donor'])

        # Adding model 'InputType'
        db.create_table(u'logframe_inputtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'logframe', ['InputType'])

        # Adding model 'Input'
        db.create_table(u'logframe_input', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('output', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Output'])),
            ('input_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.InputType'])),
            ('quantity', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'logframe', ['Input'])

        # Adding model 'InputShare'
        db.create_table(u'logframe_inputshare', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('input_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.InputType'])),
            ('total', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'logframe', ['InputShare'])


    def backwards(self, orm):
        
        # Deleting model 'RiskRating'
        db.delete_table(u'logframe_riskrating')

        # Deleting model 'Output'
        db.delete_table(u'logframe_output')

        # Deleting model 'Source'
        db.delete_table(u'logframe_source')

        # Deleting model 'Indicator'
        db.delete_table(u'logframe_indicator')

        # Deleting model 'Donor'
        db.delete_table(u'logframe_donor')

        # Deleting model 'InputType'
        db.delete_table(u'logframe_inputtype')

        # Deleting model 'Input'
        db.delete_table(u'logframe_input')

        # Deleting model 'InputShare'
        db.delete_table(u'logframe_inputshare')


    models = {
        u'logframe.donor': {
            'Meta': {'object_name': 'Donor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'logframe.indicator': {
            'Meta': {'object_name': 'Indicator'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'output': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Output']", 'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Source']"})
        },
        u'logframe.input': {
            'Meta': {'object_name': 'Input'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.InputType']"}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {}),
            'output': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Output']"}),
            'quantity': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'logframe.inputshare': {
            'Meta': {'object_name': 'InputShare'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.InputType']"}),
            'total': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'logframe.inputtype': {
            'Meta': {'object_name': 'InputType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'logframe.output': {
            'Meta': {'object_name': 'Output'},
            'assumptions': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impact_weighting': ('django.db.models.fields.SmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'risk_rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.RiskRating']"})
        },
        u'logframe.riskrating': {
            'Meta': {'object_name': 'RiskRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'logframe.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['logframe']
