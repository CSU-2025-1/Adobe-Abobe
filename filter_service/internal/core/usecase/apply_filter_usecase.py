import gc
import os
import uuid
import logging
from datetime import datetime
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

from internal.repository.s3_repo import S3Repo
from internal.repository.redis_repo import RedisRepo
from utils.filters_registry import FILTER_REGISTRY
from utils.image_loader import download_image


async def apply_filter_usecase(
        user_id: str,
        image_url: str,
        filters: list[dict],
        s3_repo: S3Repo
) -> tuple[str, str]:
    image_path = await download_image(image_url)
    original_file = image_path
    final_path = None

    try:
        image = Image.open(image_path).convert("RGB")
        image = np.array(image)

        for f in filters:
            filter_type = f["type"]
            value = f["value"]
            logging.info(f"[apply] {filter_type}={value}")
            if filter_type not in FILTER_REGISTRY:
                raise ValueError(f"Unsupported filter: {filter_type}")
            image = FILTER_REGISTRY[filter_type](image, value)

        gc.collect()
        _, encoded_image = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        buffer = BytesIO(encoded_image.tobytes())
        buffer.seek(0)

        final_filename = f"filtered_{uuid.uuid4().hex}.jpg"
        filtered_url = await s3_repo.upload_from_memory(buffer, "filtered", final_filename)

        timestamp = datetime.utcnow().isoformat()
        redis_repo = RedisRepo()
        await redis_repo.save_filter_history(user_id, filtered_url, filters, timestamp)

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
