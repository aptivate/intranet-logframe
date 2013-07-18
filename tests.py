from __future__ import absolute_import

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Context
UserModel = get_user_model()

from django_dynamic_fixture import G

from binder.test_utils import AptivateEnhancedTestCase
from .models import LogFrame, Milestone

class LogframeTest(AptivateEnhancedTestCase):
    def test_create_view_formsets(self):
        log_frame = G(LogFrame)
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

        indicator = indicators[0]
        from django.forms.models import ModelForm
        self.assertIsInstance(indicator, ModelForm)
        from .models import Indicator
        self.assertIsInstance(indicator.instance, Indicator)

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

