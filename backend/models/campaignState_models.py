from typing_extensions import TypedDict, Any

class CampaignState(TypedDict, total=False):
    user_query: str

    research_report: Any
    campaign_strategy: Any
    content_assets: Any
    visual_assets: Any
    media_plan: Any

    errors: list[str]