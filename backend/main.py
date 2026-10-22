
from dotenv import load_dotenv

load_dotenv()


def main():
    from agents.orchestrator.orchestrator import chain
    from serializer import serialize

    campaign_description = input("Enter the campaign description: ")

    state = chain.invoke({
        "user_query": campaign_description
    })

    for key in [
        "research_report",
        "campaign_strategy",
        "content_assets",
        "visual_assets",
        "media_plan",
    ]:
        print(f"\n\n{key} output:")
        print(serialize(state[key]))


if __name__ == "__main__":
    main()
