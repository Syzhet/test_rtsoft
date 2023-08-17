import asyncio
import csv
from pathlib import Path, PosixPath
from typing import Dict, List, Optional, Generator

from db.base import async_session
from db.models.models import Group, Image


class ReadCsvFile:
    """
    Класс для чтения данных из csv файла.
    """

    def __init__(self, name_csv_file: str) -> None:
        self.name_csv_file: str = name_csv_file
        self.result_data: Optional[List[Dict[str, str]]] = []

    def _get_path_to_csv_file(self) -> PosixPath:
        """
        Функция определяет путь до csv файла данные из которого
        необходимо прочитать.

        Returns:
            PosixPath: путь до csv файла
        """

        current_file_path: PosixPath = Path(__file__).parent
        return Path(current_file_path, f'{self.name_csv_file}.csv')

    def _read_data_from_csv_file(self) -> Generator[List[str], None, None]:
        """
        Генератор возвращает данные построчно из csv файла.

        Yields:
            List: строка csv файла преобразованная в список
        """

        with open(
            self._get_path_to_csv_file(),
            'r', encoding='UTF-8'
        ) as file:
            data = csv.reader(
                file,
                delimiter=';',
                skipinitialspace=True
            )
            for row in data:
                yield row

    def return_data(self) -> Generator[List[str], None, None]:
        """
        Функция возвращает объект генератора с данными из csv файла.

        Returns:
            Generator[List[str], None, None]: объект генератора

        Yields:
            Generator[List[str], None, None]: объект генератора с данными
                                              из csv файла
        """

        self.result_data = self._read_data_from_csv_file()
        return self.result_data

    def __str__(self) -> str:
        return f'path to .csv file: {self.get_path_to_csv_file()}'


class LoadInitDataToDB:
    """
    Класс для вставки исходных значений в таблицы базы данных.
    """

    def __init__(self, data_source: ReadCsvFile, file_name: str) -> None:
        self.data_source = data_source
        self.file_name = file_name

    def _get_data(self) -> Generator[List[str], None, None]:
        return self.data_source(self.file_name).return_data()

    def _prepare_data(self) -> Generator[Dict[str, str], None, None]:
        """
        Генератор поочередно отдает словари с данными разделенными
        для создания объектов Image и Group.

        Yields:
            Generator[Dict[str, str], None, None]: словарь с данными
                                                   разделенными для
                                                   создания объектов
                                                   Image и Group
        """

        initial_data: List[List[str]] = self._get_data()
        for row in initial_data:
            row_dict: Dict[str, str] = {
                "Image": row[:2],
                "Groups": row[2:]
            }
            yield row_dict

    def _prepare_group(self) -> Dict[str, Group]:
        """
        Функция возвращает словарь где значениями являются
        объекты класса Group. Ключи в словаре имеют
        то же значение что и поле title объекта Group,
        отображающегося на данный ключ.

        Returns:
            Dict[str, Group]: словарь с объектами
                              Group в значениях
        """

        data = self._prepare_data()
        unique_groups: Dict[str, Group] = {}
        for data_obj in data:
            for group in data_obj['Groups']:
                if group in unique_groups:
                    continue
                unique_groups[group]: Group = Group(title=group)
        return unique_groups

    async def create_objs_in_db(self) -> None:
        """
        Функция создает записи в таблицах базы данных
        на основании объектов Image и Group.
        """

        groups_data: Dict[str, Group] = self._prepare_group()
        for data_obj in self._prepare_data():
            async with async_session() as session:
                new_image: Image = Image(
                    image_url=data_obj['Image'][0],
                    count=int(data_obj['Image'][1])
                )
                session.add(new_image)
                groups = [groups_data[group] for group in data_obj['Groups']]
                session.add_all(groups)
                new_image.groups.extend(groups)
                await session.commit()


async def main() -> None:
    """
    Точка входа для создания записей в базе данных
    на основании конфигурационного csv файла.
    """

    data_source_obj = LoadInitDataToDB(ReadCsvFile, 'data')
    await data_source_obj.create_objs_in_db()

if __name__ == '__main__':
    asyncio.run(main())
