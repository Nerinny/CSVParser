import csv
from _csv import Dialect
from csv import DictReader
from io import TextIOBase
from typing import Any, Type


class CSVParser:
    """CSV parser supporting custom delimiter, quoting and header logic"""

    def __init__(self, file: TextIOBase, custom_headers: list[str] | None  = None):
        """
        Initialize the parser with TextIOBase object.
        :param TextIOBase file: TextIOBase content
        :raises ValueError: If the file object cannot be read or seek.
        """
        self._custom_headers = custom_headers
        self._file = file
        self._reset_file()
        self._dialect = self._detect_dialect()
        self._reset_file()
        self._has_header = self._detect_header()
        self._reset_file()

    def _reset_file(self) -> None:
        try:
            self._file.seek(0)
        except (AttributeError, Exception):
            raise ValueError("Provided file object must support seek and read")

    def _detect_dialect(self) -> Type[Dialect]:
        """Sniff the CSV dialect (delimiter, quotechar, etc) from the first 1024 characters."""
        sample = self._file.read(1024)
        return csv.Sniffer().sniff(sample)

    def _detect_header(self) -> bool:
        """ Detect if the CSV has a header"""
        sample = self._file.read()
        return csv.Sniffer().has_header(sample)

    @property
    def delimiter(self) -> str:
        """Return the detected delimiter."""
        return self._dialect.delimiter

    @property
    def quotechar(self) -> str:
        """Return the detected quote character"""
        return self._dialect.quotechar

    def parse(self) -> list[dict[str, Any]]:
        """"
        Parse the CSV file and return a list of dictionaries, one per valid row.

        - If no header is present, it assigns a default one.
        - Skips rows that are completely empty or missing critical fields like 'surname' or 'age'.

        Returns:
            List[Dict[str, Any]]: A list of parsed and validated rows.
        """

        self._file.seek(0)

        fieldnames = None
        if not self._has_header and (fieldnames := self._custom_headers) is None:
            raise Exception('No headers detected or specified')

        reader = DictReader(
            self._file,
            fieldnames=fieldnames,
            restkey='extra_keys',
            skipinitialspace=True,
            delimiter=self.delimiter,
            quotechar=self.quotechar
        )

        rows = []
        for row in reader:
            if not any(row.values()):
                continue # skip blank lines

            name = (row.get('name') or '').strip() or "Unknown"
            surname = (row.get('surname') or '').strip() or "Unknown"
            age_s = row.get('age') or ''
            age = int(age_s) if age_s.isdigit() else None
            city = row.get('city') or "Unknown"
            country = row.get('country') or "Unknown"
            position = row.get('position') or "Unknown"

            if surname == "Unknown" or age is None:
                continue # enforce required fields

            rows.append({
                'name': name,
                'surname': surname,
                'age': age,
                'city': city,
                'country': country,
                'position': position
            })

        return rows
