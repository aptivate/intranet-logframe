from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property

# http://djangosnippets.org/snippets/1054/


class LogFrame(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @cached_property
    def milestones(self):
        return self.milestone_set.all()

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class Milestone(models.Model):
    name = models.CharField(max_length=255)
    log_frame = models.ForeignKey(LogFrame)

    class Meta:
        ordering = ['id']

    def save(self):
        ret = super(Milestone, self).save()
        # TODO use a modified version of cached_property that is reversible
        # self.log_frame.invalidate_cache()
        return ret

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class RiskRating(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['id']

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class Result(models.Model):
    """ abstract class to be used by Impact(/Goal), Outcome and Output """
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Output(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.IntegerField()
    # fk to stream
    impact_weighting = models.SmallIntegerField(blank=True, null=True)
    # fk to outcome
    assumptions = models.TextField(blank=True)
    risk_rating = models.ForeignKey(RiskRating, null=True, blank=True)
    log_frame = models.ForeignKey(LogFrame)

    # these are here for now - they might move at some point
    budget_planned = models.IntegerField()
    budget_spent = models.IntegerField()
    activities_planned = models.IntegerField()
    activities_complete = models.IntegerField()
    activities_on_schedule = models.IntegerField()

    def budget_percent(self):
        return int(100 * self.budget_spent / float(self.budget_planned))

    def activities_percent(self):
        return int(100 * self.activities_on_schedule / float(self.activities_planned))

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class Indicator(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    source = models.TextField()
    output = models.ForeignKey(Output, null=True)

    def _calculate_target_percent(self, subindicators):
        percent_list = [s.target_percent for s in subindicators]
        if len(percent_list) == 0:
            return 0
        return sum(percent_list) / len(percent_list)

    def target_percent(self):
        """ average of subindicators """
        return self._calculate_target_percent(self.subindicator_set.all())

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class SubIndicator(models.Model):
    name = models.CharField(max_length=255, blank=True)
    indicator = models.ForeignKey(Indicator)

    # this is just being put here for now - it should really be multiple
    # entries in another class
    current_result = models.IntegerField(default=0)

    @property
    def milestones(self):
        return self.indicator.output.log_frame.milestones

    @property
    def targets(self):
        """ return a list of targets for this subindicator.  First get all
        the already existing targets for this SI.  Then go through each
        milestone, and if there isn't an existing target that matches, create
        one. """
        targets_by_milestone = dict([
            (target.milestone.id, target)
            for target in self.target_set.all()
        ])
        targets_out = [
            # use default value of 1 to avoid divide by zero
            targets_by_milestone.get(milestone.id,
                Target(milestone=milestone, sub_indicator=self, value=1))
            for milestone in self.milestones
        ]
        return targets_out

    @property
    def last_target(self):
        last_milestone = self.milestones.last()
        target_for_last_milestone = self.target_set.filter(milestone=last_milestone)
        if target_for_last_milestone.count() == 0:
            # use default value of 1 to avoid divide by zero
            return Target(milestone=last_milestone, sub_indicator=self, value=1)
        else:
            return target_for_last_milestone.first()

    def target_percent(self):
        return int(100 * self.current_result / float(self.last_target.value))

    @python_2_unicode_compatible
    def __str__(self):
        return self.name

    @property
    def targets_fake_queryset(self):
        return SubIndicator.FakeTargetQuerySet(self)

    class FakeTargetQuerySet(list):

        def __init__(self, subindicator):
            values = subindicator.targets
            super(SubIndicator.FakeTargetQuerySet, self).__init__(values)
            self.subindicator = subindicator
            self.db = self.subindicator.target_set.all().db
            self.ordered = True

        def none(self):
            """Normally we would return an empty QuerySet here, but
            BaseInlineFormSet calls none() whenever the parent object's
            pk is unset, which it will be for us whenever we're creating
            a new SubIndicator. In that case we still want to list all our
            empty Targets.

            We could use BaseInlineQuerySet's extra (blank) forms to
            instantiate missing Targets instead, but if there's a mixture of
            existing and nonexistent Targets in a SubIndicator, how would we
            BaseInlineFormSet to render them in the right order? It's better
            to completely control the list of instances, which is what this
            FakeTargetQuerySet does."""
            return self

        def filter(self, **kwargs):
            """ We are already filtered, so just return ourself. """
            return self


class Target(models.Model):
    sub_indicator = models.ForeignKey(SubIndicator)
    milestone = models.ForeignKey(Milestone)
    value = models.IntegerField()


class Donor(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class InputType(models.Model):
    """Financial or human resources? (which row of inputs)"""

    name = models.CharField(max_length=255)
    units = models.CharField(max_length=255)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class Input(models.Model):
    """Value of inputs on a particular Output and type"""

    output = models.ForeignKey(Output)
    input_type = models.ForeignKey(InputType)
    quantity = models.CharField(max_length=255)
    order = models.SmallIntegerField()

    @python_2_unicode_compatible
    def __str__(self):
        return "%s, %s, %s" % (self.output, self.input_type, self.quantity)


class InputShare(models.Model):
    input_type = models.ForeignKey(InputType)
    total = models.CharField(max_length=255)
