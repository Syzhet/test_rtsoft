import csv
from pathlib import Path, PosixPath
from typing import Dict, List, Optional


class ReadCsvFile:
    """
    Класс для чтения данных
    """
    def __init__(self, name_csv_file: str) -> None:
        self.name_csv_file: str = name_csv_file
        self.result_data: Optional[List[Dict[str, str]]] = []

    def _get_path_to_csv_file(self) -> PosixPath:
        current_file_path = Path(__file__).parent
        return Path(current_file_path, f'{self.name_csv_file}.csv')

    def _read_data_from_csv_file(self) -> None:
        with open(
            self._get_path_to_csv_file(),
            'r', encoding='UTF-8'
        ) as file:
            data = csv.DictReader(
                file,
                delimiter=';',
                skipinitialspace=True
            )
            for row in data:
                self.result_data.append(row)

    def return_data(self):
        self._read_data_from_csv_file()
        return self.result_data

    def __str__(self):
        return f'path to .csv file: {self.get_path_to_csv_file()}'
