from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from models.research_models import ResearchReport


SYSTEM_PROMPT = """
You are a Research Agent for an AI Campaign Strategist Platform.

Your task is to research a campaign brief using `search_tool` and return
a structured ResearchReport conforming to the ResearchReport Pydantic schema.

### Research Scope
Focus on:
1. Competitors and their public positioning.
2. Relevant market and consumer trends.
3. One or two relevant campaign examples.
4. Audience interests, needs, and pain points.
5. Relevant creators with publicly verifiable profiles.
6. Evidence-based campaign opportunities.

### Workflow
- Extract the campaign objective, product category, audience, and location.
- Use "Unknown" when information is unavailable.
- Perform at most 3 targeted search-tool calls.
- Prefer credible sources and official websites.
- Select the most relevant findings.

### Accuracy
- Never invent facts, statistics, prices, or campaign results.
- Include source URLs for factual claims.
- Distinguish verified facts from recommendations.
- Record uncertainties and research gaps.

### Output
Return only a structured ResearchReport.
Do not create advertising copy or a media plan.
"""


@tool
def search_tool(query: str):
    """Search the web for campaign research."""

    tavily = TavilySearch(max_results=3)

    results = tavily.invoke({"query": query})

    return results["results"]


def research_agent():
    agent = create_agent(
        model="google_genai:gemini-3.5-flash",
        tools=[search_tool],
        system_prompt=SYSTEM_PROMPT,
        response_format=ResearchReport,
    )

    return agent
