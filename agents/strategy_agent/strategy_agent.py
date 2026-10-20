from langchain.agents import create_agent

from models.strategy_models import CampaignStrategy

research_report = {
  "research_summary": "This research report evaluates market trends, competitor strategies, and Gen Z student behaviors to inform an Environment Day campaign for an independent coffee shop. Gen Z college students place high importance on environmental responsibility, with approximately 84% interested in or actively practicing sustainability and over a third viewing it as a top priority. However, financial constraints represent a major barrier; students desire eco-friendly choices such as plant-based milks and waste reduction but resist high price premiums. Industry leaders such as Blue Bottle demonstrate that tangible economic incentives, such as doubling personal cup discounts and introducing zero-waste cafe pilots, drive measurable behavioral shifts away from disposable single-use cups. For Environment Day, an optimal campaign pairs accessible price relief (such as a Bring Your Own Cup discount and waived plant-milk upcharges) with transparent digital storytelling and campus micro-influencer partnerships to build genuine brand affinity without evoking greenwashing skepticism.",

  "competitor_analysis": [
    {
      "competitor_name": "Blue Bottle Coffee",
      "website_url": "https://blog.bluebottlecoffee.com/posts/timeline",
      "product_or_service": "Specialty coffee beverages, whole bean coffee, and eco-friendly merchandise",
      "positioning": "Premium specialty roaster focused on verified carbon neutrality, regenerative agriculture, and zero-waste cafe operations",
      "pricing": "Premium price point ($5.00 to $8.00 per specialty beverage; standard 25-cent personal cup discount)",
      "public_product_claims": [
        "Achieved 2024 carbon neutrality through operational emission reductions and verified carbon offsets",
        "Sourcing verified under the Coffee Sustainability Reference Code and Enveritas Responsibly Sourced standard"
      ],
      "strengths": [
        "Pioneered zero-waste cafe pilots to eliminate single-use disposable cups",
        "Clear, verifiable sustainability milestones that resonate with ethically minded consumers"
      ],
      "weaknesses_or_gaps": [
        "High premium pricing creates an accessibility barrier for budget-constrained college students",
        "National brand scale lacks hyper-local campus community integration"
      ],
      "source_urls": [
        "https://blog.bluebottlecoffee.com/posts/timeline",
        "https://www.cbsnews.com/news/blue-bottle-coffee-to-eliminate-disposable-cups-and-packaging-by-the-end-of-2020"
      ],
      "confidence": "high"
    },
    {
      "competitor_name": "Starbucks Coffee",
      "website_url": "https://www.starbucks.com/",
      "product_or_service": "Commercial specialty espresso drinks, cold brew, food items, and reusable drinkware",
      "positioning": "Mass-market convenience and lifestyle coffee hub with corporate sustainability targets",
      "pricing": "Mid-to-high price tier ($4.00 to $7.00 per beverage; 10-cent reusable cup discount)",
      "public_product_claims": [
        "Commitment to cut carbon, water, and waste footprints by 50% by 2030",
        "Offers personal cup incentives across in-store and drive-thru channels"
      ],
      "strengths": [
        "Ubiquitous physical presence near college campuses and highly adopted digital loyalty program",
        "Convenient operational infrastructure for quick customer turnover"
      ],
      "weaknesses_or_gaps": [
        "Frequently scrutinized by Gen Z consumers for slow implementation of waste-free solutions",
        "High volume of single-use plastic cups fuels perception of corporate greenwashing"
      ],
      "source_urls": [
        "https://www.mdpi.com/2071-1050/16/8/3126"
      ],
      "confidence": "high"
    }
  ],

  "market_trends": [
    {
      "trend": "Plant-Based Dairy Alternatives as Sustainability Drivers",
      "description": "Rising preference among younger generations for oat, almond, and soymilks due to their significantly lower carbon, water, and land footprints compared to dairy agriculture.",
      "relevance_to_campaign": "Waiving plant-based milk upcharges on Environment Day directly aligns with Gen Z values and removes a common purchase friction point.",
      "evidence": "Animal agriculture contributes substantially to greenhouse gas emissions and water usage; industry research shows Gen Z actively adopts plant milks as an everyday ethical choice.",
      "source_urls": [
        "https://www.drinkripples.com/blog/eco-friendly-coffee-trends"
      ],
      "confidence": "high"
    },
    {
      "trend": "Transition from Single-Use Packaging to Circular Reusables",
      "description": "Accelerating push to eliminate disposable cups through Bring Your Own Cup (BYOC) incentives, deposit mug programs, and compostable packaging.",
      "relevance_to_campaign": "Single-use cup reduction serves as an immediately visible, participatory campaign hook for students on Environment Day.",
      "evidence": "Average cafes dispose of approximately 15,000 single-use cups per month; First Insight research indicates Gen Z shoppers actively favor sustainable brands and are willing to pay up to 10% more for sustainable practices.",
      "source_urls": [
        "https://www.drinkripples.com/blog/eco-friendly-coffee-trends",
        "https://www.cbsnews.com/news/blue-bottle-coffee-to-eliminate-disposable-cups-and-packaging-by-the-end-of-2020"
      ],
      "confidence": "high"
    },
    {
      "trend": "Transparent Social-First Eco-Storytelling",
      "description": "Gen Z consumers increasingly verify sustainability claims via short-form social video platforms (TikTok, Instagram) focusing on behind-the-scenes authenticity rather than corporate jargon.",
      "relevance_to_campaign": "The campaign must highlight tangible, verifiable cafe practices (e.g., composting spent coffee grounds) via digital content created with relatable peers.",
      "evidence": "A 2024 University of Pennsylvania study found that 84% of Gen Z TikTok users seek sustainability content, prioritizing authentic, practical, and trust-based advice over corporate claims.",
      "source_urls": [
        "https://www.theearthandi.org/post/sustainability-influencers-are-reaching-gen-z",
        "https://www.mdpi.com/2071-1050/16/8/3126"
      ],
      "confidence": "high"
    }
  ],

  "campaign_research": [
    {
      "campaign_name": "Earth Month Reusable Cup Incentive",
      "brand_name": "Blue Bottle Coffee",
      "campaign_objective": "Incentivize reusable container adoption and lower single-use cup waste during Earth Month.",
      "target_audience": "Urban, eco-conscious specialty coffee drinkers",
      "campaign_approach": [
        "Doubled the standard bring-your-own-cup discount from 25 cents to 50 cents throughout April",
        "Amplified educational content across social media highlighting progress toward carbon neutrality and cafe waste elimination"
      ],
      "observed_outcomes": [
        "Drove heightened consumer awareness around personal waste generation",
        "Generated strong customer engagement on Instagram Reels regarding practical sustainability habits"
      ],
      "lessons_for_campaign": [
        "Direct financial incentives reduce the friction of carrying personal cups, making sustainable habits tangible for students."
      ],
      "source_urls": [
        "https://www.instagram.com/reel/C6Esza2P3p_",
        "https://www.cbsnews.com/news/blue-bottle-coffee-to-eliminate-disposable-cups-and-packaging-by-the-end-of-2020"
      ],
      "confidence": "high"
    }
  ],

  "audience_insights": [
    {
      "insight_type": "pain_point",
      "description": "College students face strict budget limits and view sustainability premiums or plant-milk surcharges as an unfair financial burden.",
      "supporting_evidence": "Academic research on Gen Z coffee consumption underscores that while students want eco-friendly offerings, cafes must directly manage cost concerns to maintain patronage.",
      "source_urls": [
        "https://www.wittenborg.eu/eba-thesis-explores-gen-zs-sustainable-coffee-shop-choices-vietnam.htm"
      ],
      "confidence": "high"
    },
    {
      "insight_type": "interest",
      "description": "Gen Z is deeply committed to climate change mitigation, zero-waste initiatives, and ethical consumerism.",
      "supporting_evidence": "Survey data indicates that 84% of surveyed Gen Z social media users are actively engaged in or curious about sustainable living, and 35% treat sustainability as a core everyday priority.",
      "source_urls": [
        "https://www.theearthandi.org/post/sustainability-influencers-are-reaching-gen-z",
        "https://www.mdpi.com/2071-1050/16/8/3126"
      ],
      "confidence": "high"
    },
    {
      "insight_type": "behavior",
      "description": "Young adults discover and evaluate sustainable lifestyle practices primarily through peer creators and micro-influencers on TikTok and Instagram.",
      "supporting_evidence": "Research on sustainability influencers confirms Gen Z relies on social creators for authentic tips on sustainable student routines, valuing relatability over polished corporate branding.",
      "source_urls": [
        "https://www.theearthandi.org/post/sustainability-influencers-are-reaching-gen-z",
        "https://afluencer.com/blog/coffee-shop-marketing"
      ],
      "confidence": "high"
    },
    {
      "insight_type": "opportunity",
      "description": "Rewarding eco-friendly student behaviors with affordable perks (e.g., free non-dairy upgrades, loyalty stamps) fosters long-term campus loyalty.",
      "supporting_evidence": "MDPI research demonstrates that active promotion of eco-friendly practices in coffee shops directly enhances green brand image, brand attachment, and brand advocacy among Gen Z.",
      "source_urls": [
        "https://www.mdpi.com/2071-1050/16/8/3126"
      ],
      "confidence": "high"
    }
  ],

  "campaign_opportunities": [
    {
      "opportunity": "The 'Campus BYOC (Bring Your Own Cup)' Environment Day Challenge",
      "rationale": "Overcomes the student financial barrier while visibly cutting single-use cup waste, providing an immediate incentive to visit the shop on Environment Day.",
      "supporting_evidence": [
        "Blue Bottle demonstrated success by doubling personal cup discounts to 50 cents",
        "Gen Z is motivated by practical, budget-conscious green habits rather than costly green products"
      ],
      "recommended_direction": "Offer 50% off drip coffee or cold brew and waive plant-milk surcharges for any student bringing a reusable cup on Environment Day, accompanied by a digital stamp card rewarding repeat reusable visits.",
      "limitations": [
        "Requires baristas to follow strict local health codes and hygiene handling procedures for customer-supplied cups during peak hours."
      ]
    },
    {
      "opportunity": "'Grounds to Grow' Circular Upcycling & Peer Content Collaboration",
      "rationale": "Provides a tangible, transparent sustainability initiative that students can experience firsthand and share on social media, reinforcing authenticity.",
      "supporting_evidence": [
        "Gen Z values tangible eco-friendly practices (EFPs) over abstract claims",
        "Micro-influencer collaborations drive localized foot traffic and credible word-of-mouth on campus"
      ],
      "recommended_direction": "Package spent espresso grounds into free take-home plant fertilizer bags for students with plant-care tips, while partnering with campus sustainability student ambassadors to document the zero-waste workflow on TikTok.",
      "limitations": [
        "Requires advance collection, drying, and packaging of coffee grounds to ensure clean and safe distribution without mold growth."
      ]
    }
  ],

  "research_gaps": [
    {
      "topic": "Campus-Specific Beverage Price Elasticity",
      "reason": "Student budgets and willingness to pay vary significantly depending on public vs. private university location and campus meal plan flex dollars.",
      "additional_data_needed": "In-store transaction analysis or a short student survey testing volume response across different discount levels."
    },
    {
      "topic": "Local Campus Competitor Sustainability Initiatives",
      "reason": "Independent competitor cafes adjacent to the university may already run existing reusable cup or mug-share programs.",
      "additional_data_needed": "Direct on-the-ground audit of promotional offerings within a 1-mile perimeter of the college campus."
    }
  ],

  "sources": [
    {
      "source_id": "src_01",
      "title": "Eco Friendly Coffee Shop Trends Unveiled",
      "url": "https://www.drinkripples.com/blog/eco-friendly-coffee-trends",
      "publisher": "Ripples",
      "publication_date": "2023-08-15",
      "access_date": "2025-02-23",
      "source_type": "industry_report",
      "supports_claims": [
        "Gen Z shoppers prefer sustainable brands and are willing to pay up to 10% more",
        "Plant-based milk and eco-packaging significantly decrease cafe environmental footprint"
      ]
    },
    {
      "source_id": "src_02",
      "title": "EBA Thesis Explores Gen Z's Sustainable Coffee Shop Choices in Vietnam",
      "url": "https://www.wittenborg.eu/eba-thesis-explores-gen-zs-sustainable-coffee-shop-choices-vietnam.htm",
      "publisher": "Wittenborg University of Applied Sciences",
      "publication_date": "2024-03-12",
      "access_date": "2025-02-23",
      "source_type": "research_paper",
      "supports_claims": [
        "Gen Z coffee consumers demand green practices but have tight budget constraints",
        "Green promotions and transparent communication drive student purchase intent"
      ]
    },
    {
      "source_id": "src_03",
      "title": "The Impact of Eco-Friendly Practices on Generation Z's Green Image, Brand Attachment, Brand Advocacy, and Brand Loyalty in Coffee Shop",
      "url": "https://www.mdpi.com/2071-1050/16/8/3126",
      "publisher": "MDPI - Sustainability",
      "publication_date": "2024-04-10",
      "access_date": "2025-02-23",
      "source_type": "research_paper",
      "supports_claims": [
        "35% of Gen Z considers sustainability a top priority",
        "Promoting tangible eco-friendly practices across social networks enhances brand attachment and customer advocacy"
      ]
    },
    {
      "source_id": "src_04",
      "title": "Blue Bottle Coffee to test eliminating disposable cups and packaging",
      "url": "https://www.cbsnews.com/news/blue-bottle-coffee-to-eliminate-disposable-cups-and-packaging-by-the-end-of-2020",
      "publisher": "CBS News",
      "publication_date": "2019-12-13",
      "access_date": "2025-02-23",
      "source_type": "news",
      "supports_claims": [
        "Individual cafes generate approximately 15,000 single-use cups monthly",
        "Reusable container programs can eliminate landfill waste in retail coffee"
      ]
    },
    {
      "source_id": "src_05",
      "title": "Sustainability Influencers Are Reaching Gen Z",
      "url": "https://www.theearthandi.org/post/sustainability-influencers-are-reaching-gen-z",
      "publisher": "The Earth & I (Penn Center for Science, Sustainability, and the Media)",
      "publication_date": "2024-06-18",
      "access_date": "2025-02-23",
      "source_type": "research_paper",
      "supports_claims": [
        "84% of Gen Z social media users are interested in or actively seeking sustainability advice",
        "Authenticity and practical advice from creators are vital to driving real-world eco actions"
      ]
    },
    {
      "source_id": "src_06",
      "title": "Earth Month Reusable Cup Promotion",
      "url": "https://www.instagram.com/reel/C6Esza2P3p_",
      "publisher": "Instagram / Blue Bottle Coffee",
      "publication_date": "2024-04-22",
      "access_date": "2025-02-23",
      "source_type": "social_profile",
      "supports_claims": [
        "Blue Bottle doubled reusable cup discounts to 50 cents during Earth Month to drive waste reduction"
      ]
    }
  ],

  "metadata": {
    "research_scope": "Environment Day sustainability campaign strategy targeting Gen Z college students for an independent coffee shop",
    "geographic_location": "Unknown",
    "product_category": "Coffee & Beverage Retail",
    "research_date": "2025-02-23",
    "limitations": [
      "Specific university campus and geography were not specified in the brief",
      "Operational margins and promotional budgets for discounts were not provided"
    ],
    "overall_confidence": "high"
  }
}


