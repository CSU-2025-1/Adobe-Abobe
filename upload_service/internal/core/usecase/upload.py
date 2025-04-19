from internal.core.entity.image import Image
from internal.repository import s3_repo, redis_repo
from utils.uuid import generate_uuid

def handle_upload(image: Image) -> str:
    image_id = f"{generate_uuid()}_{image.filename}"
    image_url = s3_repo.upload_to_s3(image_id, image.content, image.content_type)
    redis_repo.save_image_mapping(image.user_id, image_id, image_url)
    return image_id
