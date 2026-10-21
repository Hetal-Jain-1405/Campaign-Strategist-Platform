from langchain.agents import create_agent

from models.media_planner_models import MediaPlan

visual_assets = {
  "assets": [
    {
      "asset_type": "social_media_creative",
      "platform": "Instagram",
      "aspect_ratio": "1:1",
      "visual_description": "A stylish reusable iced coffee tumbler filled with an iced oat latte on a sunlit campus study desk with notebooks and potted greenery.",
      "image_prompt": "A sleek reusable iced coffee tumbler with a glass straw filled with an iced oat milk latte, sitting on a sunlit wooden university study desk next to notebooks and small potted green plants, warm natural lighting, aesthetic college vibe, photorealistic, 4k, no text",
      "source_content_reference": "Your daily iced latte shouldn't cost the earth.",
      "image_path": "media/campaigns/1f1ce36af94a4f4b908d7bb6138d670f.png"
    },
    {
      "asset_type": "social_media_creative",
      "platform": "TikTok",
      "aspect_ratio": "9:16",
      "visual_description": "A vibrant and modern eco-friendly campus coffee bar showcasing stainless steel tumblers, glass cold brew decanters, and lush plants.",
      "image_prompt": "Vibrant modern eco-friendly campus coffee bar counter with reusable stainless steel tumblers, potted indoor plants, glass cold brew decanters, natural wood accents, warm ambient lighting, vertical composition, photorealistic, cinematic, no text",
      "source_content_reference": "POV: You found the campus coffee spot that actually matches your eco-values.",
      "image_path": "media/campaigns/1b3726569b7141bf83c45e3d96418c7a.png"
    },
    {
      "asset_type": "blog_image",
      "platform": "Blog",
      "aspect_ratio": "16:9",
      "visual_description": "Minimalist overhead editorial flat lay featuring a reusable ceramic travel mug, organic coffee beans, a journal, and botanical foliage in soft natural daylight.",
      "image_prompt": "Clean editorial overhead flat-lay photography featuring a ceramic reusable coffee travel mug, roasted organic coffee beans in a small wooden dish, a notebook with a pen, and green botanical leaves on a textured stone surface, soft natural daylight, minimalist aesthetic, high resolution, no text",
      "source_content_reference": "Beyond the Cup: How College Students Can Sip More Sustainably",
      "image_path": "media/campaigns/36272609ad7947bf9ce46a81e51ca35f.png"
    }
  ]
}

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
You are the Media Planner Agent for an AI Campaign Strategist Platform.

Your task is to create a campaign-specific media plan using the
provided campaign strategy, research report, content assets,
visual assets, budget, campaign duration and user campaign details.

## Responsibilities
- Recommend marketing channels suited to the campaign's target audience.
- Match existing content and visuals to appropriate platforms.
- Recommend suitable content formats and posting frequencies.
- Organize activities into campaign phases aligned with campaign goals.
- Create a practical posting schedule.
- Propose budget allocations when budget information is available.
- Recommend testing approaches and measurable performance metrics.

## General Rules
- Treat the approved campaign strategy as the primary source of direction.
- Use research findings to support channel and audience recommendations.
- Consider the campaign objective, target audience, brand voice,
  messaging, CTAs, and available resources in every recommendation.
- Use the provided content and visual assets; do not invent asset
  references or create new content or visuals.
- Select platforms based on audience relevance and campaign goals,
  not generic defaults or personal assumptions.
- Ensure every planned activity supports a specific campaign objective.
- Adapt campaign phases, channels, formats, and schedules to the
  campaign's context rather than using a fixed template.
- Do not assume a B2B, corporate, or professional audience unless
  specified in the provided inputs.
- Do invent dates, budgets, costs, audience data, or performance results.
- If information is missing, state the limitation or record a reasonable,
  clearly identified assumption.
- Label budget allocations as proposals, not approved spending.
- Do not publish, schedule, or purchase advertisements.

## Output
Return only a structured MediaPlan object conforming to the
provided Pydantic schema.

Ensure the plan is consistent with the supplied campaign strategy
and uses available assets wherever relevant.
Do not include commentary outside the structured output.
"""



def media_planner_agent():
    """Creates a media plan thtat includes a list of media channels, budget allocation, and a timeline for the campaign."""

    print("Invoking Media Planner Agent...")

    agent = create_agent(
        model = 'google_genai:gemini-3.8-flash',
        system_prompt = SYSTEM_PROMPT,
        response_format = MediaPlan
    )

    result = agent.invoke(
        {
            'messages': [
                {
                    'role': 'user',
                    'content': 'Strategy Report: {strategy_report}, Research Report: {research_report}, Content Assets: {content_assets}, Visual Assets: {visual_assets}. For Environment Day, I want to create a campaign for my coffee shop that attracts Gen Z college students while raising awareness about environmentally sustainable coffee and eco-friendly practices.'
                }
            ]
        }
    )

    print("Media Planner Agent Result:")

    media_plan = result['structured_response']
    print(media_plan)