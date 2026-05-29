from fastapi import FastAPI, UploadFile, File, status, Response
from fastapi.responses import FileResponse
from PIL import Image, UnidentifiedImageError
from typing import Annotated

app = FastAPI()


@app.get("/")
async def main(response: Response):
    response.status_code = status.HTTP_200_OK
    return FileResponse("index.html")


@app.get("/login")
async def login(response: Response):
    response.status_code = status.HTTP_200_OK
    return {"author": "1155281"}


@app.post("/size2json")
async def size2json(image: Annotated[UploadFile, File()], response: Response):
    try:
        img = Image.open(image.file)

        width, height = img.size
        response.status_code = status.HTTP_200_OK
        return {"width": width, "height": height}

    except UnidentifiedImageError:
        response.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        return {"result": "invalid filetype"}