from pydantic import BaseModel, Field
from typing import Literal


class SocialMediaPost(BaseModel):
    platform: str = Field(
        description="Social media platform for the post"
    )
    hook: str = Field(
        description="Attention-grabbing opening line"
    )
    caption: str = Field(
        description="Complete written social media post caption"
    )
    call_to_action: str = Field(
        description="Action the audience should take"
    )
    hashtags: list[str] = Field(
        description="Relevant hashtags for the post"
    )


class BlogArticle(BaseModel):
    title: str = Field(
        description="Title of the blog article"
    )
    introduction: str = Field(
        description="Opening that introduces the topic"
    )
    sections: list[str] = Field(
        description="Blog sections with headings and body content"
    )
    conclusion: str = Field(
        description="Closing summary of the article"
    )
    call_to_action: str = Field(
        description="Relevant action for the reader"
    )


class ContentAsset(BaseModel):
    content_type: Literal[
        "social_media_post",
        "blog"
    ] = Field(
        description="Type of written content"
    )
    social_media_post: SocialMediaPost | None = None
    blog: BlogArticle | None = None


class ContentAssets(BaseModel):
    assets: list[ContentAsset] = Field(
        description="All requested social media posts and blog articles"
    )