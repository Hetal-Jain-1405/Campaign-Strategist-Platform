from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

from models.campaignState_models import CampaignState
from agents.nodes.nodes import run_research, run_strategy, run_content, run_visual, run_media_planner

workflow = StateGraph(CampaignState)

workflow.add_node('research_agent', run_research)
workflow.add_node('strategy_agent', run_strategy)
workflow.add_node('content_agent', run_content)
workflow.add_node('visual_agent', run_visual)
workflow.add_node('media_planner_agent', run_media_planner)

workflow.add_edge(START, 'research_agent')
workflow.add_edge('research_agent', 'strategy_agent')
workflow.add_edge('strategy_agent', 'content_agent')
workflow.add_edge('content_agent', 'visual_agent')
workflow.add_edge('visual_agent', 'media_planner_agent')
workflow.add_edge('media_planner_agent', END)

# Workflow compile
chain = workflow.compile()

# Show workflow
display(Image(chain.get_graph().draw_mermaid_png()))
