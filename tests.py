from __future__ import absolute_import

from django.contrib.auth import get_user_model
#from django.conf import settings
from django.core.urlresolvers import reverse
#from django.template import Context
UserModel = get_user_model()

from django_dynamic_fixture import G

from binder.test_utils import AptivateEnhancedTestCase
from .models import LogFrame, Milestone, Output, Indicator


class LogframeTest(AptivateEnhancedTestCase):

    def assert_get_management_form(self):
        total = self.get_page_element('.//' + self.xhtml('input') + '[@id="id_indicator_set-TOTAL_FORMS"]')
        initial = self.get_page_element('.//' + self.xhtml('input') + '[@id="id_indicator_set-INITIAL_FORMS"]')
        max_num = self.get_page_element('.//' + self.xhtml('input') + '[@id="id_indicator_set-MAX_NUM_FORMS"]')
        return {
            element.get('name'): element.get('value')
            for element in [total, initial, max_num]
        }

    def test_create_view_context_contains_the_correct_formsets(self):
        log_frame = G(LogFrame)

        # While the OutputCreate view attaches the new Output to the first
        # LogFrame it can find, we must have just one in the database for
        # tests to pass.
        self.assertEquals([log_frame], list(LogFrame.objects.all()),
            "There should be no other LogFrame objects in the database "
            "at the beginning of the test, otherwise it may fail!")

        milestones = [
            G(Milestone, log_frame=log_frame, name="Baseline 2013"),
            G(Milestone, log_frame=log_frame, name="Milestone 1 2014"),
            G(Milestone, log_frame=log_frame, name="Target 2017"),
        ]

        url = reverse('logframe-output-create')
        response = self.client.get(url)
        form = response.context['form']

        from .forms import OutputForm
        self.assertIsInstance(form, OutputForm)

        indicators = response.context['indicators']
        from .forms import IndicatorFormSet
        self.assertIsInstance(indicators, IndicatorFormSet)

        # there should be a management form in the page for the indicator formset
        self.assert_get_management_form()

        self.assertEquals(1, len(indicators),
            "There should be one empty form to use as a template")
        self.assertTrue(indicators[0].empty_permitted,
            "The first form should be allowed to be empty")
        self.assertTrue(indicators[0].empty,
            "The second form should be marked as the special empty form")
        empty_form_row = self.get_page_element('.//' + self.xhtml('tr') +
            '[@id="id_indicator_set-__prefix__"]')
        self.assertEquals("display: none;", empty_form_row.get('style'),
            "The empty form should be hidden (not displayed)")

        indicator = indicators[0]
        from django.forms.models import ModelForm
        self.assertIsInstance(indicator, ModelForm)
        self.assertIsInstance(indicator.instance, Indicator)

        # there should be a hidden ID field for this indicator form
        self.get_page_element('.//' + self.xhtml('input') + '[@id="id_indicator_set-__prefix__-id"]')

        subindicators = indicator.subindicators
        # from .forms import SubIndicatorFormSet
        # self.assertIsInstance(subindicators, SubIndicatorFormSet)

        subindicator = subindicators[0]
        self.assertIsInstance(subindicator, ModelForm)
        from .models import SubIndicator
        self.assertIsInstance(subindicator.instance, SubIndicator)

        self.assertEquals(milestones, list(response.context['milestones']),
            "The view needs to put the list of milestones into the context "
            "for the form to render the right columns")

        from .models import Target
        targets = subindicator.instance.targets
        self.assertEquals([Target() for m in milestones], targets,
            "Every SubIndicator should have a target for every milestone")
        for i, t in enumerate(targets):
            self.assertEquals(subindicator.instance, t.sub_indicator)
            m = milestones[i]
            self.assertEquals(m, t.milestone)
        self.assertEquals(targets, subindicator.instance.targets_fake_queryset,
            "The fresh Target objects should have been added to the Fake QuerySet")
        self.assertEquals(targets, [form.instance for form in subindicator.targets],
            "The fake queryset should have generated instances in the InlineFormSet")

        from .forms import TargetFormSet
        self.assertIsInstance(subindicator.targets, TargetFormSet)
        self.assertEquals("subindicator_%s_targets" % subindicator.instance.pk,
            subindicator.targets.prefix, "Each subindicator targets formset "
            "must use a unique prefix to avoid them colliding in the page")

    def assert_submit_output_form(self, output_to_update_if_any=None,
            override_form_values={}):

        default_form_values = {
            'name': 'Print',
            'description': 'hello world',
            'log_frame': LogFrame.objects.first().pk,
        }

        form_values = dict()
        form_values.update(default_form_values)

        # we have to do a GET to find the management form values
        if output_to_update_if_any:
            url = reverse('logframe-output-update',
                kwargs={'pk': output_to_update_if_any.pk})
        else:
            url = reverse('logframe-output-create')

        response = self.client.get(url)
        form_values.update(self.assert_get_management_form())

        # Copy all the formset form values from initial to the request dict,
        # to ensure that the forms think they haven't been touched (all
        # values still set to initial) and therefore don't try to validate
        # themselves, which would fail because we haven't provided values.
        for indicator_form in response.context['indicators']:
            for name, field in indicator_form.fields.items():
                prefixed_name = indicator_form.add_prefix(name)
                if name in indicator_form.initial:
                    form_values[prefixed_name] = indicator_form.initial[name]

            prefix = 'indicator_%s_subindicators-' % indicator_form.instance.id
            form_values.update({
                prefix + 'TOTAL_FORMS': '0',
                prefix + 'INITIAL_FORMS': '0',
            })

        form_values.update(override_form_values)

        response = self.client.post(url, form_values)
        if response.status_code != 302:
            # try to diagnose the error better
            output_form = response.context.get('form', None)
            if output_form is not None:
                self.assertEquals({}, output_form.errors,
                    "Expected the object to be saved and to be redirected "
                    "to its edit page, but the form didn't validate, so "
                    "that didn't happen")

            indicator_formset = response.context.get('indicators', None)
            if indicator_formset is not None:
                self.assertEquals({}, indicator_formset.errors,
                    "Expected the object to be saved and to be redirected "
                    "to its edit page, but the form didn't validate, so "
                    "that didn't happen")

        self.assertEquals(302, response.status_code, "Expected the object "
            "to be saved and to be redirected to its edit page, but this "
            "happened instead: %s" %
            (None if response.status_code is 302 else response.content))

        if output_to_update_if_any:
            output = output_to_update_if_any
            edit_url = url
        else:
            output = Output.objects.last()
            edit_url = reverse('logframe-output-update',
                kwargs={'pk': output.pk})

        self.assertRedirectedWithoutFollowing(response, edit_url)

        response = self.client.get(edit_url)
        self.assertInDict('form', response.context,
            "Where are we? should be rendering the same page again, "
            "but got this instead: %s" % response.content)

        return response, form_values, output

    def test_submit_output_form_creates_output(self):
        G(LogFrame)
        response, form_values, output = self.assert_submit_output_form()

        self.assertEquals(form_values['name'], output.name,
            "The POST values should have been saved in the database")
        self.assertEquals(form_values['description'], output.description,
            "The POST values should have been saved in the database")
        self.assertEquals(form_values['log_frame'], output.log_frame.pk,
            "The POST values should have been saved in the database")
        self.assertEquals(1, output.order, "The first Output for a given "
            "LogFrame should have order set to 1")

    def test_second_output_has_higher_order(self):
        output = G(Output, order=1)

        response, form_values, output2 = self.assert_submit_output_form()
        self.assertNotEquals(output, output2,
            "POST should have created a new Output with a different PK")
        self.assertEquals(2, output2.order, "The second Output for a given "
            "LogFrame should have order set to 2")

    def test_create_output_with_indicator_already_populated(self):
        G(LogFrame)

        from django.forms import formsets
        override_form_values = {
            'indicator_set-0-name': 'Left Indicator',
            'indicator_set-0-description': 'Used when going left',
            'indicator_set-0-' + formsets.DELETION_FIELD_NAME: '',
            'indicator_set-TOTAL_FORMS': 1,
        }

        response, form_values, output = self.assert_submit_output_form(
            override_form_values=override_form_values)
        self.assertEquals(1, output.indicator_set.count(),
            "An indicator should have been created to go with the new "
            "Output object.")

        from .models import Indicator
        indicator = Indicator.objects.first()
        self.assertEquals(override_form_values['indicator_set-0-name'],
            indicator.name)
        self.assertEquals(override_form_values['indicator_set-0-description'],
            indicator.description)

    def test_create_output_with_indicator_added_using_javascript(self):
        G(LogFrame)

        from django.forms import formsets
        override_form_values = {
            'indicator_set-0-name': 'Left Indicator',
            'indicator_set-0-description': 'Used when going left',
            'indicator_set-0-' + formsets.DELETION_FIELD_NAME: '',
            'indicator_set-1-name': 'Speedometer',
            'indicator_set-1-description': "Used to check that you won't "
                "get a speeding fine",
            'indicator_set-1-' + formsets.DELETION_FIELD_NAME: '',
            'indicator_set-TOTAL_FORMS': 2,
        }

        response, form_values, output = self.assert_submit_output_form(
            override_form_values=override_form_values)
        self.assertEquals(2, output.indicator_set.count(),
            "Two indicators should have been created to go with the new "
            "Output object.")

        from .models import Indicator
        indicator = Indicator.objects.all()[0]
        self.assertEquals(override_form_values['indicator_set-0-name'],
            indicator.name)
        self.assertEquals(override_form_values['indicator_set-0-description'],
            indicator.description)

        indicator = Indicator.objects.all()[1]
        self.assertEquals(override_form_values['indicator_set-1-name'],
            indicator.name)
        self.assertEquals(override_form_values['indicator_set-1-description'],
            indicator.description)

    def test_output_impact_weighting_saved(self):
        G(LogFrame)

        override_form_values = {
            'impact_weighting': '1'
        }
        response, form_values, output = self.assert_submit_output_form(
            override_form_values=override_form_values)
        self.assertEqual(1, output.impact_weighting)

    def test_add_subindicator_to_existing_indicator(self):
        indicator = G(Indicator)
        prefix = 'indicator_%d_subindicators-' % indicator.id
        noneprefix = 'indicator_None_subindicators-'

        override_form_values = {
            'indicator_set-0-id': indicator.id,
            'indicator_set-0-name': indicator.name,
            'indicator_set-0-description': indicator.description,
            'indicator_set-TOTAL_FORMS': 1,
            prefix + 'TOTAL_FORMS': '1',
            prefix + 'INITIAL_FORMS': '0',
            prefix + 'MAX_NUM_FORMS': '1000',
            prefix + '0-name': 'new sub',
            noneprefix + 'TOTAL_FORMS': '0',
            noneprefix + 'INITIAL_FORMS': '0',
        }
        response, form_values, output = self.assert_submit_output_form(
            output_to_update_if_any=indicator.output,
            override_form_values=override_form_values)
        self.assertEqual(1, indicator.subindicator_set.count())
        self.assertEqual('new sub', indicator.subindicator_set.first().name)
