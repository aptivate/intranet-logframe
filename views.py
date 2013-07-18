from __future__ import absolute_import

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Output, LogFrame, Indicator, SubIndicator
from .forms import OutputForm, IndicatorFormSet

class OutputCreate(CreateView):
    context_object_name = 'output'
    queryset = Output.objects.all()
    form_class = OutputForm
    template_name = 'logframe/output_edit_form.html'
    log_frame = LogFrame.objects.first()

    def get_context_data(self, **kwargs):
        context = super(OutputCreate, self).get_context_data(**kwargs)
        context['milestones'] = self.log_frame.milestone_set.all()
        output = Output(log_frame=self.log_frame)
        indicators = context['indicators'] = IndicatorFormSet(instance=output,
            initial=[
                {'name': 'Indicator I.1',
                 'description': '',
                },
                {'name': 'Indicator I.2',
                 'description': '',
                }
            ])

        for form in indicators:
            indicator = form.instance
            indicator.output = output

            # Subclass ModelForm for SubIndicator, to populate new (empty)
            # instances of SubIndicator with the correct Indicator, so that
            # they can get their Milestones.
            from django.forms.models import ModelForm
            class CustomSubIndicatorForm(ModelForm):
                class Meta:
                    model = SubIndicator
                def __init__(self, instance=None, **kwargs):
                    if instance is None:
                        instance = SubIndicator(indicator=indicator)
                    super(CustomSubIndicatorForm, self).__init__(
                        instance=instance, **kwargs)

            from django.forms.models import inlineformset_factory
            SubIndicatorFormSet = inlineformset_factory(Indicator,
                SubIndicator, extra=1, form=CustomSubIndicatorForm)

            form.subindicators = SubIndicatorFormSet(instance=indicator,
                initial=[
                    {'indicator': indicator}
                ])
            for sif in form.subindicators:
                subindicator = sif.instance
                from .forms import TargetFormSet
                sif.targets = TargetFormSet(
                    queryset=subindicator.targets_fake_queryset,
                    instance=subindicator,
                    prefix="subindicator_%s_targets" % subindicator.pk)
        return context
