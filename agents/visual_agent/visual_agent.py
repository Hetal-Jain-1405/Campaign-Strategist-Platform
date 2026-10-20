from langchain.agents import create_agent

from agents.visual_agent.generate_campaign_image import generate_campaign_image
from models.visual_models import VisualAssets


content_assets = {
  "assets": [
    {
      "content_type": "social_media_post",
      "social_media_post": {
        "platform": "Instagram",
        "hook": "Your daily iced latte shouldn't cost the earth.",
        "caption": "Studying for finals hits different when your caffeine fix actually gives back. This Environment Day, we're shining a light on conscious sipping. From ethically sourced beans to zero single-use plastic cups behind our counter, we believe small daily habits spark real change. Bring your own reusable tumbler today and grab your favorite brew while keeping landfills lighter. Let's make sustainable sips the new normal on campus.",
        "call_to_action": "Tag a study buddy who always remembers their reusable cup and stop by today!",
        "hashtags": [
          "#EnvironmentDayReady",
          "#SipSustainably",
          "#CampusEcoHabits",
          "#GenZClimateAction",
          "#EcoCoffee"
        ]
      },
      "blog": None
    },
    {
      "content_type": "social_media_post",
      "social_media_post": {
        "platform": "TikTok",
        "hook": "POV: You found the campus coffee spot that actually matches your eco-values.",
        "caption": "We know greenwashing is real, so let's keep it 100% transparent: our coffee grounds get composted, our oat milk cartons get recycled, and your reusable mug gets you an instant high five (and less waste in the bin). Doing good for the planet does not mean giving up your morning cold brew. Small swaps, massive campus impact.",
        "call_to_action": "Drop your favorite eco-friendly study routine tip in the comments!",
        "hashtags": [
          "#SustainableStudent",
          "#EcoFriendlyLiving",
          "#CollegeLifeHacks",
          "#EnvironmentDay",
          "#ConsciousCoffee"
        ]
      },
      "blog": None
    },
    {
      "content_type": "blog",
      "social_media_post": None,
      "blog": {
        "title": "Beyond the Cup: How College Students Can Sip More Sustainably",
        "introduction": "Between early lectures, library study marathons, and balancing campus life, coffee is often the non-negotiable fuel of student existence. But as Gen Z leads the conversation around climate accountability and environmental awareness, many students are asking: what is the true footprint of our daily caffeine habit? For Environment Day, we explore how thoughtful everyday choices can transform our coffee culture without giving up your favorite morning ritual.",
        "sections": [
          "The Lifecycle of Your Daily Brew: Sustainable coffee starts long before the espresso machine turns on. Responsible sourcing prioritizes shade-grown crops, biodiversity protection, and fair labor practices for farming communities. When coffee shops choose certified ethical suppliers, every cup helps safeguard vital ecosystems and reduces deforestation risks.",
          "Tackling the Single-Use Dilemma: Millions of disposable cups end up in landfills every single day because paper to-go cups often feature a plastic lining that prevents conventional recycling. Shifting toward reusable mugs, steel tumblers, and compostable alternatives is one of the most immediate, high-impact changes students can adopt across campus dining halls and local cafes.",
          "Circular Habits on Campus: Sustainability is not about doing everything flawlessly; it is about building practical, repeatable habits. From supporting cafes that compost used espresso grounds to choosing plant-based milk options that generally require less water and land to produce, student choices actively direct how businesses operate."
        ],
        "conclusion": "Individual choices gain immense power when adopted across a student community. Celebrating Environment Day is not just about a single moment of awareness—it is about turning daily rituals into steady acts of care for our collective future.",
        "call_to_action": "Bring your own reusable mug to our counter this week and join the campus movement toward conscious coffee consumption."
      }
    }
  ]
}



SYSTEM_PROMPT = """
You are the Visual Agent for an AI Campaign Strategist Platform.

Your task is to generate actual images based on the ContentAssets
provided by the Content Agent.

## Responsibilities
- Analyze each content asset to understand its message, audience,
  and intended platform.
- Create a detailed image-generation prompt for each asset.
- Use the generate_campaign_image tool to generate the actual images.
- Match the visual style to the content, campaign, and platform.
- Link each generated image to its corresponding content asset.
- Generate visuals only; do not rewrite posts or blog content.

## Guidelines
- Follow the provided content and brand guidelines.
- Do not invent facts, logos, or product details.
- Avoid generating text within images unless explicitly requested.
- Do not claim image generation succeeded if the tool fails.

## Output
Return only a structured VisualAssets object containing each
asset's type, platform, aspect ratio, visual description,
image prompt, content reference, and generated image path or URL.

Generate visuals only for the supplied ContentAssets.
Do not include commentary outside the structured output.
"""



def visual_agent():
    """Creates a visual agent that can generate images based on content assets"""

    print(f'Initialising the visual agent.....')

    agent = create_agent(
        model = "google_genai:gemini-3.8-flash",
        system_prompt = SYSTEM_PROMPT,
        tools = [generate_campaign_image,],
        response_format = VisualAssets,
    )

    result = agent.invoke(
        {
            'messages': [
                {
                    'role': 'user',
                    "content": f"""
                    Generate visual assets for the following content.

                    Content Assets: {content_assets}

                    Generate an actual image for each content asset
                    using the generate_campaign_image tool.
                    Return the structured VisualAssets output.
                    """
                }
            ]
        }
    )

    print(f'Visual Agent has completed the image generation.....')

    visual_assets = result['structured_response']
    print(visual_assets)
