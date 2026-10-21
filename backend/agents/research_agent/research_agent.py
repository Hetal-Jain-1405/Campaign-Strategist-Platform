from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from models.research_models import ResearchReport
# import os
# from dotenv import load_dotenv

# load_dotenv()

SYSTEM_PROMPT = """
You are a Research Agent for an AI Campaign Strategist Platform.

Your task is to research a campaign brief using `search_tool` and return
a structured ResearchReport conforming to the ResearchReport Pydantic schema.

### Research Scope
Focus on these areas:
1. Competitors and their public positioning.
2. Relevant market and consumer trends.
3. One or two relevant campaign examples.
4. Audience interests, needs, and pain points.
5. Relevant creators with publicly verifiable profiles.
6. Evidence-based campaign opportunities.

### Workflow
- Extract the campaign objective, product category, audience, and location
  from the brief. Use "Unknown" when unavailable.
- Perform at most 3 targeted search-tool calls, combining related research
  questions where the tool supports it.
- Prefer credible, relevant sources and official websites.
- Use available search-result evidence; retrieve additional pages only when
  essential to verify an important claim.
- Select only the most relevant findings instead of producing exhaustive lists.

### Accuracy
- Never invent facts, statistics, prices, campaign results, or creator metrics.
- Include source URLs for factual claims.
- Distinguish verified facts from interpretations and recommendations.
- Use null for unavailable optional values and empty lists when no reliable
  findings are available.
- Use only the schema's permitted confidence and classification values.
- Record important uncertainties and research gaps.

### Output
Return a ResearchReport with all required top-level fields:
research_summary, competitor_analysis, market_trends, campaign_research,
influencer_research, audience_insights, campaign_opportunities,
research_gaps, sources, and metadata.

Ensure the output conforms to the Pydantic schema.
Do not return raw search results as the final answer.
Do not create the final campaign, advertising copy, or media plan.

Return only the structured research report.
"""



def search_tool(query: str):
    """Search the web for information relevant to the research query."""

    print('search tool is called')

    tavily = TavilySearch(max_results=3)
    results = tavily.invoke(
        {
            'query': query,
        }
    )
    print('search is done')
    return results['results']

def research_agent():

    agent = create_agent(
        model = 'google_genai:gemini-3.8-flash',
        tools = [search_tool, ],
        system_prompt = SYSTEM_PROMPT,
        response_format = ResearchReport,
    )

    print(f'Initialising the agent.....')

    result = agent.invoke(
        {
            'messages' : [
                {
                    'role': 'user',
                    'content' : 'For Environment Day, I want to create a campaign for my coffee shop that attracts Gen Z college students while raising awareness about environmentally sustainable coffee and eco-friendly practices.'
                }
            ]
        }
    )
    print(f'Agent has completed the research.....')
    research_report = result['structured_response']
    print(research_report)


