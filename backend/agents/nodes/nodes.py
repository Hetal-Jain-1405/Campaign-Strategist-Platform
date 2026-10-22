# 3. Research Agent node
# -----------------------------------------

from agents.research_agent.research_agent import research_agent
from agents.strategy_agent.strategy_agent import strategy_agent
from models.campaignState_models import CampaignState
from agents.content_agent.content_agent import content_agent
from agents.visual_agent.visual_agent import visual_agent
from agents.media_planner_agent.media_planner_agent import media_planner_agent

from serializer import serialize

research = research_agent()

def run_research(state: CampaignState):
    result = research.invoke({
        "messages": [
            {
                "role": "user",
                "content": state["user_query"],
            }
        ]
    })

    return {
        "research_report": result["structured_response"]
    }


# -----------------------------------------
# 4. Strategy Agent node
# -----------------------------------------

strategy = strategy_agent()

def run_strategy(state: CampaignState):
    prompt = f"""
    Original campaign description:
    {state["user_query"]}

    Research report:
    {serialize(state["research_report"])}

    Develop the campaign strategy using both inputs.
    """

    result = strategy.invoke({
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    return {
        "campaign_strategy": result["structured_response"]
    }


# -----------------------------------------
# 5. Content Agent node
# -----------------------------------------

content = content_agent()

def run_content(state: CampaignState):
    prompt = f"""
    Original campaign description:
    {state["user_query"]}

    Research report:
    {serialize(state["research_report"])}

    Approved campaign strategy:
    {serialize(state["campaign_strategy"])}

    Generate the campaign content using these inputs.
    Follow the content requirements configured for the campaign.
    """

    result = content.invoke({
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    return {
        "content_assets": result["structured_response"]
    }


# -----------------------------------------
# 6. Visual Agent node
# -----------------------------------------

visual = visual_agent()

def run_visual(state: CampaignState):
    prompt = f"""
    Original campaign description:
    {state["user_query"]}

    Campaign strategy:
    {serialize(state["campaign_strategy"])}

    Content assets:
    {serialize(state["content_assets"])}

    Generate the actual visual assets corresponding to
    the supplied content using your configured image tool.
    """

    result = visual.invoke({
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    return {
        "visual_assets": result["structured_response"]
    }


# -----------------------------------------
# 7. Media Planner Agent node
# -----------------------------------------

media_planner = media_planner_agent()

def run_media_planner(state: CampaignState):
    prompt = f"""
    Original campaign description:
    {state["user_query"]}

    Research report:
    {serialize(state["research_report"])}

    Campaign strategy:
    {serialize(state["campaign_strategy"])}

    Content assets:
    {serialize(state["content_assets"])}

    Visual assets:
    {serialize(state["visual_assets"])}

    Create a campaign-specific media plan.
    Use the actual supplied assets and do not invent references.
    """

    result = media_planner.invoke({
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    return {
        "media_plan": result["structured_response"]
    }