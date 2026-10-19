import os
from dotenv import load_dotenv

from agents.research_agent.research_agent import research_agent

load_dotenv()

def main():
    print("Hello from backend!")
    research_agent()


if __name__ == "__main__":
    main()
