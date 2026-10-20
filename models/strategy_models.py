
from pydantic import BaseModel, Field
from typing import Optional


class CampaignGoal(BaseModel):
    goal: str = Field(description="A measurable or qualitative campaign goal")
    kpi: list[str] = Field(
        description="Metrics used to evaluate this goal"
    )
    target_value: Optional[str] = Field(
        default=None,
        description="Target value, only when supported by available information"
    )


class CampaignStrategy(BaseModel):
    campaign_objective: str = Field(
        description="The primary objective of the campaign"
    )

    secondary_objectives: list[str] = Field(
        description="Additional objectives, if relevant"
    )

    primary_audience: str = Field(
        description="The main audience, including relevant needs and motivations"
    )

    secondary_audience: Optional[str] = Field(
        default=None,
        description="An additional audience, if justified"
    )

    brand_positioning: str = Field(
        description="How the brand should be perceived by its target audience"
    )

    unique_selling_proposition: str = Field(
        description="The brand's differentiating value proposition, when supported"
    )

    campaign_concept: str = Field(
        description="The central idea guiding the campaign"
    )

    key_message: str = Field(
        description="The main message the audience should remember"
    )

    messaging_pillars: list[str] = Field(
        description="Supporting themes that reinforce the key message"
    )

    brand_voice: list[str] = Field(
        description="Recommended brand voice and communication tone"
    )

    primary_cta: str = Field(
        description="The main action the audience should take"
    )

    secondary_ctas: list[str] = Field(
        description="Additional calls to action, if relevant"
    )

    campaign_goals: list[CampaignGoal] = Field(
        description="Campaign goals and relevant performance indicators"
    )

    strategic_rationale: str = Field(
        description="Why the proposed strategy fits the brief and research"
    )

    evidence_and_assumptions: list[str] = Field(
        description="Research-supported insights and clearly identified strategic assumptions"
    )

    risks_and_constraints: list[str] = Field(
        description="Relevant risks, uncertainties, and business constraints"
    )

    information_gaps: list[str] = Field(
        description="Missing information that could affect the strategy"
    )
