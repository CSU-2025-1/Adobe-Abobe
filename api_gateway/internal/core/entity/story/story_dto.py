from pydantic import BaseModel

class StoryRequest(BaseModel):
    user_id: str
    timestamp: str