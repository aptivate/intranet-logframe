from __future__ import absolute_import, unicode_literals

from unittest import TestCase
from django_dynamic_fixture import N

from ..models import Output


class TestOutput(TestCase):

    def test_budget_percentage(self):
        output = N(Output, budget_planned=200, budget_spent=50)
        self.assertEqual(25, output.budget_percent())

    def test_activity_percentage_uses_on_schedule_not_complete(self):
        output = N(Output, activities_planned=25,
                   activities_complete=4, activities_on_schedule=9)
        self.assertEqual(36, output.activities_percent())
