# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Output.budget_planned'
        db.add_column(u'logframe_output', 'budget_planned',
                      self.gf('django.db.models.fields.IntegerField')(default=500000),
                      keep_default=False)

        # Adding field 'Output.budget_spent'
        db.add_column(u'logframe_output', 'budget_spent',
                      self.gf('django.db.models.fields.IntegerField')(default=265500),
                      keep_default=False)

        # Adding field 'Output.activities_planned'
        db.add_column(u'logframe_output', 'activities_planned',
                      self.gf('django.db.models.fields.IntegerField')(default=25),
                      keep_default=False)

        # Adding field 'Output.activities_complete'
        db.add_column(u'logframe_output', 'activities_complete',
                      self.gf('django.db.models.fields.IntegerField')(default=4),
                      keep_default=False)

        # Adding field 'Output.activities_on_schedule'
        db.add_column(u'logframe_output', 'activities_on_schedule',
                      self.gf('django.db.models.fields.IntegerField')(default=9),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Output.budget_planned'
        db.delete_column(u'logframe_output', 'budget_planned')

        # Deleting field 'Output.budget_spent'
        db.delete_column(u'logframe_output', 'budget_spent')

        # Deleting field 'Output.activities_planned'
        db.delete_column(u'logframe_output', 'activities_planned')

        # Deleting field 'Output.activities_complete'
        db.delete_column(u'logframe_output', 'activities_complete')

        # Deleting field 'Output.activities_on_schedule'
        db.delete_column(u'logframe_output', 'activities_on_schedule')


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
            'activities_complete': ('django.db.models.fields.IntegerField', [], {}),
            'activities_on_schedule': ('django.db.models.fields.IntegerField', [], {}),
            'activities_planned': ('django.db.models.fields.IntegerField', [], {}),
            'assumptions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'budget_planned': ('django.db.models.fields.IntegerField', [], {}),
            'budget_spent': ('django.db.models.fields.IntegerField', [], {}),
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