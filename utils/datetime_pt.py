import datetime

def years_list(start_year=None, end_year=None):
    if start_year is None:
        current_year = datetime.datetime.now().year
        start_year = current_year - 5

    if end_year is None:
        end_year = start_year + 15

    return [ano for ano in range(start_year, end_year)]

MONTHS = [
    'Janeiro', 
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro',
]

YEARS = years_list()  # Chama a função para criar a lista de anos automaticamente
