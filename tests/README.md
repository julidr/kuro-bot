# Running Kuro Bot Tests
[![pytest](https://img.shields.io/badge/pytest-6.2.4-009bdb)](https://docs.pytest.org/en/6.2.x/)
[![pytest-cov](https://img.shields.io/badge/pytest%20cov-2.12.1-009bdb)](https://pytest-cov.readthedocs.io/en/latest/index.html)
[![coverage-badge](https://img.shields.io/badge/coverage%20badge-1.0.1-009bdb)](https://pypi.org/project/coverage-badge/)

All tests should go in `tests/` folder with its respective package organization that reflects the `src/` folder.

To avoid dealing with a lot of issues and because I'm kind of lazy, don't forget to add the `__init__.py` file
in each directory inside `tests/`.

## Building Tests

### Test Files
Test files should always start with the `test` prefix follow by the name of the `.py` file that they are going to test.
```
date_utils.py --> test_date_utils.py
```

### Test Classes
All test files are grouping tests in classes depending on the scope and number of tests. 
In this case for date utils classes executed tests for different scenarios of the methods in `date_utils.py`

Those classes should start with `Test` prefix and then the name of the method that is going to be tests in **camel-case**.
```python
class TestConvertStrToDate
```

### Test Methods
The name of all methods inside one test class should start with `test` prefix follow by `when` and one explanation of
the scenario that is going to be tested.

The content of each method should be organized in its respective _arrange_, _act_ and _assert_.
```python
def test_when_no_format_is_specified_and_correct_date_str(self):
    # Arrange
    sample_date = '01/08'

    # Act
    result = convert_str_to_date(sample_date)

    # Assert
    assert result.day == 1
    assert result.month == 8
```

## Executing Tests

Test are execute by `pytest`, so writing this simple command will execute all test that it finds in `tests/` folder
and that have the conventions mentioned before, generating a report with the tests results.

To obtain the coverage of the project execute the following command:
```
pytest --cov=src tests/
```
Finally, to generate or update the coverage badge, once the pytest coverage ran then execute:
```
coverage-badge -o coverage.svg
```