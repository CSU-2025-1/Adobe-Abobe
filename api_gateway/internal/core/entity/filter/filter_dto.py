from pydantic import BaseModel


class FilterRequest(BaseModel):
    image_id: str
    filters: dict[str, float]
