from pydantic import BaseModel, Field


class MediaActivity(BaseModel):
    activity: str = Field(
        description="Planned marketing activity"
    )
    content_reference: str | None = Field(
        default=None,
        description="Reference to an existing content asset"
    )
    visual_reference: str | None = Field(
        default=None,
        description="Path or reference to an existing visual asset"
    )
    platform: str = Field(
        description="Marketing platform for the activity"
    )
    format: str = Field(
        description="Format such as post, reel, story, or blog"
    )
    scheduled_date: str | None = Field(
        default=None,
        description="Planned publication date in YYYY-MM-DD format"
    )
    objective: str = Field(
        description="Purpose of the activity"
    )


class CampaignPhase(BaseModel):
    phase: str = Field(
        description="Campaign phase, such as awareness or conversion"
    )
    duration: str = Field(
        description="Duration of the phase"
    )
    activities: list[MediaActivity] = Field(
        description="Activities planned for this phase"
    )


class ChannelAllocation(BaseModel):
    channel: str = Field(
        description="Recommended marketing channel"
    )
    purpose: str = Field(
        description="Reason for selecting this channel"
    )
    proposed_budget: float | None = Field(
        default=None,
        description="Proposed budget allocation, if known"
    )
    currency: str = Field(
        default="INR",
        description="Currency of the proposed budget"
    )


class MediaPlan(BaseModel):
    campaign_duration: str = Field(
        description="Overall campaign duration"
    )
    recommended_channels: list[str] = Field(
        description="Recommended marketing channels"
    )
    channel_allocations: list[ChannelAllocation] = Field(
        description="Proposed budget allocation by channel"
    )
    campaign_phases: list[CampaignPhase] = Field(
        description="Campaign phases and their planned activities"
    )
    posting_schedule: list[MediaActivity] = Field(
        description="Chronological schedule of marketing activities"
    )
    testing_recommendations: list[str] = Field(
        description="Recommended experiments or content tests"
    )
    performance_metrics: list[str] = Field(
        description="KPIs for evaluating campaign performance"
    )
    assumptions: list[str] = Field(
        description="Assumptions and missing information"
    )