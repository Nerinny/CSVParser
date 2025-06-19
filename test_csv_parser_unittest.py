import unittest
from io import StringIO
from csv_parser import CSVParser


class TestCSVParser(unittest.TestCase):
    def setUp(self):
        self.csv_with_header = StringIO(
            "name,surname,age,city,country,position\n"
            "Alice,Smith,30,Paris,France,Engineer\n"
        )
        self.csv_without_header = StringIO(
            "Ben,Brown,22,Amsterdam,Netherlands,Dev\n"
            "Anna,Green,23,Groningen,Netherlands,QA\n"
            "Tony,Bluee,43,\"New York\",US,Project Manager\n"
        )

    def test_delimiter_and_quote(self):
        parser = CSVParser(self.csv_with_header)
        self.assertEqual(parser.delimiter, ",")
        self.assertEqual(parser.quotechar, '"')

    def test_parse_with_header(self):
        custom_headers = ['name', 'surname', 'age', 'city', 'country', 'position']
        parser = CSVParser(self.csv_with_header, custom_headers)
        rows = parser.parse()
        expected = [{
            "name": "Alice", "surname": "Smith", "age": 30,
            "city": "Paris", "country": "France", "position": "Engineer"
        }]
        self.assertEqual(rows, expected)

    def test_parse_without_header(self):
        custom_headers = ['name', 'surname', 'age', 'city', 'country', 'position']
        parser = CSVParser(self.csv_without_header, custom_headers)
        rows = parser.parse()
        expected = [{
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
            }
        ]
        self.assertEqual(rows, expected)

    def test_skip_invalid_rows(self):
        custom_headers = ['name', 'surname', 'age', 'city', 'country', 'position']
        src = StringIO(
            "name,surname,age,city,country,position\n"
            "Unknown,,20,,,Intern\n"
            "Carol,Doe,,London,UK,Manager\n"
            "Dave,Doe,40,Seattle,USA,\n"
        )
        parser = CSVParser(src, custom_headers)
        rows = parser.parse()
        expected = [{
        "name": "Dave", "surname": "Doe", "age": 40,
        "city": "Seattle", "country": "USA", "position": "Unknown"
        }]
        self.assertEqual(rows, expected)


if __name__ == '__main__':
    unittest.main()
