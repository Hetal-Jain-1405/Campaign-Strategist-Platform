from pydantic import BaseModel, Field
from typing import Literal


class VisualAsset(BaseModel):
    asset_type: Literal[
        "moodboard",
        "social_media_creative",
        "blog_image",
        "ad_creative"
    ]
    platform: str
    aspect_ratio: str
    visual_description: str
    image_prompt: str
    source_content_reference: str | None = None
    image_path: str | None = None


class VisualAssets(BaseModel):
    assets: list[VisualAsset]