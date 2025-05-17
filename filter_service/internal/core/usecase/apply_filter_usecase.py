import asyncio
import logging

from internal.core.entity.image_data import ImageData
from internal.repository.redis_repo import RedisRepo
from internal.repository.s3_repo import S3Repo
from utils.filters import _apply_filter
from utils.image_loader import download_image


async def apply_filter_usecase(
    image_id: str,
    filter: dict,
    redis_repo: RedisRepo,
    s3_repo: S3Repo
) -> str:
    image_url = await redis_repo.get_current_version_url(image_id)
    image_data = ImageData(image_id=image_id, image_url=image_url)

    image_path = await download_image(image_data.image_url)

    loop = asyncio.get_running_loop()
    filtered_path = await loop.run_in_executor(None, _apply_filter, image_path, filter)
    logging.debug(f"apply_filter_usecase - filtered_path: {filtered_path}")
    logging.info(f"apply_filter_usecase - filtered_path: {filtered_path}")
    filtered_url = await s3_repo.upload_filtered(image_id, filtered_path)

    # Контроль версий
    await redis_repo.push_new_version(image_id, filtered_url)
    logging.debug(f"apply_filter_usecase - filtered_url: {filtered_url}")
    logging.info(f"apply_filter_usecase - filtered_url: {filtered_url}")

    return filtered_url
