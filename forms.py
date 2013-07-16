from django import forms

from models import Output

class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        fields = ['order', 'description', 'impact_weighting', 'assumptions',
            'risk_rating']

