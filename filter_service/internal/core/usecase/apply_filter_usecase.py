from internal.core.entity.image_data import ImageData
from internal.repository.redis_repo import RedisRepo
from internal.repository.s3_repo import S3Repo
from utils.filters import apply_filters
from utils.image_loader import download_image


async def apply_filter_usecase(
        image_id: str,
        filters: dict,
        redis_repo: RedisRepo,
        s3_repo: S3Repo
) -> str:
    image_url = await redis_repo.get_image_url(image_id)
    image_data = ImageData(image_id=image_id, image_url=image_url)

    image_path = await download_image(image_data.image_url)

    filtered_path = apply_filters(image_path, filters)

    filtered_url = await s3_repo.upload_filtered(image_id, filtered_path)

    return filtered_url
