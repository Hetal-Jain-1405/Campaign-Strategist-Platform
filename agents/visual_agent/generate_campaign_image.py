
import os
import uuid
import requests

from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

WORKER_URL = os.environ["CLOUDFLARE_WORKER_URL"]
WORKER_API_KEY = os.environ["CLOUDFLARE_WORKER_API_KEY"]

OUTPUT_DIR = Path("media/campaigns")


@tool
def generate_campaign_image(prompt: str) -> str:
    """Generate a campaign image from a text prompt using
    the Cloudflare Worker API. Save the image locally and
    return the path to the generated image."""

    print(f'tool is called with prompt')

    response = requests.post(
        WORKER_URL,
        headers={
            "Authorization": f"Bearer {WORKER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"prompt": prompt},
        timeout=180,
    )

    response.raise_for_status()

    # Save the generated image bytes.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.png"
    output_path = OUTPUT_DIR / filename

    output_path.write_bytes(response.content)

    print(f'Image generated and saved')

    return str(output_path)
