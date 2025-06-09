import asyncio
import gc
import uuid
from datetime import datetime
from io import BytesIO
import cv2

from internal.repository.s3_repo import S3Repo
from internal.repository.redis_repo import RedisRepo
from utils.filters_registry import FILTER_REGISTRY
from utils.image_loader import download_image_array


async def apply_filter_usecase(
        user_id: str,
        image_url: str,
        filters: list[dict],
        task_id: str,
        s3_repo: S3Repo,
        redis_repo: RedisRepo
):
    image = await download_image_array(image_url)

    for f in filters:
        filter_type = f["type"]
        value = f["value"]
        if filter_type not in FILTER_REGISTRY:
            raise ValueError(f"Unsupported filter: {filter_type}")

        image = await asyncio.to_thread(FILTER_REGISTRY[filter_type], image, value)

    gc.collect()
    _, encoded_image = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    buffer = BytesIO(memoryview(encoded_image))

    final_filename = f"filtered_{uuid.uuid4().hex}.jpg"
    filtered_url = await s3_repo.upload_from_memory(buffer, "filtered", final_filename)

    timestamp = datetime.utcnow().isoformat()

    await asyncio.gather(
        redis_repo.save_filter_history(user_id, filtered_url, filters, timestamp),
        redis_repo.save_filter_result(task_id, filtered_url, timestamp)
    )
