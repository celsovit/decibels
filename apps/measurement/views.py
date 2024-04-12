from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from datetime import datetime
import csv

from utils.datetime_custom import get_start_of_day, get_end_of_day
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
        query_params = self.request.session.get('measurement_query_params')
        user = self.request.user

        if query_params and self.has_parameters(query_params):
            start_date_str = f"{query_params['start_date']}:00"
            end_date_str = f"{query_params['end_date']}:59"

            start_date = make_aware(datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S"))
            end_date = make_aware(datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S"))

            return (
                Measurement.objects.filter(
                    location__organization=user.organization,
                    location=query_params['location'],
                    registration_date__range=(start_date, end_date)
                ).order_by('registration_date')
            )
        
        return Measurement.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        query_params = self.request.session.get('measurement_query_params')

        context['locations'] = Location.objects.filter(organization=user.organization).order_by('name')

        # if query_params and self.has_parameters(query_params):
        context['selected_location'] = query_params['location']
        context['selected_start_date'] = query_params['start_date']
        context['selected_end_date'] = query_params['end_date']
        # else:
        #     context['selected_location'] = context['locations'].first()
        #     context['selected_start_date'] = get_start_of_day().strftime('%Y-%m-%dT%H:%M')
        #     context['selected_end_date'] = get_end_of_day().strftime('%Y-%m-%dT%H:%M')
        
        return context


    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':

            query_params_get = self.get_parameters(self.request.GET)
            query_params_session = request.session.get('measurement_query_params')

            if self.has_parameters(query_params_get):
                request.session['measurement_query_params'] = query_params_get
            elif not query_params_session:
                query_params_get['start_date'] = get_start_of_day().strftime('%Y-%m-%dT%H:%M')
                query_params_get['end_date'] = get_end_of_day().strftime('%Y-%m-%dT%H:%M')
                request.session['measurement_query_params'] = query_params_get

        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def get_parameters(data):
        return {
            'location': data.get('location'),
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
        }
    
    @staticmethod
    def has_parameters(query_params):
        return all(value is not None for value in query_params.values())


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


@method_decorator(login_required, name='dispatch')
class MeasurementDeleteView(DeleteView):
    model = Measurement
    success_url = reverse_lazy('measurement_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
    

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
            registration_date = make_aware(datetime.strptime(row['registration_date'], '%Y-%m-%d %H:%M:%S'))

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
