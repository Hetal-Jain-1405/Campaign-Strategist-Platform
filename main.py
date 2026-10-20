import os
from dotenv import load_dotenv

from agents.strategy_agent.strategy_agent import strategy_agent
from agents.research_agent.research_agent import research_agent
from agents.content_agent.content_agent import content_agent
from agents.visual_agent.visual_agent import visual_agent

load_dotenv()

def main():
    print("Hello from backend!")
    # research_agent()
    # strategy_agent()
    # content_agent()
    visual_agent()

if __name__ == "__main__":
    main()
