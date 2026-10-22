"""Validate the local provider and offline integration configuration."""

from agents.content_agent.content_agent import content_agent
from agents.media_planner_agent.media_planner_agent import media_planner_agent
from agents.research_agent.research_agent import research_agent
from agents.strategy_agent.strategy_agent import strategy_agent
from agents.visual_agent.generate_campaign_image import generate_campaign_image
from agents.visual_agent.visual_agent import visual_agent


def main() -> None:
    agents = {
        "research": research_agent(),
        "strategy": strategy_agent(),
        "content": content_agent(),
        "visual": visual_agent(),
        "media_planner": media_planner_agent(),
    }
    fixture_path = generate_campaign_image.invoke({"prompt": "local demo fixture"})
    print(f"Configured agents: {', '.join(agents)}")
    print(f"Fixture visual: {fixture_path}")


if __name__ == "__main__":
    main()
