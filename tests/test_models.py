from __future__ import absolute_import, unicode_literals

from collections import namedtuple
from django_dynamic_fixture import N
from unittest import TestCase

from ..models import Output, Indicator


class TestOutput(TestCase):

    def test_budget_percentage(self):
        output = N(Output, budget_planned=200, budget_spent=50)
        self.assertEqual(25, output.budget_percent())

    def test_activity_percentage_uses_on_schedule_not_complete(self):
        output = N(Output, activities_planned=25,
                   activities_complete=4, activities_on_schedule=9)
        self.assertEqual(36, output.activities_percent())


class TestIndicator(TestCase):

    FakeSubIndicator = namedtuple('FakeSubIndicator', ['target_percent'])

    def test_calculate_target_percent_returns_0_when_no_subindicators(self):
        indicator = N(Indicator)
        self.assertEqual(0, indicator._calculate_target_percent([]))

    def test_calculate_target_percent_returns_subind_percent(self):
        indicator = N(Indicator)
        sub1 = self.FakeSubIndicator(43)
        self.assertEqual(43, indicator._calculate_target_percent([sub1]))

    def test_calculate_target_percent_averages_two_subindicators(self):
        indicator = N(Indicator)
        sub1 = self.FakeSubIndicator(45)
        sub2 = self.FakeSubIndicator(55)
        self.assertEqual(50, indicator._calculate_target_percent([sub1, sub2]))
