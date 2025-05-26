import os
import uuid
import asyncio
import logging
from datetime import datetime

from internal.repository.s3_repo import S3Repo
from utils.filters import _apply_filter
from utils.image_loader import download_image
from internal.repository.redis_repo import RedisRepo
from utils import filters


async def apply_filter_usecase(
    user_id: str,
    image_url: str,
    filters: list[dict],
    s3_repo: S3Repo
) -> tuple[str, str]:
    image_path = await download_image(image_url)
    current_path = image_path

    for f in filters:
        loop = asyncio.get_running_loop()
        current_path = await loop.run_in_executor(None, _apply_filter, current_path, f)

    output_path = os.path.splitext(current_path)[0] + f"_final_{uuid.uuid4().hex}.jpg"
    os.rename(current_path, output_path)

    filtered_url = await s3_repo.upload_filtered("filtered", output_path)

    timestamp = datetime.utcnow().isoformat()
    redis_repo = RedisRepo()
    await redis_repo.save_filter_history(user_id, filtered_url, filters, timestamp)

    logging.info(f"[filter-usecase] uploaded to: {filtered_url}")
    return filtered_url, timestamp
