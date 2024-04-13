from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Avg, F, Count
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Location
from measurement.models import Measurement

from utils.charts import months, get_year_dict, lightBlue, lightOrange


@method_decorator(login_required, name='dispatch')
class LocationListView(ListView):
    model = Location
    template_name = 'location_list.html'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Location.objects.filter(organization=user.organization).order_by('name')


@method_decorator(login_required, name='dispatch')
class LocationCreateView(CreateView):
    model = Location
    fields = ('name', 'threshold')
    template_name = 'location_edit.html'
    success_url = reverse_lazy('location_list')

    def form_valid(self, form):
        # Define a organização do usuário atual para a localização criada
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class LocationUpdateView(UpdateView):
    model = Location
    fields = ('name', 'threshold')
    template_name = 'location_edit.html'
    success_url = reverse_lazy('location_list')


@method_decorator(login_required, name='dispatch')
class LocationDeleteView(DeleteView):
    model = Location
    success_url = reverse_lazy('location_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
    

class LocationFilterOptionsView(View):

    def get(self, request, *args, **kwargs):
        location_id = kwargs.get('pk')

        grouped_measurements = (Measurement.objects
            .filter(location=location_id)
            .annotate(year=ExtractYear('registration_date')).values('year')
            .order_by('-year')
            .distinct()
        )

        options = [ metrics["year"] for metrics in grouped_measurements ]

        return JsonResponse({
            "options": options,
        })


class LocationGraphicView(View):

    def get(self, request, *args, **kwargs):
        location_id = kwargs.get('pk')
        year = kwargs.get('year')

        data = {
            'labels': [],
            'datasets': [
                {
                    'type': 'bar',
                    'label': 'Número de Vezes Excedido',
                    'backgroundColor': lightOrange,
                    'borderColor': 'orange',
                    'borderWidth': 2,
                    'data': [],
                },
                {
                  'type': 'line',
                    'label': 'Média de Decibéis',
                    'fill': False,
                    'borderColor': lightBlue,
                    'borderWidth': 3,
                    'data': [],
                },
            ],
        }

        monthly_average = self.get_monthly_average(location_id, year)
        peak_monthly = self.get_peak_monthly(location_id, year)
        combined_metrics = self.combine_metrics(monthly_average, peak_monthly)

        for month, (monthly_avg, monthly_peak) in combined_metrics.items():
            data['labels'].append(month)
            data['datasets'][0]['data'].append(monthly_peak)
            data['datasets'][1]['data'].append(monthly_avg)

        return JsonResponse({
            'title': f'Titulo {year}',
            'data': data,
        })


    def get_monthly_average(self, location_id, year):

        monthly_average = (Measurement.objects
            .filter(
                location=location_id,
                registration_date__year=year
            )
            .annotate(month=ExtractMonth('registration_date'))
            .values('month')
            .annotate(average=Avg('measured_value'))
            .values('month', 'average')
            .order_by('month')
        )

        metrics_dict = get_year_dict()

        for group in monthly_average:
            month_name = months[group['month'] - 1]
            metrics_dict[month_name] = round(group['average'], 2)

        return metrics_dict


    def get_peak_monthly(self, location_id, year):

        peak_monthly_peaks = (Measurement.objects
            .filter(
                location=location_id,
                registration_date__year=year,
                measured_value__gt=F('location__threshold')
            )
            .annotate(month=ExtractMonth('registration_date'))
            .values('month')
            .annotate(exceeded_threshold_count=Count('id'))
            .order_by('month')
        )

        metrics_dict = get_year_dict()

        for group in peak_monthly_peaks:
            month_name = months[group['month'] - 1]
            metrics_dict[month_name] = group['exceeded_threshold_count']

        return metrics_dict


    def combine_metrics(self, monthly_average, peak_monthly):
        combined_metrics = {}

        for month in months:
            avg_value = monthly_average.get(month, 0)
            peak_value = peak_monthly.get(month, 0)
            combined_metrics[month] = (avg_value, peak_value)

        return combined_metrics
    
