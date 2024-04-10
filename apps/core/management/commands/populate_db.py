from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.utils import timezone
import random

from measurement.models import Measurement
from location.models import Location
from organization.models import Organization
from users.models import CustomUser
from django.db import transaction


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados gerados randomicamente.'

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, nargs='?', default=None, help='Data inicial no formato YYYY-MM-DD')
        parser.add_argument('end_date', type=str, nargs='?', default=None, help='Data final no formato YYYY-MM-DD')
        parser.add_argument('--no_truncate', action='store_true', default=False, help='Excluir dados existentes antes de executar')

    def handle(self, *args, **kwargs):
        start_date_str = kwargs['start_date']
        end_date_str = kwargs['end_date']
        truncate = not kwargs['no_truncate']

        if start_date_str:
            self.start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        else:
            self.start_date = datetime.now().replace(month=1, day=1)

        if end_date_str:
            self.end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        else:
            self.end_date = Command.get_last_date_of_year(self.start_date)
        
        with transaction.atomic():
            self.create_organization()
            self.create_user()
            self.populate_measurements(truncate)
        
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso.'))

    def populate_measurements(self, truncate):
        if truncate:
            Measurement.objects.all().delete()
         
        locations = (
           'Dante Rodini',
           'Biblioteca', 
           'Lago', 
           'RH', 
           'Pq Ecológico', 
           'Rodoviária', 
           'Caic', 
           'Terminal', 
        )

        for local_str in locations:
            organization = Organization.objects.get(pk=1)
            location = Location.objects.get_or_create(name=local_str, organization=organization)[0]
            measurements = []

            current_date = self.start_date
            while current_date <= self.end_date:
                if current_date.weekday() == 5:
                    # salta fim de semana
                    current_date += timedelta(days=2)
                
                entries_qty = random.randint(11, 71)

                for _ in range(entries_qty):
                    random_hour = random.randint(8, 17)
                    random_minute = random.randint(0, 59)
                    random_second = random.randint(0, 59)

                    temp_date = current_date.replace(
                        hour=random_hour, minute=random_minute, second=random_second
                    )

                    min_value = random.randint(5, 20)
                    max_value = random.randint(62, 98)
                    measured_value = round(random.uniform(min_value, max_value), 2)

                    current_date_aware = timezone.make_aware(temp_date)

                    measurements.append(Measurement(
                        location=location, 
                        registration_date=current_date_aware, 
                        measured_value=measured_value
                    ))

                current_date += timedelta(days=1)

            Measurement.objects.bulk_create(measurements)

    def create_user(self):
        organization = Organization.objects.get(pk=1)
        if not CustomUser.objects.filter(username='user').exists():
            user = CustomUser.objects.create_user('user', 'user@example.com', 'user')
            user.organization = organization
            user.first_name='user'
            user.save()

    def create_organization(self):
        if not Organization.objects.filter(pk=1).exists():
            organization, created = Organization.objects.get_or_create(pk=1, defaults={
               'name': 'Nome da Organização',
               'image_file': 'brasoes/brasao_araras.png'
            })

    @staticmethod
    def get_last_date_of_year(date):
        last_day_of_year = datetime(date.year, 12, 31)
        return min(last_day_of_year, datetime.now())
