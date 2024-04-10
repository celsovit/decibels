from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from datetime import datetime
import csv

from utils.datetime_pt import MONTHS, YEARS
from .forms import MeasurementForm
from .models import Measurement
from location.models import Location


@method_decorator(login_required, name='dispatch')
class MeasurementListView(ListView):
    model = Measurement
    template_name = 'measurement_list.html'
    paginate_by = 8

    def get_queryset(self):
        parameters = MeasurementListView.get_parameters(self.request.GET)
        user = self.request.user

        if not parameters['location'] or not parameters['month'] or not parameters['year']:
            return []

        month_number = MONTHS.index(parameters['month']) + 1

        return (
            Measurement.objects.filter(
                location__organization=user.organization,
                location=parameters['location'],
                registration_date__year=parameters['year'],
                registration_date__month=month_number
            ).order_by('registration_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        filter = MeasurementListView.get_parameters(self.request.GET)

        context['locations'] = Location.objects.filter(organization=user.organization).order_by('name')
        context['months'] = MONTHS
        context['years'] = YEARS

        if filter['location']:
            context['selected_location'] = filter['location']
            context['selected_month'] = filter['month']
            context['selected_year'] = filter['year']
        else:
            context['selected_location'] = context['locations'].first()
            context['selected_month'] = MONTHS[datetime.now().month - 1]
            context['selected_year'] = str(datetime.now().year)
        
        return context
    
    @staticmethod
    def get_parameters(data):
        return {
            'location': data.get('location'),
            'month': data.get('month'),
            'year': data.get('year'),
        }


@method_decorator(login_required, name='dispatch')
class MeasurementCreateView(CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'measurement_edit.html'
    success_url = reverse_lazy('measurement_list')

    def get_form_kwargs(self):
        # filtrar locations da organization do usuário
        kwargs = super(MeasurementCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class MeasurementUpdateView(UpdateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'measurement_edit.html'
    success_url = reverse_lazy('measurement_list')

    def get_form_kwargs(self):
        # filtrar locations da organization do usuário
        kwargs = super(MeasurementUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        user = self.request.user
        return Measurement.objects.filter(location__organization=user.organization)


@method_decorator(login_required, name='dispatch')
class MeasurementDeleteView(DeleteView):
    model = Measurement
    template_name = 'measurement_delete.html'
    success_url = reverse_lazy('measurement_list')

    def get_queryset(self):
        user = self.request.user
        return Measurement.objects.filter(location__organization=user.organization)
    

@method_decorator(login_required, name='dispatch')
class MeasurementImportView(View):

    def __init__(self):
        super().__init__()
        self.reader = None
        self.batch_size = 1000

    def post(self, request):
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            
            try:
                if csv_file.name.endswith('.csv'):
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    self.reader = csv.DictReader(decoded_file, fieldnames=[
                        'location_id', 'registration_date', 'measured_value'
                    ])

                    for batch in self.read_csv_batch():
                        if batch:
                            Measurement.objects.bulk_create(batch)
                else:
                    raise ValidationError("O arquivo selecionado não é um arquivo CSV.")
                
            except ValueError as e:
                print(f'Erro ao processar arquivo CSV: {e}')

        return HttpResponseRedirect(reverse('measurement_list'))

    def read_csv_batch(self):
        batch = []
        count = 0

        for row in self.reader:
            location_id = row['location_id']
            measured_value = row['measured_value']
            registration_date = datetime.strptime(row['registration_date'], '%Y-%m-%d %H:%M:%S')

            measurement = Measurement(
                location_id=location_id,
                measured_value=measured_value,
                registration_date=registration_date
            )

            batch.append(measurement)
            count += 1

            if count >= self.batch_size:
                yield batch
                batch = []
                count = 0
    
        if batch:
            yield batch
