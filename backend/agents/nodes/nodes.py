# 3. Research Agent node
# -----------------------------------------

from agents.research_agent.research_agent import research_agent
from agents.strategy_agent.strategy_agent import strategy_agent
from models.campaignState_models import CampaignState
from agents.content_agent.content_agent import content_agent
from agents.visual_agent.visual_agent import visual_agent
from agents.media_planner_agent.media_planner_agent import media_planner_agent

from serializer import serialize
import logging
import json
import os
import re
from time import perf_counter

logger = logging.getLogger("campaign.agents")

research = research_agent()

def _bounded_context(value: object, limit: int, label: str) -> str:
    text = serialize(value)
    if len(text) <= limit:
        return text
    logger.warning(
        "Context truncated: section=%s original_chars=%d limit_chars=%d",
        label,
        len(text),
        limit,
    )
    return f"{text[:limit]}\n\n[Context truncated for demo speed; preserve the key decisions above.]"

def _print_message_content(content: object) -> None:
    if isinstance(content, str):
        print(content, end="", flush=True)
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, str):
                print(block, end="", flush=True)
            elif isinstance(block, dict) and isinstance(block.get("text"), str):
                print(block["text"], end="", flush=True)


def _find_structured_response(value: object) -> object | None:
    if isinstance(value, dict):
        if "structured_response" in value:
            return value["structured_response"]
        for child in value.values():
            found = _find_structured_response(child)
            if found is not None:
                return found
    elif isinstance(value, (list, tuple)):
        for child in value:
            found = _find_structured_response(child)
            if found is not None:
                return found
    return None


def _parse_streamed_json(text: str) -> object | None:
    cleaned = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).replace("```", "")
    decoder = json.JSONDecoder()
    candidates: list[object] = []
    for index, character in enumerate(cleaned):
        if character not in "{[":
            continue
        try:
            value, _ = decoder.raw_decode(cleaned[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, (dict, list)):
            candidates.append(value)
    dictionaries = [candidate for candidate in candidates if isinstance(candidate, dict)]
    return dictionaries[0] if dictionaries else (candidates[-1] if candidates else None)


def _stream_parts(agent, payload: dict):
    """Yield normalized (mode, data) pairs across LangGraph stream versions."""
    for part in agent.stream(
        payload,
        stream_mode=["messages", "updates", "values"],
    ):
        if isinstance(part, tuple) and len(part) == 2:
            yield part
        elif isinstance(part, dict) and "type" in part and "data" in part:
            yield part["type"], part["data"]
        else:
            logger.debug("Ignoring unrecognized agent stream part: %s", type(part).__name__)


def _invoke_agent(agent, agent_name: str, payload: dict):
    started = perf_counter()
    logger.info("LLM call started: agent=%s", agent_name)
    try:
        if agent_name == "strategy" and os.getenv("STREAM_STRATEGY", "false").lower() != "true":
            logger.info("Using structured strategy invoke mode for demo reliability: agent=%s", agent_name)
            result = agent.invoke(payload)
            structured_response = _find_structured_response(result)
            if structured_response is None:
                raise RuntimeError("strategy did not return a structured response")
            logger.info(
                "LLM response received: agent=%s duration_ms=%d structured_response=true",
                agent_name,
                round((perf_counter() - started) * 1000),
            )
            return {"structured_response": structured_response}
        print(f"\n--- {agent_name} Ollama output ---", flush=True)
        stream_chunks: list[object] = []
        streamed_text: list[str] = []
        for mode, chunk in _stream_parts(agent, payload):
            stream_chunks.append(chunk)
            if mode == "messages":
                message, _metadata = chunk
                content = getattr(message, "content", "")
                _print_message_content(content)
                if isinstance(content, str):
                    streamed_text.append(content)
                elif isinstance(content, list):
                    streamed_text.extend(
                        block
                        for block in content
                        if isinstance(block, str)
                    )
        print(f"\n\n[{agent_name}] token stream ended", flush=True)
        structured_response = _find_structured_response(stream_chunks)
        if structured_response is None:
            structured_response = _parse_streamed_json("".join(streamed_text))
            if structured_response is not None:
                logger.warning(
                    "Using streamed JSON fallback: agent=%s",
                    agent_name,
                )
        if structured_response is None:
            logger.error(
                "Agent stream ended without structured response: agent=%s chunk_types=%s",
                agent_name,
                [type(chunk).__name__ for chunk in stream_chunks],
            )
            raise RuntimeError(f"{agent_name} did not return a structured response")
        result = {"structured_response": structured_response}
    except Exception:
        logger.exception(
            "LLM call failed: agent=%s duration_ms=%d",
            agent_name,
            round((perf_counter() - started) * 1000),
        )
        raise
    logger.info(
        "LLM response received: agent=%s duration_ms=%d structured_response=%s",
        agent_name,
        round((perf_counter() - started) * 1000),
        "structured_response" in result,
    )
    for handler in logger.handlers:
        handler.flush()
    return result

def run_research(state: CampaignState):
    result = _invoke_agent(research, "research", {
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
    {_bounded_context(state["research_report"], 8000, "strategy.research")}

    Develop the campaign strategy using both inputs.
    Keep every string concise, use short list items, and do not repeat the
    research report. Return only the required structured strategy fields.
    """

    result = _invoke_agent(strategy, "strategy", {
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
    {_bounded_context(state["research_report"], 5000, "content.research")}

    Approved campaign strategy:
    {_bounded_context(state["campaign_strategy"], 7000, "content.strategy")}

    Generate the campaign content using these inputs.
    Follow the content requirements configured for the campaign.
    """

    result = _invoke_agent(content, "content", {
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
    {_bounded_context(state["campaign_strategy"], 7000, "visual.strategy")}

    Content assets:
    {_bounded_context(state["content_assets"], 7000, "visual.content")}

    Generate the actual visual assets corresponding to
    the supplied content using your configured image tool.
    """

    result = _invoke_agent(visual, "visual", {
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
    {_bounded_context(state["research_report"], 3500, "media.research")}

    Campaign strategy:
    {_bounded_context(state["campaign_strategy"], 6000, "media.strategy")}

    Content assets:
    {_bounded_context(state["content_assets"], 6000, "media.content")}

    Visual assets:
    {_bounded_context(state["visual_assets"], 5000, "media.visuals")}

    Create a campaign-specific media plan.
    Use the actual supplied assets and do not invent references.
    """

    result = _invoke_agent(media_planner, "media_planner", {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    return {
        "media_plan": result["structured_response"]
    }