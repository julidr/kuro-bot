import datetime

import pytest

from src.utils.date_utils import convert_str_to_date, convert_date_to_str


class TestConvertStrToDate:

    def test_when_no_format_is_specified_and_correct_date_str(self):
        # Arrange
        sample_date = '01/08'

        # Act
        result = convert_str_to_date(sample_date)

        # Assert
        assert result.day == 1
        assert result.month == 8

    def test_when_no_format_is_specified_and_incorrect_date_str(self):
        # Arrange
        bad_sample_date = '01-08-2021'
        expected_error_message = "time data '{0}' does not match format '%d/%m'".format(bad_sample_date)

        # Act
        with pytest.raises(ValueError) as exception:
            convert_str_to_date(bad_sample_date)

        # Assert
        assert str(exception.value) == expected_error_message

    def test_when_format_is_specified_and_correct_date_str(self):
        # Arrange
        sample_date = '01-08-2003'
        sample_format = '%d-%m-%Y'

        # Act
        result = convert_str_to_date(sample_date, sample_format)

        # Assert
        assert result.day == 1
        assert result.month == 8
        assert result.year == 2003

    def test_when_format_is_specified_and_incorrect_date_str(self):
        # Arrange
        bad_sample_date = '01/08'
        sample_format = '%d-%m-%Y'
        expected_error_message = "time data '{0}' does not match format '{1}'".format(bad_sample_date, sample_format)

        # Act
        with pytest.raises(ValueError) as exception:
            convert_str_to_date(bad_sample_date, sample_format)

        # Assert
        assert str(exception.value) == expected_error_message


class TestConvertDateToStr:

    def test_when_date_is_str_not_specified_date_and_str_format_and_valid_date(self):
        # Arrange
        sample_date = '01/08'
        expected_result = 'August 01'

        # Act
        result = convert_date_to_str(sample_date)

        # Assert
        assert expected_result == result

    def test_when_date_is_str_not_specified_date_and_str_format_and_invalid_date(self):
        # Arrange
        bad_sample_date = '01-08-2021'
        expected_error_message = "time data '{0}' does not match format '%d/%m'".format(bad_sample_date)

        # Act
        with pytest.raises(ValueError) as exception:
            convert_date_to_str(bad_sample_date)

        # Assert
        assert str(exception.value) == expected_error_message

    def test_when_date_is_str_specified_date_format_and_valid_date(self):
        # Arrange
        sample_date = '01/08'
        sample_format = '%m-%d'
        expected_result = '08-01'

        # Act
        result = convert_date_to_str(sample_date, sample_format)

        # Assert
        assert expected_result == result

    def test_when_date_is_str_specified_date_format_and_invalid_date(self):
        # Arrange
        bad_sample_date = '01-08-2021'
        sample_format = '%m-%d-%y'
        expected_error_message = "time data '{0}' does not match format '%d/%m'".format(bad_sample_date)

        # Act
        with pytest.raises(ValueError) as exception:
            convert_date_to_str(bad_sample_date, sample_format)

        # Assert
        assert str(exception.value) == expected_error_message

    def test_when_date_is_str_specified_str_format_and_valid_date(self):
        # Arrange
        sample_date = '01-08-2003'
        sample_format = '%d-%m-%Y'
        expected_result = 'August 01'

        # Act
        result = convert_date_to_str(sample_date, date_str_format=sample_format)

        # Assert
        assert expected_result == result

    def test_when_date_is_str_specified_str_format_and_invalid_date(self):
        # Arrange
        bad_sample_date = '2021/01/08'
        sample_format = '%m-%d-%y'
        expected_error_message = "time data '{0}' does not match format '{1}'".format(bad_sample_date, sample_format)

        # Act
        with pytest.raises(ValueError) as exception:
            convert_date_to_str(bad_sample_date, date_str_format=sample_format)

        # Assert
        assert str(exception.value) == expected_error_message

    def test_when_date_is_str_specified_date_and_str_format_and_valid_date(self):
        # Arrange
        sample_date = '01-08-2003'
        str_sample_format = '%d-%m-%Y'
        date_sample_format = '%d %b'
        expected_result = '01 Aug'

        # Act
        result = convert_date_to_str(sample_date, date_sample_format, str_sample_format)

        # Assert
        assert expected_result == result

    def test_when_is_date_not_specified_date_format_and_valid_date(self):
        # Arrange
        sample_date = datetime.datetime(2003, 8, 1)
        expected_result = 'August 01'

        # Act
        result = convert_date_to_str(sample_date)

        # Assert
        assert expected_result == result

    def test_when_is_date_specified_date_format_and_valid_date(self):
        # Arrange
        sample_date = datetime.datetime(2003, 8, 1)
        sample_format = '%d-%m-%Y'
        expected_result = '01-08-2003'

        # Act
        result = convert_date_to_str(sample_date, sample_format)

        # Assert
        assert expected_result == result
