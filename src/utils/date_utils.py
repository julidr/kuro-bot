from datetime import datetime


def convert_str_to_date(date: str, date_format: str = '%d/%m') -> datetime:
    """
    Receive a date String and convert it into its respective datetime

    :param date: String to convert
    :param date_format: The format to be able to recognize the date String and transform it to datetime
    :return: A new datetime with the given information
    """
    return datetime.strptime(date, date_format)


def convert_date_to_str(date, date_format: str = '%B %d', date_str_format: str = '%d/%m') -> str:
    """
    Converts a date either str or datetime into an specific String format

    :param date: The date to transform into String, can be a str or a datetime
    :param date_format: The string format to transform the given date
    :param date_str_format: original format of the date in case that is an str
    :return: A string with the respective date information and format
    """
    if type(date) == str:
        date = convert_str_to_date(date, date_str_format)
    return datetime.strftime(date, date_format)
