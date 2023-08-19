from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, Field


class QueryParametr(BaseModel):
    """Класс для обработки параметров запроса."""

    category: Optional[List[str]] = Field(
        Query([], alias="category[]")
    )
