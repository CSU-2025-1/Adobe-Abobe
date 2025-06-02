import numpy as np
import cv2
from utils.aiohttp_session import get_session


async def download_image_array(url: str) -> np.ndarray:
    session = await get_session()
    async with session.get(url) as resp:
        if resp.status != 200:
            raise ValueError(f"Failed to download image: {resp.status}")
        data = await resp.read()

    image_array = np.asarray(bytearray(data), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Failed to decode image")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image