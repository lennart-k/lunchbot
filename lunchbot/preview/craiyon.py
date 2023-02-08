import os
from hashlib import sha256
from base64 import b64decode
import asyncio
import aiohttp
from mensautils.parser.canteen_result import Serving
from lunchbot.config import PUBLIC_URL
import logging
from PIL import Image
from io import BytesIO

LOGGER = logging.getLogger(__name__)


def webp_to_file(webp: bytes, path: str):
    img = Image.open(BytesIO(webp), formats=("WEBP",))
    img.save(path)


async def generate_preview_images(title: str) -> list[bytes]:
    LOGGER.info(f"Requesting a preview for '{title}'")
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "https://backend.craiyon.com/generate", json={"prompt": title}
        )
        if response.status != 200:
            return []
        data = await response.json()

    LOGGER.info(f"Generated a preview for '{title}'")
    return [b64decode(image) for image in data["images"]]


def publish_images(prefix: str, folder: str, images: list[bytes]) -> list[str]:
    filenames = []
    for i, image in enumerate(images):
        name = f"{prefix}_{i}.png"
        path = os.path.join(folder, name)
        webp_to_file(image, path)
        filenames.append(name)
    return filenames


async def get_preview_image_path(title: str, folder: str) -> str:
    titlehash = sha256(title.encode(), usedforsecurity=False).hexdigest()[:20]
    filename = f"{titlehash}_0.png"
    path = os.path.join(folder, filename)
    if not os.path.isfile(path):
        images = await generate_preview_images(title)
        publish_images(titlehash, folder, images)

    return filename


async def create_menu_images(menu: list[Serving], folder: str) -> list[str]:
    image_paths = await asyncio.gather(
        *(get_preview_image_path(item.title, folder) for item in menu)
    )
    return [f"{PUBLIC_URL}/{image_path}" for image_path in image_paths]
