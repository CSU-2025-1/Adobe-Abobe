from dataclasses import dataclass

@dataclass
class Image:
    image_id: str
    filename: str
    content_type: str
    content: bytes
    user_id: str
