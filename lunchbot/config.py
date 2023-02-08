import os

IMAGE_FOLDER = os.getenv("IMAGE_FOLDER")
assert IMAGE_FOLDER and os.path.isdir(IMAGE_FOLDER)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PUBLIC_URL = os.getenv("PUBLIC_URL")
RUN_SECRET = os.getenv("PUBLIC_URL", "amazingsecret")
