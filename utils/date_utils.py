from datetime import datetime


def convert_str_to_date(date: str):
    return datetime.strptime(date, '%d/%m')


def convert_date_to_day_and_month(date):
    if type(date) == str:
        date = convert_str_to_date(date).date()
    return datetime.strftime(date, '%B %d')
