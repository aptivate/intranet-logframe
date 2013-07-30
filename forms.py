from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.functional import cached_property

from models import Output, Indicator, SubIndicator, Target

class BaseIndicatorFormSet(BaseInlineFormSet):
    @cached_property
    def forms(self):
        forms = super(BaseIndicatorFormSet, self).forms
        for form in forms:
            form.empty = False
        empty = self.empty_form # for use by javascript
        empty.empty = True
        forms.append(empty)
        return forms

IndicatorFormSet = inlineformset_factory(Output, Indicator, extra=1,
    formset=BaseIndicatorFormSet)
TargetFormSet = inlineformset_factory(SubIndicator, Target, extra=0)

class OutputForm(forms.ModelForm):
    class Meta:
        model = Output

    def __init__(self, **kwargs):
        super(OutputForm, self).__init__(**kwargs)
        self.fields['order'].required = False
