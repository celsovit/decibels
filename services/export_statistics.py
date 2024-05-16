import os
import zipfile
import tempfile
import pandas as pd

from . import measurement_statistics as ms
from utils.charts import weekdays

class ExportStatistics:

    def __init__(self, organization, year):
        self.organization = organization
        self.year = year
        self.temp_dir = None
        self.excel_files = []


    def export(self):
        self.temp_dir = tempfile.mkdtemp()   # Cria um diretório temporário

        self._export_monthly_average()
        self._export_top_peak_times()
        self._export_top_peak_weekdays()
        self._export_top_locations()

        return self._zip_files()


    def _export_monthly_average(self):
        metrics_dict = ms.fetch_monthly_average(self.organization, self.year)
        df = pd.DataFrame(metrics_dict.items(), columns=['Mês', 'Média'])
        self._save_to_excel(df, 'monthly_average_data.xlsx')


    def _export_top_peak_times(self):
        peak_times = ms.fetch_top_peak_times(self.organization, self.year, TOP_N=5)

        translated_columns = {
            'hour': 'hora',
            'exceeded_threshold_count': 'registros_de_pico'
        }
        df = pd.DataFrame(peak_times).rename(columns=translated_columns)
        df['hora'] = df['hora'].apply(lambda x: f'{x:02}:00')   # formatado como hora

        self._save_to_excel(df, 'top_peak_times_data.xlsx')


    def _export_top_peak_weekdays(self):
        peak_weekdays = ms.fetch_top_peak_weekdays(self.organization, self.year)

        for data in peak_weekdays:
            idx = data['weekday'] - 1
            data['weekday'] = weekdays[idx]

        translated_columns = {
            'weekday': 'dia_da_semana',
            'exceeded_threshold_count': 'registros_de_pico'
        }
        df = pd.DataFrame(peak_weekdays).rename(columns=translated_columns)

        self._save_to_excel(df, 'top_peak_weekdays_data.xlsx')


    # def _export_top_locations(self):
    #     top_locations = ms.fetch_locations_average(self.organization, self.year, TOP_N=8)
    #     df = pd.DataFrame(top_locations)
    #     self._save_to_excel(df, 'top_locations_data.xlsx')

    def _export_top_locations(self):
        top_locations = ms.fetch_locations_average(self.organization, self.year, TOP_N=8)
        
        location_data = []
        for location, data in top_locations.items():
            location_data.append({'Locação': location, 'Média': data['avg_value'], 'Limite': data['threshold']})

        df = pd.DataFrame(location_data)
        self._save_to_excel(df, 'top_locations_data.xlsx')


    def _save_to_excel(self, df, filename):
        file_path = os.path.join(self.temp_dir, filename)
        df.to_excel(file_path, index=False)
        self.excel_files.append(file_path)


    def _zip_files(self):
        zipfile_path = os.path.join(self.temp_dir, 'exported_data.zip')
        with zipfile.ZipFile(zipfile_path, 'w') as zipf:
            for excel_file_path in self.excel_files:
                zipf.write(excel_file_path, os.path.basename(excel_file_path))

        return zipfile_path
