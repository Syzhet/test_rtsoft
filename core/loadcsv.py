import asyncio
import csv
import logging
import sys
from pathlib import Path, PosixPath
from typing import Dict, Generator, List, Optional

from sqlalchemy.exc import SQLAlchemyError

from db.base import async_session
from db.models.models import Category, Image

logger = logging.getLogger('loadcsv.py')
logger.setLevel(logging.ERROR)

stdout_handler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(
    u'%(filename)s:%(lineno)d: '
    u'#%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
)
stdout_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)


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
        return Path(
            current_file_path.parent,
            'core',
            f'{self.name_csv_file}.csv'
        )

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
        для создания объектов Image и Category.

        Yields:
            Generator[Dict[str, str], None, None]: словарь с данными
                                                   разделенными для
                                                   создания объектов
                                                   Image и Category
        """

        initial_data: List[List[str]] = self._get_data()
        for row in initial_data:
            row_dict: Dict[str, str] = {
                "Image": row[:2],
                "Categories": row[2:]
            }
            yield row_dict

    def _prepare_category(self) -> Dict[str, Category]:
        """
        Функция возвращает словарь где значениями являются
        объекты класса Category. Ключи в словаре имеют
        то же значение что и поле title объекта Category,
        отображающегося на данный ключ.

        Returns:
            Dict[str, Category]: словарь с объектами
                                 Category в значениях
        """

        data = self._prepare_data()
        unique_categories: Dict[str, Category] = {}
        for data_obj in data:
            for category in data_obj['Categories']:
                if category in unique_categories:
                    continue
                unique_categories[category]: Category = Category(
                    title=category
                )
        return unique_categories

    async def create_objs_in_db(self) -> None:
        """
        Функция создает записи в таблицах базы данных
        на основании объектов Image и Category.
        """

        categories_data: Dict[str, Category] = self._prepare_category()
        for data_obj in self._prepare_data():
            try:
                async with async_session() as session:
                    new_image: Image = Image(
                        image_url=data_obj['Image'][0],
                        count=int(data_obj['Image'][1])
                    )
                    session.add(new_image)
                    categories = [
                        categories_data[category] for category
                        in data_obj['Categories']
                    ]
                    session.add_all(categories)
                    new_image.categories.extend(categories)
                    await session.commit()
            except SQLAlchemyError as e:
                logger.error(e)
                await session.rollback()


async def main() -> None:
    """
    Точка входа для создания записей в базе данных
    на основании конфигурационного csv файла.
    """

    data_source_obj = LoadInitDataToDB(ReadCsvFile, 'data')
    await data_source_obj.create_objs_in_db()

if __name__ == '__main__':
    asyncio.run(main())
