from sqlalchemy import Column, Integer, String, DateTime, Float
from . database import Base
import datetime

class VideoModel(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_published = Column(DateTime, default=datetime.datetime.now())
    size = Column(Float)
    file_path = Column(String)
