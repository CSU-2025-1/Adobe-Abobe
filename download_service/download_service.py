from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from minio_data_store.minio_client import client, bucket_name
from minio.error import S3Error

app = FastAPI()

@app.get("/download/last")
def download_last_uploaded_image():
    try:
        objects = list(client.list_objects(bucket_name, recursive=True))

        if not objects:
            raise HTTPException(status_code=404, detail="No files in bucket")

        last_uploaded = max(objects, key=lambda obj: obj.last_modified)

        response = client.get_object(bucket_name, last_uploaded.object_name)

        return StreamingResponse(response, media_type="image/jpeg")

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
