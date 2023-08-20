from typing import List, Optional, Union

from fastapi import Query
from pydantic import BaseModel, Field, validator


class QueryParametr(BaseModel):
    """Класс для обработки параметров запроса."""

    category: Optional[List[str]] = Field(
        Query([], alias="category[]")
    )

    @validator('category')
    def check_query_category(cls, value) -> Union[List[str], Exception]:
        """Проверка количества передаваемых категорий."""

        if len(value) <= 10:
            return value
        raise ValueError(
            'Нельзя передавать больше 10 категорий в запросе'
        )
