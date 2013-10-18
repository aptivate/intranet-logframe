from __future__ import absolute_import, unicode_literals

from collections import namedtuple
from django_dynamic_fixture import N
from unittest import TestCase

from ..models import Output, AverageTargetPercentMixin


class TestOutput(TestCase):

    def test_budget_percentage(self):
        output = N(Output, budget_planned=200, budget_spent=50)
        self.assertEqual(25, output.budget_percent())

    def test_activity_percentage_uses_on_schedule_not_complete(self):
        output = N(Output, activities_planned=25,
                   activities_complete=4, activities_on_schedule=9)
        self.assertEqual(36, output.activities_percent())


class TestAverageTargetPercentMixin(TestCase):

    FakeChild = namedtuple('FakeChild', ['target_percent'])
    FakeWeightedChild = namedtuple('FakeWeightedChild', ['target_percent', 'impact_weighting'])

    def setUp(self):
        self.testobj = AverageTargetPercentMixin()

    def test_calculate_target_percent_returns_0_when_no_children(self):
        self.assertEqual(0, self.testobj._calculate_target_percent([]))

    def test_calculate_target_percent_returns_child_percent_when_one_child_present(self):
        child1 = self.FakeChild(43)
        self.assertEqual(43, self.testobj._calculate_target_percent([child1]))

    def test_calculate_target_percent_averages_two_children(self):
        child1 = self.FakeChild(45)
        child2 = self.FakeChild(55)
        self.assertEqual(50, self.testobj._calculate_target_percent([child1, child2]))

    def test_calculate_weighted_target_percent_returns_0_when_no_children(self):
        self.assertEqual(0, self.testobj._calculate_weighted_target_percent([]))

    def test_calculate_weighted_target_percent_returns_child_percent_when_one_child_present(self):
        child1 = self.FakeWeightedChild(43, 20)
        self.assertEqual(43, self.testobj._calculate_weighted_target_percent([child1]))

    def test_calculate_weighted_target_percent_averages_two_children(self):
        child1 = self.FakeWeightedChild(45, 20)
        child2 = self.FakeWeightedChild(60, 10)
        self.assertEqual(50, self.testobj._calculate_weighted_target_percent([child1, child2]))
