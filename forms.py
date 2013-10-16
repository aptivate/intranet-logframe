from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.functional import cached_property

from models import Output, Indicator, SubIndicator, Target


class BaseInlineFormSetWithEmpty(BaseInlineFormSet):
    @cached_property
    def forms(self):
        forms = super(BaseInlineFormSetWithEmpty, self).forms
        for form in forms:
            form.empty = False
        empty = self.empty_form  # for use by javascript
        empty.empty = True
        forms.append(empty)
        return forms


class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Output Description'}),
            'assumptions': forms.Textarea(attrs={'placeholder': 'Assumptions'}),
        }

    def __init__(self, **kwargs):
        super(OutputForm, self).__init__(**kwargs)
        self.fields['order'].required = False


class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Indicator Description'}),
            'source': forms.Textarea(attrs={'placeholder': 'Enter source for indicator data'}),
        }


class SubIndicatorForm(forms.ModelForm):
    class Meta:
        model = SubIndicator
        widgets = {
            'name': forms.Textarea(attrs={'placeholder': 'Name'}),
        }


class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        widgets = {
            'value': forms.TextInput(attrs={'placeholder': 'Enter value'}),
        }

IndicatorFormSet = inlineformset_factory(
    Output, Indicator, extra=0,
    form=IndicatorForm,
    formset=BaseInlineFormSetWithEmpty)
TargetFormSet = inlineformset_factory(
        SubIndicator, Target, form=TargetForm, extra=0)
