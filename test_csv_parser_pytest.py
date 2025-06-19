import pytest
from io import StringIO
from csv_parser import CSVParser

@pytest.fixture
def with_header():
    return StringIO(
        "name,surname,age,city,country,position\n"
        "Alice,Smith,30,Paris,France,Engineer\n"
    )

@pytest.fixture
def no_header():
    return StringIO(
        "Ben,Brown,22,Amsterdam,Netherlands,Dev\n"
        "Anna,Green,23,Groningen,Netherlands,QA\n"
        "Tony,Bluee,43,\"New York\",US,Project Manager\n"
    )

def test_properties_with_header(with_header):
    parser = CSVParser(with_header)
    assert parser.delimiter == ","
    assert parser.quotechar == '"'

def test_parse_with_header(with_header):
    parser = CSVParser(with_header)
    rows = parser.parse()
    assert rows == [{
        "name": "Alice", "surname": "Smith", "age": 30,
        "city": "Paris", "country": "France", "position": "Engineer"
    }]

def test_parse_no_header(no_header):
    custom_headers = ['name', 'surname', 'age', 'city', 'country', 'position']
    parser = CSVParser(no_header, custom_headers)
    rows = parser.parse()
    assert rows == [{
        "name": "Ben", "surname": "Brown", "age": 22,
        "city": "Amsterdam", "country": "Netherlands", "position": "Dev"
    },
    {
        "name": "Anna", "surname": "Green", "age": 23,
        "city": "Groningen", "country": "Netherlands", "position": "QA"
    },
    {
        "name": "Tony", "surname": "Bluee", "age": 43,
        "city": "New York", "country": "US", "position": "Project Manager"
    },
]

def test_skip_rows_missing_fields():
    custom_headers = ['name', 'surname', 'age', 'city', 'country', 'position']
    src = StringIO(
        "name,surname,age,city,country,position\n"
        "Unknown,,20,,,Intern\n"
        "Carol,Doe,,London,UK,Manager\n"
        "Dave,Doe,40,Seattle,USA,\n"
    )
    parser = CSVParser(src, custom_headers)
    rows = parser.parse()
    assert rows == [{
        "name": "Dave", "surname": "Doe", "age": 40,
        "city": "Seattle", "country": "USA", "position": "Unknown"
    }]
