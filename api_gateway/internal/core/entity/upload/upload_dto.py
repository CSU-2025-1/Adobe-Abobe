from pydantic import BaseModel


class UploadRequest(BaseModel):
    content: bytes
    filename: str
    content_type: str
    user_id: str
