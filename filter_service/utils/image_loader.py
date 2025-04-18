import aiohttp
import uuid
import os

TEMP_DIR = "/tmp" if os.name != "nt" else os.getenv("TEMP", ".")


async def download_image(url: str) -> str:
    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(TEMP_DIR, filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise ValueError(f"Failed to download image: {resp.status}")
            with open(file_path, "wb") as f:
                f.write(await resp.read())

    return file_path
