from pydantic import BaseModel


class FilterConfig(BaseModel):
    type: str
    value: float


class FilterRequest(BaseModel):
    image_id: str
    filter: FilterConfig
