import binder.models
import django.dispatch

from django.db import models

# http://djangosnippets.org/snippets/1054/

class RiskRating(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class Output(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    order = models.IntegerField()
    # fk to stream
    impact_weighting = models.SmallIntegerField()
    # fk to outcome
    assumptions = models.TextField()
    risk_rating = models.ForeignKey(RiskRating)

    def __unicode__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class Indicator(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    source = models.ForeignKey(Source)
    output = models.ForeignKey(Output, null=True)

    def __unicode__(self):
        return self.name

class Donor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class InputType(models.Model):
    """Financial or human resources? (which row of inputs)"""

    name = models.CharField(max_length=255)
    units = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Input(models.Model):
    """Value of inputs on a particular Output and type"""

    output = models.ForeignKey(Output)
    input_type = models.ForeignKey(InputType)
    quantity = models.CharField(max_length=255)
    order = models.SmallIntegerField()

    def __unicode__(self):
        return "%s, %s, %s" % (output, input_type, quantity)

class InputShare(models.Model):
    input_type = models.ForeignKey(InputType)
    total = models.CharField(max_length=255)