SYSTEM_PROMPT = """
You are the Strategy Agent for an AI Campaign Strategist Platform.

Your task is to transform the original marketing brief and Research
Agent's report {research_report} into a clear, coherent campaign strategy.

## Responsibilities
1. Define the primary campaign objective and relevant secondary objectives.
2. Identify the primary and secondary target audiences using available evidence.
3. Establish brand positioning and a USP when supported by the inputs.
4. Develop one central campaign concept and key message.
5. Define consistent messaging pillars and brand voice.
6. Recommend relevant primary and secondary CTAs.
7. Suggest campaign goals and KPIs without inventing numerical targets.
8. Explain the strategic rationale, assumptions, risks, and information gaps.

## Guidelines
- Treat the original brief as the source of campaign requirements.
- Use the Research Agent's report as supporting evidence.
- Do not repeat the research report or conduct additional research.
- Never invent facts, statistics, brand attributes, offers, or results.
- Distinguish research-backed findings from strategic recommendations.
- If information is missing, state the assumption or identify the gap.
- Keep the objective, audience, positioning, messaging, tone, and CTA aligned.
- Do not create finished advertisements, social media posts, scripts,
  or visual assets. These belong to downstream agents.
- Ensure the strategy is specific enough for Content and Visual Agents
  to execute without redefining the campaign.

## Output
Return only a structured CampaignStrategy object conforming to the
provided Pydantic schema.
Populate all required fields. Use empty lists or null for missing
optional information where permitted by the schema.
Do not add fields outside the schema or include commentary.
"""



def strategy_agent():
    """Transform the original marketing brief and Research Agent report into a coherent, evidence-informed campaign strategy."""

    print("Running Strategy Agent...")

    agent = create_agent(
        model = 'google_genai:gemini-3.8-flash',
        system_prompt = SYSTEM_PROMPT,
        response_format = CampaignStrategy,
    )

    result = agent.invoke(
        {
            'messages' : [
              {
                'role' : 'user',
                'content' : 'For Environment Day, I want to create a campaign for my coffee shop that attracts Gen Z college students while raising awareness about environmentally sustainable coffee and eco-friendly practices. Research_Agent = {research_report} ',
              }
            ]
        }
    )

    print("Strategy Agent completed.")

    strategy_report = result['structured_response']
    print(strategy_report)