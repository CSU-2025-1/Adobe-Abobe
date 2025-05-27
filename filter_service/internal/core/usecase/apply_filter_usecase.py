import asyncio
import gc
import os
import time
import uuid
import logging
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
        s3_repo: S3Repo,
        redis_repo: RedisRepo
) -> tuple[str, str]:
    original_file = None
    final_path = None

    try:
        start = time.perf_counter()
        image = await download_image_array(image_url)
        logging.info(f"[timing] download took {time.perf_counter() - start:.2f}s")

        start1 = time.perf_counter()
        for f in filters:
            filter_type = f["type"]
            value = f["value"]
            if filter_type not in FILTER_REGISTRY:
                raise ValueError(f"Unsupported filter: {filter_type}")

            image = await asyncio.to_thread(FILTER_REGISTRY[filter_type], image, value)
        logging.info(f"[timing] for f in filters: {time.perf_counter() - start1:.2f}s")

        gc.collect()
        start2 = time.perf_counter()
        _, encoded_image = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        buffer = BytesIO(memoryview(encoded_image))
        logging.info(f"[timing] BytesIO: {time.perf_counter() - start2:.2f}s")
        start3 = time.perf_counter()
        final_filename = f"filtered_{uuid.uuid4().hex}.jpg"
        filtered_url = await s3_repo.upload_from_memory(buffer, "filtered", final_filename)
        logging.info(f"[timing] s3_repo.upload_from_memor: {time.perf_counter() - start3:.2f}s")

        timestamp = datetime.utcnow().isoformat()

        start4 = time.perf_counter()
        await redis_repo.save_filter_history(user_id, filtered_url, filters, timestamp)
        logging.info(f"[timing] redis_repo.save_filter_history: {time.perf_counter() - start4:.2f}s")

        return filtered_url, timestamp

    finally:
        try:
            if original_file and os.path.exists(original_file):
                os.remove(original_file)
            if final_path and os.path.exists(final_path):
                os.remove(final_path)
        except Exception as e:
            logging.warning(f"[cleanup] Failed to remove temp files: {e}")
        gc.collect()
