import asyncio
import logging
import uvicorn

from fastapi import FastAPI
from api.router import router
from internal.broker.rabbitclient.workers import wrap_consumer
from internal.broker.rabbitclient.workers import validate_token, get_token, get_uploaded_image_id, \
    get_filtered_image

app = FastAPI()

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.on_event("startup")
async def startup_event():
    tasks = [
        asyncio.create_task(wrap_consumer(validate_token, "validate_token")),
        asyncio.create_task(wrap_consumer(get_token, "get_token")),
        asyncio.create_task(wrap_consumer(get_uploaded_image_id, "get_uploaded_image_id")),
        asyncio.create_task(wrap_consumer(get_filtered_image, "get_filtered_image")),
    ]
    logging.info("[gateway] Auth worker started as background task")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
