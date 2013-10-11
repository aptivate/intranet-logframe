# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SubIndicator.source'
        db.alter_column(u'logframe_subindicator', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Source'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'SubIndicator.source'
        raise RuntimeError("Cannot reverse this migration. 'SubIndicator.source' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'SubIndicator.source'
        db.alter_column(u'logframe_subindicator', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['logframe.Source']))

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
            'output': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Output']", 'null': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'risk_rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.RiskRating']", 'null': 'True', 'blank': 'True'})
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
        },
        u'logframe.subindicator': {
            'Meta': {'object_name': 'SubIndicator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Indicator']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['logframe.Source']", 'null': 'True'})
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