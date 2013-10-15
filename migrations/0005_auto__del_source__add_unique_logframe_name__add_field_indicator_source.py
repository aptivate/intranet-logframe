# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Output', fields ['name']
        db.delete_unique(u'logframe_output', ['name'])

        # Deleting model 'Source'
        db.delete_table(u'logframe_source')

        # Adding unique constraint on 'LogFrame', fields ['name']
        db.create_unique(u'logframe_logframe', ['name'])

        # Adding field 'Indicator.source'
        db.add_column(u'logframe_indicator', 'source',
                      self.gf('django.db.models.fields.TextField')(default='no source yet'),
                      keep_default=False)

        # Deleting field 'SubIndicator.source'
        db.delete_column(u'logframe_subindicator', 'source_id')


    def backwards(self, orm):
        # Removing unique constraint on 'LogFrame', fields ['name']
        db.delete_unique(u'logframe_logframe', ['name'])

        # Adding model 'Source'
        db.create_table(u'logframe_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal(u'logframe', ['Source'])

        # Deleting field 'Indicator.source'
        db.delete_column(u'logframe_indicator', 'source')

        # Adding unique constraint on 'Output', fields ['name']
        db.create_unique(u'logframe_output', ['name'])

        # Adding field 'SubIndicator.source'
        db.add_column(u'logframe_subindicator', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Source'], null=True),
                      keep_default=False)


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'output': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Output']", 'null': 'True'}),
            'source': ('django.db.models.fields.TextField', [], {})
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
        u'logframe.logframe': {
            'Meta': {'object_name': 'LogFrame'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'logframe.milestone': {
            'Meta': {'object_name': 'Milestone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.LogFrame']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'logframe.output': {
            'Meta': {'object_name': 'Output'},
            'assumptions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impact_weighting': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'log_frame': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.LogFrame']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'risk_rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.RiskRating']", 'null': 'True', 'blank': 'True'})
        },
        u'logframe.riskrating': {
            'Meta': {'ordering': "[u'id']", 'object_name': 'RiskRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'logframe.subindicator': {
            'Meta': {'object_name': 'SubIndicator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Indicator']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'logframe.target': {
            'Meta': {'object_name': 'Target'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Milestone']"}),
            'sub_indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.SubIndicator']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['logframe']