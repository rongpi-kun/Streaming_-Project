from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi import Request, Response
from fastapi import Header
from . import models, schemas
from . database import get_db
from fastapi import APIRouter
import os
import io
from fastapi.responses import StreamingResponse
# from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/video',
    tags=['video']
)
# templates = Jinja2Templates(directory="templates")
CHUNK_SIZE = 1024*1024
video_path = Path("video.mp4")


# @app.get("/")
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.htm", context={"request": request})

@router.get('/')
async def show_all_videos(db = Depends(get_db)):
    video = db.query(models.VideoModel).all()
    return video

@router.post('/insert')
async def insert(request: schemas.VideoData, db = Depends(get_db)):
    video = models.VideoModel(name = request.name, file_path = request.file_path)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

@router.get("/{id}")
def stream_video(id: int, db = Depends(get_db)):
    video = db.query(models.VideoModel).filter(models.VideoModel.id == id).first()
    video_path = video.file_path
    # Replace with your video file path
    # video_file_path = "path/to/video.mp4"

    def generate():
        with open(video_path, "rb") as video_file:
            while True:
                chunk = video_file.read(1024*1024)
                if not chunk:
                    break
                yield chunk

    headers = {
            "Content-Type": "video/mp4"
        }

    return StreamingResponse(generate(), media_type="video/mp4", headers=headers)

# async def stream_video(id: int, db = Depends(get_db)):
#     # replace with your own logic for getting the video file
#     # you can read the video file from disk or from a database, for example
#     video = db.query(models.VideoModel).filter(models.VideoModel.id == id).first()
#     video_path = video.file_path
#     # video_file = open(video_path, mode='rb')

#     # use io.BytesIO to create a stream of the video file
#     # video_stream = io.BytesIO(video_file.read())

#     # create a StreamingResponse to send the video stream as a response
#     response = StreamingResponse(open(video_path, mode="rb"), media_type="video/mp4")
#     response.headers["Content-Disposition"] = f"attachment; filename={video_path}"

#     return response

# @router.get("/{id}")
# async def video_endpoint(id: int, range: str = Header(None), db = Depends(get_db)):
#     video = db.query(models.VideoModel).filter(models.VideoModel.id == id).first()
#     video_path = video.file_path
#     print('current: ', video_path)
#     print('range: ', range)
#     start, end = range.replace("bytes=", "").split("-")
#     start = int(start)
#     end = int(end) if end else start + CHUNK_SIZE
#     with open(video_path, "rb") as video:
#         video.seek(start)
#         data = video.read(end - start)
#         # filesize = str(video_path.stat().st_size)
#         filesize = os.stat(video_path).st_size
#         headers = {
#             'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#             'Accept-Ranges': 'bytes'
#         }
#         return Response(data, status_code=206, headers=headers, media_type="video/mp4")