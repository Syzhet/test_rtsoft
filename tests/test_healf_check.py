import unittest
from typing import Generator, List

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.main import app
from core.loadcsv import ReadCsvFile
from db.base import async_session
from db.models.models import Group, Image


class TestHealthCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.CLIENT: TestClient = TestClient(app)

    def test_health_check(self) -> None:
        """Home Page Test."""

        response = self.CLIENT.get('/api/v1/health-check')
        assert response.status_code == 200
        assert response.text == 'Application: OK'


class TestLoadDataFromCSV(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        cls.initial_data: Generator[List[str], None, None] = (
            ReadCsvFile('data').return_data()
        )

    async def test_load_data(self):
        csv_image_count = 0
        csv_group = set()
        for row in self.initial_data:
            csv_group.update(row[2:])
            csv_image_count += 1
        csv_group_count = len(csv_group)
        async with async_session() as session:
            query_image = select(Image).with_only_columns(Image.id)
            result_image = await session.execute(query_image)
            db_images_count = len(list(result_image.scalars()))

            query_group = select(Group).with_only_columns(Group.id)
            result_group = await session.execute(query_group)
            db_groups_count = len(list(result_group.scalars()))
        self.assertEqual(
            csv_image_count,
            db_images_count
        )
        self.assertEqual(
            csv_group_count,
            db_groups_count
        )


if __name__ == '__main__':
    unittest.main()
