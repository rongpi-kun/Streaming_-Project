from pydantic import BaseModel

class VideoData(BaseModel):
    name: str
    file_path: str