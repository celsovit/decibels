from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractHour, ExtractWeekDay
from django.db.models import Count, F, Q, Avg
from django.http import JsonResponse

from utils.charts import months, weekdays, get_year_dict
from utils.charts import lightRed, lightBlue, lightYellow, lightCyan, lightPurple, lightOrange, lightGreen

from measurement.models import Measurement


@login_required
def statistics_view(request):
    user_organization = request.user.organization
    organization_image_url = user_organization.image_file.url if user_organization and user_organization.image_file else None
    return render(request, 'dashboard.html', {'organization_image_url': organization_image_url})
    # return render(request, 'dashboard.html', {})


@login_required
def get_filter_options(request):
    user_organization = request.user.organization

    grouped_measurements = (Measurement.objects
            .filter(location__organization=user_organization)
            .annotate(year=ExtractYear("registration_date")).values("year")
            .order_by("-year")
            .distinct()
    )

    options = [ metrics["year"] for metrics in grouped_measurements ]

    return JsonResponse({
        "options": options,
    })


@login_required
def get_monthly_average(request, year):
    user_organization = request.user.organization

    measurements = Measurement.objects.filter(
        Q(location__organization=user_organization) &
        Q(registration_date__year=year)
    )

    grouped_measurements = (measurements
        .annotate(month=ExtractMonth('registration_date'))
        .values('month')
        .annotate(average=Avg('measured_value'))
        .values('month', 'average')
        .order_by('month')
    )
    
    metrics_dict = get_year_dict()

    for group in grouped_measurements:
        metrics_dict[months[ group['month'] - 1 ]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Titulo { year }',
        'data': {
            'labels': list(metrics_dict.keys()),
            'datasets': [{
                'label': 'Medição',
                'backgroundColor': lightBlue,
                'borderColor': 'dodgerblue',
                'borderWidth': 2,
                'data': list(metrics_dict.values())
            }]
        },
    })


@login_required
def get_top_peak_times(request, year):
    user_organization = request.user.organization
    TOP_N = 5

    chart_data = {
        'title': f'Top {TOP_N} Peak Times in {year}',
        'data': {
            'labels': [],
            'datasets': [{
                'label': 'Registros de Pico',
                'backgroundColor': [
                    lightRed,
                    lightBlue,
                    lightYellow,
                    lightCyan,
                    lightPurple,
                ],
                'borderColor': 'WhiteSmoke',
                'data': [],
            }]
        }
    }

    peak_times = (
        Measurement.objects
        .filter(
            Q(location__organization=user_organization) &
            Q(registration_date__year=year) &
            Q(measured_value__gt=F('location__threshold'))
        )
        .annotate(hour=ExtractHour('registration_date'))
        .values('hour')
        .annotate(exceeded_threshold_count=Count('id'))
        .order_by('-exceeded_threshold_count')[:TOP_N]
    )

    for data in peak_times:
        formatted_time = '{:02d}:00'.format(data['hour'])
        chart_data['data']['labels'].append(formatted_time)
        chart_data['data']['datasets'][0]['data'].append(data['exceeded_threshold_count'])

    return JsonResponse(chart_data)


@login_required
def get_top_peak_weekdays(request, year):
    user_organization = request.user.organization

    chart_data = {
        'title': f'Top Peak Weekday in { year }',
        'data': {
            'labels': [],
            'datasets': [{
                'label': 'Registros de Pico',
                'backgroundColor': [
                    lightRed,
                    lightBlue,
                    lightYellow,
                    lightCyan,
                    lightPurple,
                    lightOrange,
                    lightGreen,
                ],
                'borderColor': 'WhiteSmoke',
                'data': [],
            }]
        }
    }

    peak_weekdays = (
        Measurement.objects
        .filter(
            Q(location__organization=user_organization) &
            Q(registration_date__year=year) &
            Q(measured_value__gt=F('location__threshold'))
        )
        .annotate(weekday=ExtractWeekDay('registration_date')).values('weekday')
        .annotate(exceeded_threshold_count=Count('id'))
    )

    days_of_week = {idx: day for idx, day in enumerate(weekdays, start=1)}
    occurrences_by_day = {day_name: 0 for day_number, day_name in days_of_week.items()}

    for data in peak_weekdays:
        weekday_number = data['weekday']
        weekday_name = days_of_week.get(weekday_number, 'Desconhecido')
        occurrences_by_day[weekday_name] = data['exceeded_threshold_count']

    for day, count in occurrences_by_day.items():
        chart_data['data']['labels'].append(day)
        chart_data['data']['datasets'][0]['data'].append(count)

    return JsonResponse(chart_data)


@login_required
def get_locations_average(request, year):
    user_organization = request.user.organization
    TOP_N = 8
    year = int(year)

    chart_data = {
        'title': f'Top { TOP_N } Locations with Highest Average Measurements in {year}',
        'data': {
            'labels': [],
            'datasets': [
                {
                    'type': 'bar',
                    'label': 'Medição Média',
                    'backgroundColor': lightOrange,
                    'borderColor': 'orange',
                    'borderWidth': 2,
                    'data': [],
                },
                {
                    'type': 'line',
                    'label': 'Limite',
                    'fill': False,
                    'borderColor': lightBlue,
                    'borderWidth': 3,
                    'data': [],
                },
            ],
        },
    }

    top_locations = (
        Measurement.objects
        .filter(
            Q(location__organization=user_organization) &
            Q(registration_date__year=year)
        )
        .values('location__name', 'location__threshold')
        .annotate(avg_value=Avg('measured_value'))
        .order_by('-avg_value')[:TOP_N]
    )

    location_data_dict = {
        location_data['location__name']: {
            'avg_value': location_data['avg_value'],
            'threshold': location_data['location__threshold']
        } for location_data in top_locations
    }

    for location, data in location_data_dict.items():
        chart_data['data']['labels'].append(location)
        chart_data['data']['datasets'][0]['data'].append(data['avg_value'])
        chart_data['data']['datasets'][1]['data'].append(data['threshold'])

    return JsonResponse(chart_data)