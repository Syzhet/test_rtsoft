import unittest
from typing import Generator, List

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.main import app
from core.loadcsv import ReadCsvFile
from db.base import async_session
from db.models.models import Category, Image


class TestHealthCheck(unittest.TestCase):
    """
    Класс для тестирования эндпоинта приложения FastAPI.
    """

    @classmethod
    def setUpClass(cls):
        cls.CLIENT: TestClient = TestClient(app)

    def test_health_check(self) -> None:
        """
        Тест эндпоинтма /api/v1/health-check.
        """

        response = self.CLIENT.get('/api/v1/health-check')
        assert response.status_code == 200
        assert response.text == 'Application: OK'


class TestLoadDataFromCSV(unittest.IsolatedAsyncioTestCase):
    """
    Класс для тестирования инициализации БД PostgreSQL.
    """

    @classmethod
    def setUpClass(cls):
        cls.initial_data: Generator[List[str], None, None] = (
            ReadCsvFile('data').return_data()
        )

    async def test_load_data(self):
        """
        Тестирование данных в БД PostgreSQL
        после запуска проекта.
        """

        csv_image_count = 0
        csv_category = set()
        for row in self.initial_data:
            csv_category.update(row[2:])
            csv_image_count += 1
        csv_category_count = len(csv_category)
        async with async_session() as session:
            query_image = select(Image).with_only_columns(Image.id)
            result_image = await session.execute(query_image)
            db_images_count = len(list(result_image.scalars()))

            query_category = select(Category).with_only_columns(Category.id)
            result_category = await session.execute(query_category)
            db_categories_count = len(list(result_category.scalars()))
        self.assertEqual(
            csv_image_count,
            db_images_count
        )
        self.assertEqual(
            csv_category_count,
            db_categories_count
        )


if __name__ == '__main__':
    unittest.main()
