from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from minio_client import client, bucket_name
import uuid
import io

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть картинкой")

    file_id = f"{uuid.uuid4()}_{file.filename}"

    try:
        file_content = await file.read()

        file_stream = io.BytesIO(file_content)

        client.put_object(
            bucket_name,
            file_id,
            file_stream,
            length=len(file_content),
            content_type=file.content_type
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
