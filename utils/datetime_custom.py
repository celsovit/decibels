from datetime import datetime, time

def get_start_of_day(date=None):
    """
    Retorna a primeira hora do dia para a data especificada.
    Se nenhuma data for fornecida, usa a data atual.
    """
    if date is None:
        date = datetime.now().date()
    return datetime.combine(date, time.min)


def get_end_of_day(date=None):
    """
    Retorna a última hora do dia para a data especificada.
    Se nenhuma data for fornecida, usa a data atual.
    """
    if date is None:
        date = datetime.now().date()
    return datetime.combine(date, time.max)