from django.db.models.functions import ExtractYear, ExtractMonth, ExtractHour, ExtractWeekDay
from django.db.models import Count, F, Avg

from measurement.models import Measurement

from utils.charts import months, get_year_dict


def fetch_measurement_years(organization):
    """ Retorna um Django Queryset com os anos que possuem medições """

    years = (Measurement.objects
        .filter(location__organization=organization)
        .annotate(year=ExtractYear('registration_date')).values('year')
        .order_by('-year')
        .distinct()
    )

    return years


def fetch_monthly_average(organization, year):
    """ Retorna um dicionário com os meses do ano e suas respectivas médias """

    grouped_measurements = (
        Measurement.objects
            .filter(location__organization=organization, registration_date__year=year)
            .annotate(month=ExtractMonth('registration_date'))
            .values('month')
            .annotate(average=Avg('measured_value'))
            .values('month', 'average')
            .order_by('month')
        )

    metrics_dict = get_year_dict()

    for group in grouped_measurements:
        month_name = months[ group['month'] - 1 ]
        metrics_dict[month_name] = round(group['average'], 2)

    return metrics_dict


def fetch_top_peak_times(organization, year, TOP_N = 5):
    """ Retorna um Django Queryset com os horários de pico de medição """

    peak_times = (
        Measurement.objects
            .filter(
                location__organization=organization,
                registration_date__year=year,
                measured_value__gt=F('location__threshold')
            )
            .annotate(hour=ExtractHour('registration_date'))
            .values('hour')
            .annotate(exceeded_threshold_count=Count('id'))
            .order_by('-exceeded_threshold_count')[:TOP_N]
    )

    sorted_top_peak_times = sorted(peak_times, key=lambda x: x['hour'])

    return sorted_top_peak_times


def fetch_top_peak_weekdays(organization, year):
    """ Retorna um Django Queryset com a semana e os picos de medição de cada dia """

    peak_weekdays = (
        Measurement.objects
            .filter(
                location__organization=organization,
                registration_date__year=year,
                measured_value__gt=F('location__threshold')
            )
            .annotate(weekday=ExtractWeekDay('registration_date'))
            .values('weekday')
            .annotate(exceeded_threshold_count=Count('id'))
            .order_by('weekday')
    )

    return peak_weekdays


def fetch_locations_average(organization, year, TOP_N = 8):
    """ Retorna um dicionário com N locais de valor médio mais alto """

    top_locations = (
        Measurement.objects
            .filter(
                location__organization=organization,
                registration_date__year=year
            )
            .values('location__name', 'location__threshold')
            .annotate(avg_value=Avg('measured_value'))
            .order_by('-avg_value')[:TOP_N]
    )

    location_data_dict = {
        data['location__name'] : { 'avg_value': data['avg_value'], 'threshold': data['location__threshold'] } for data in top_locations
    }

    return location_data_dict
