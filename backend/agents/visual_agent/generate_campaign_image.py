
import os
import uuid
import requests

from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

WORKER_URL = os.getenv("CLOUDFLARE_WORKER_URL", "")
WORKER_API_KEY = os.getenv("CLOUDFLARE_WORKER_API_KEY", "")

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "media" / "campaigns"
FIXTURE_IMAGES = sorted(OUTPUT_DIR.glob("*.png"))


@tool
def generate_campaign_image(prompt: str) -> str:
    """Generate a campaign image from a text prompt using
    the Cloudflare Worker API. Save the image locally and
    return the path to the generated image."""

    mode = os.getenv("VISUAL_MODE", "fixture").strip().lower()
    if mode == "fixture":
        if not FIXTURE_IMAGES:
            raise RuntimeError("VISUAL_MODE=fixture requires images in backend/media/campaigns")
        fixture = FIXTURE_IMAGES[len(prompt) % len(FIXTURE_IMAGES)]
        return f"/media/campaigns/{fixture.name}"
    if mode != "cloudflare":
        raise ValueError("VISUAL_MODE must be 'fixture' or 'cloudflare'")
    if not WORKER_URL or not WORKER_API_KEY:
        raise RuntimeError(
            "VISUAL_MODE=cloudflare requires CLOUDFLARE_WORKER_URL and "
            "CLOUDFLARE_WORKER_API_KEY"
        )

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

    return f"/media/campaigns/{filename}"
