from api import video, models
from api.database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

origins = [
    'http://127.0.0.1:5500',
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials=True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

app.include_router(video.router)