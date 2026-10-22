from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


CampaignStatus = Literal["draft", "queued", "running", "completed", "failed"]


class CampaignCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    brief: str = Field(min_length=1)
    brand_context: str | None = None
    market_context: str | None = None


class CampaignUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    brief: str | None = Field(default=None, min_length=1)
    brand_context: str | None = None
    market_context: str | None = None


class Campaign(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: UUID
    owner_id: UUID
    name: str
    brief: str
    brand_context: str | None = None
    market_context: str | None = None
    status: CampaignStatus
    failure_details: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime


RunStatus = Literal["queued", "running", "completed", "failed"]


class CampaignRun(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: UUID
    campaign_id: UUID
    status: RunStatus
    current_agent: str | None = None
    completed_agents: list[str] = Field(default_factory=list)
    progress: int = Field(ge=0, le=100)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_details: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime


class CampaignOutput(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: UUID
    run_id: UUID
    output_type: Literal["research", "strategy", "content", "visuals", "media_plan"]
    payload: Any
    created_at: datetime
    updated_at: datetime
