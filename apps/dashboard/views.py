from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import os
import shutil

from utils.charts import weekdays
from utils.charts import lightRed, lightBlue, lightYellow, lightCyan, lightPurple, lightOrange, lightGreen

from services import measurement_statistics as ms
from services.export_statistics import ExportStatistics

@login_required
def statistics_view(request):
    user_organization = request.user.organization
    organization_image_url = user_organization.image_file.url if user_organization and user_organization.image_file else None
    return render(request, 'dashboard.html', {'organization_image_url': organization_image_url})
    # return render(request, 'dashboard.html', {})


@login_required
def get_filter_options(request):
    queryset = ms.fetch_measurement_years(request.user.organization)
    options = [ metrics["year"] for metrics in queryset ]

    return JsonResponse({
        "options": options,
    })


@login_required
def get_monthly_average(request, year):
    metrics_dict = ms.fetch_monthly_average(request.user.organization, year)

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
    TOP_N = 5
    queryset = ms.fetch_top_peak_times(request.user.organization, year, TOP_N)

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

    for data in queryset:
        formatted_time = '{:02d}:00'.format(data['hour'])
        chart_data['data']['labels'].append(formatted_time)
        chart_data['data']['datasets'][0]['data'].append(data['exceeded_threshold_count'])

    return JsonResponse(chart_data)


@login_required
def get_top_peak_weekdays(request, year):
    queryset = ms.fetch_top_peak_weekdays(request.user.organization, year)
    
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

    days_of_week = {idx: day for idx, day in enumerate(weekdays, start=1)}
    occurrences_by_day = {day_name: 0 for day_number, day_name in days_of_week.items()}

    for data in queryset:
        weekday_number = data['weekday']
        weekday_name = days_of_week.get(weekday_number, 'Desconhecido')
        occurrences_by_day[weekday_name] = data['exceeded_threshold_count']

    for day, count in occurrences_by_day.items():
        chart_data['data']['labels'].append(day)
        chart_data['data']['datasets'][0]['data'].append(count)

    return JsonResponse(chart_data)


@login_required
def get_locations_average(request, year):
    TOP_N = 8
    year = int(year)
    location_data_dict = ms.fetch_locations_average(request.user.organization, year, TOP_N)

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

    for location, data in location_data_dict.items():
        chart_data['data']['labels'].append(location)
        chart_data['data']['datasets'][0]['data'].append(data['avg_value'])
        chart_data['data']['datasets'][1]['data'].append(data['threshold'])

    return JsonResponse(chart_data)


@login_required
def save_as_excel(request, year):

    exporter = ExportStatistics(request.user.organization, year)
    zip_filepath = exporter.export()

    download_zipfile = _get_temp_zipfile_name(year)   

    with open(zip_filepath, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{download_zipfile}"'

    _remove_temp_directory(zip_filepath)

    return response


def _get_temp_zipfile_name(year):
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'export{year}_{current_datetime}.zip'


def _remove_temp_directory(zip_filepath):
    temp_dir = os.path.dirname(zip_filepath)
    shutil.rmtree(temp_dir)
