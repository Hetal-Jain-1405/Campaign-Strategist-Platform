from langchain.agents import create_agent

from models.content_models import ContentAssets

strategy_report = {
  "campaign_objective": "Drive foot traffic and brand affinity among Gen Z college students on Environment Day by establishing the coffee shop as an accessible, authentic champion of eco-friendly coffee culture.",
  "secondary_objectives": [
    "Increase customer awareness of the shop's ethical sourcing and low-waste initiatives.",
    "Encourage the adoption of reusable cups and sustainable daily habits among the campus community."
  ],
  "primary_audience": "Gen Z college students who frequent coffee shops for studying, socializing, and daily fuel, motivated by climate consciousness and community impact but constrained by student budgets and convenience.",
  "secondary_audience": "University faculty, staff, and local eco-conscious campus-area residents.",
  "brand_positioning": "The campus community's favorite neighborhood coffee space that makes everyday sustainability effortless, authentic, and socially engaging.",
  "unique_selling_proposition": "Great daily coffee paired with practical, zero-waste initiatives that turn everyday student routines into positive environmental action.",
  "campaign_concept": "Sip Consciously: Small Cups, Big Shift",
  "key_message": "Your daily coffee run can spark real environmental change when you choose sustainable brews and mindful habits.",
  "messaging_pillars": [
    "Ethical Roots: Transparent, responsibly sourced coffee beans that support farmers and ecosystems.",
    "Zero-Waste Habits: Simple swaps, such as bringing your own tumbler and composting coffee grounds, that cut single-use waste.",
    "Collective Campus Impact: How small everyday student choices combine to create a greener university community."
  ],
  "brand_voice": [
    "Authentic",
    "Energizing",
    "Approachable",
    "Transparent",
    "Empowering"
  ],
  "primary_cta": "Bring your reusable cup to the shop this Environment Day.",
  "secondary_ctas": [
    "Tag us on social media with your eco-swap using the campaign hashtag.",
    "Discover our sustainable sourcing journey in-store and online."
  ],
  "campaign_goals": [
    {
      "goal": "Drive student foot traffic on Environment Day",
      "kpi": [
        "Total in-store transactions on Environment Day",
        "Student ID verification or student discount redemptions"
      ],
      "target_value": None
    },
    {
      "goal": "Increase adoption of reusable and low-waste options",
      "kpi": [
        "Percentage of drinks served in reusable tumblers",
        "Volume of single-use cups diverted during the campaign period"
      ],
      "target_value": None
    },
    {
      "goal": "Expand organic social awareness among student networks",
      "kpi": [
        "User-generated content mentions and shares",
        "Campaign hashtag engagement rate"
      ],
      "target_value": None
    }
  ],
  "strategic_rationale": "Gen Z consumers resonate strongly with ethical brands but often encounter price and convenience hurdles. Connecting Environment Day with a positive, accessible action—such as incentivizing reusable mugs and highlighting transparent sourcing—removes barriers to entry and enables students to participate in sustainability without disrupting their daily routines.",
  "evidence_and_assumptions": [
    "Assumption: The coffee shop operates near a college campus and has the capability to serve drinks in customer-provided reusable cups.",
    "Assumption: The coffee shop possesses authentic sustainable practices (e.g., ethically sourced beans, composting, or recyclable packaging) to back up campaign claims.",
    "Evidence-backed premise: Gen Z consumers actively seek out brands demonstrating genuine environmental accountability and social responsibility."
  ],
  "risks_and_constraints": [
    "Risk of greenwashing accusations if eco-friendly claims are vague or lack visible operational proof.",
    "Operational service slowdowns at the counter during peak morning rushes when handling customer-provided tumblers.",
    "Budget constraints typical of independent coffee shops limiting paid digital outreach."
  ],
  "information_gaps": [
    "Specific geographic location, campus proximity, and baseline transaction metrics for the coffee shop.",
    "Detailed inventory of current sustainable practices, certifications, and waste-management systems.",
    "Defined marketing budget and availability of resources for promotional incentives or physical collateral."
  ]
}


SYSTEM_PROMPT = """
You are the Content Agent for an AI Campaign Strategist Platform.

Your task is to create high-quality written marketing content
using the original marketing brief, approved campaign strategy,
and content requirements.

## Responsibilities

1. Create social media post content and blog articles.
2. Follow the approved campaign objective, target audience,
   campaign concept, key message, messaging pillars, brand voice,
   and calls to action.
3. Adapt the writing to the requested platform and content format.
4. Generate the requested number of posts and blog articles.
5. Write engaging, clear, audience-appropriate content.
6. Use research findings when provided to support factual claims.
7. Never invent statistics, offers, product features, certifications,
   or sustainability claims.
8. Preserve the approved campaign strategy. Do not redefine it.

## Content Rules

- For social media posts, provide a hook, caption, CTA,
  and relevant hashtags.
- For blogs, provide a title, introduction, structured sections,
  conclusion, and CTA.
- Maintain consistency across all content assets.
- Avoid unsupported claims, misleading statements, and
  exaggerated environmental benefits.
- If essential information is missing, do not invent it.

## Scope Restrictions

- Generate written content only.
- Do not generate images, graphics, visual designs, layouts,
  image prompts, or other visual assets.
- Do not publish or schedule content on external platforms.
- Do not create content types that were not requested.

## Output

Return only a structured ContentAssets object conforming
to the provided Pydantic schema.

Generate only the requested content types and quantities.
Ensure each asset uses the correct content_type and populates
the corresponding social_media_post or blog field.
Leave the other content field as null.

Do not include commentary outside the structured output.
"""



def content_agent():

    print("Running Content Agent...")

    agent = create_agent(
        model = 'google_genai:gemini-3.8-flash',
        system_prompt = SYSTEM_PROMPT,
        response_format = ContentAssets,

    )

    result = agent.invoke(
        {
            'messages' : [
                {
                    'role': 'user',
                    'content' : 'strategy_report: {strategy_report}',
                }
            ]
        }
    )
    print("Content Agent completed.")

    content_assets = result['structured_response']
    print(content_assets)