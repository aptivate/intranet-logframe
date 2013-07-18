from django import forms
from django.forms.models import inlineformset_factory

from models import Output, Indicator, SubIndicator, Target

IndicatorFormSet = inlineformset_factory(Output, Indicator, extra=1)
TargetFormSet = inlineformset_factory(SubIndicator, Target, extra=0)

class OutputForm(forms.ModelForm):
    class Meta:
        model = Output

    def __init__(self, **kwargs):
        super(OutputForm, self).__init__(**kwargs)
        self.fields['order'].required = False
