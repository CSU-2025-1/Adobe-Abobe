from typing import List
from pydantic import BaseModel


class FilterConfig(BaseModel):
    type: str
    value: float


class FilterRequest(BaseModel):
    user_id: int
    image_url: str
    filters: List[FilterConfig]
