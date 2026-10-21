
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


# 1. Competitor Analysis
class Competitor(BaseModel):
    competitor_name: str
    website_url: HttpUrl | None = None
    product_or_service: str
    positioning: str
    pricing: str | None = None
    public_product_claims: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses_or_gaps: list[str] = Field(default_factory=list)
    source_urls: list[HttpUrl] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]


# 2. Market Trends
class MarketTrend(BaseModel):
    trend: str
    description: str
    relevance_to_campaign: str
    evidence: str
    source_urls: list[HttpUrl] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]


# 3. Campaign Research
class CampaignExample(BaseModel):
    campaign_name: str
    brand_name: str
    campaign_objective: str | None = None
    target_audience: str | None = None
    campaign_approach: list[str] = Field(default_factory=list)
    observed_outcomes: list[str] = Field(default_factory=list)
    lessons_for_campaign: list[str] = Field(default_factory=list)
    source_urls: list[HttpUrl] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]


# 4. Influencer / Creator Research
# class CreatorMetrics(BaseModel):
#     followers: int | None = None
#     engagement_rate: float | None = None
#     verification_date: str | None = None
#     source_url: HttpUrl | None = None


# class Influencer(BaseModel):
#     creator_name: str
#     platform: str
#     profile_url: HttpUrl | None = None
#     content_niche: str
#     audience_relevance: str
#     publicly_verified_metrics: CreatorMetrics = Field(
#         default_factory=CreatorMetrics
#     )
#     confidence: Literal["high", "medium", "low"]


# 5. Audience Insights
class AudienceInsight(BaseModel):
    insight_type: Literal[
        "interest",
        "pain_point",
        "need",
        "behavior",
        "opportunity",
    ]
    description: str
    supporting_evidence: str
    source_urls: list[HttpUrl] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]


# 6. Campaign Opportunities
class CampaignOpportunity(BaseModel):
    opportunity: str
    rationale: str
    supporting_evidence: list[str] = Field(default_factory=list)
    recommended_direction: str
    limitations: list[str] = Field(default_factory=list)


# 7. Research Gaps
class ResearchGap(BaseModel):
    topic: str
    reason: str
    additional_data_needed: str


# 8. Source Registry
class ResearchSource(BaseModel):
    source_id: str
    title: str
    url: HttpUrl
    publisher: str | None = None
    publication_date: str | None = None
    access_date: str
    source_type: Literal[
        "official_website",
        "industry_report",
        "news",
        "social_profile",
        "research_paper",
        "other",
    ]
    supports_claims: list[str] = Field(default_factory=list)


# 9. Research Metadata
class ResearchMetadata(BaseModel):
    research_scope: str
    geographic_location: str
    product_category: str
    research_date: str
    limitations: list[str] = Field(default_factory=list)
    overall_confidence: Literal["high", "medium", "low"]


# 10. Final Research Report
class ResearchReport(BaseModel):
    research_summary: str
    competitor_analysis: list[Competitor] = Field(default_factory=list)
    market_trends: list[MarketTrend] = Field(default_factory=list)
    campaign_research: list[CampaignExample] = Field(default_factory=list)
    # influencer_research: list[Influencer] = Field(default_factory=list)
    audience_insights: list[AudienceInsight] = Field(default_factory=list)
    campaign_opportunities: list[CampaignOpportunity] = Field(
        default_factory=list
    )
    research_gaps: list[ResearchGap] = Field(default_factory=list)
    sources: list[ResearchSource] = Field(default_factory=list)
    metadata: ResearchMetadata
