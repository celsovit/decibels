from django import forms

from measurement.models import Measurement
from location.models import Location

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['location', 'registration_date', 'measured_value']

    def __init__(self, user, *args, **kwargs):
        # filtrar locations da organization do usuário
        super(MeasurementForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(organization=user.organization)
