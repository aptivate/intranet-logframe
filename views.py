from __future__ import absolute_import

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Output, LogFrame, Indicator, SubIndicator
from .forms import OutputForm, IndicatorFormSet

class OutputBase(object):
    context_object_name = 'output'
    queryset = Output.objects.all()
    form_class = OutputForm
    template_name = 'logframe/output_edit_form.html'
    log_frame = LogFrame.objects.first()

    def get_context_data(self, **kwargs):
        context = super(OutputBase, self).get_context_data(**kwargs)
        context['milestones'] = self.log_frame.milestone_set.all()
        context['indicators'] = self.create_indicator_formset()
        return context

    def create_indicator_formset(self):
        output = self.get_object()

        indicator_formset = IndicatorFormSet(
            data=(self.request.POST if self.request.method == 'POST' else None),
            instance=output,
            initial=[
                {'name': 'Indicator I.1',
                 'description': '',
                },
                {'name': 'Indicator I.2',
                 'description': '',
                }
            ])

        for form in indicator_formset:
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

        return indicator_formset

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse('logframe-output-update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        indicator_formset = self.create_indicator_formset()
        if not indicator_formset.is_valid():
            return self.form_invalid(form)

        if form.instance.order is None:
            from django.db.models import Max
            max_order = Output.objects.filter(log_frame=self.log_frame).aggregate(Max('order'))['order__max']
            if max_order is None:
                new_order = 1
            else:
                new_order = max_order + 1
            form.instance.order = new_order

        # save the Output object before its dependents:
        response = super(OutputBase, self).form_valid(form)
        indicator_formset.save()
        return response

class OutputCreate(OutputBase, CreateView):
    def get_form_kwargs(self):
        kwargs = super(OutputCreate, self).get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_object(self):
        return Output(log_frame=self.log_frame)

class OutputUpdate(OutputBase, UpdateView):
    pass

