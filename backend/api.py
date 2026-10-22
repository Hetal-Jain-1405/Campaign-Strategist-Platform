import os
import logging
from datetime import datetime, timezone
from typing import Annotated, Any
from uuid import UUID

import requests
from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api_models import (
    Campaign,
    CampaignCreate,
    CampaignOutput,
    CampaignRun,
    CampaignUpdate,
)

load_dotenv()
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("campaign.api")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())


class ConfigurationError(RuntimeError):
    pass


def _setting(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ConfigurationError(f"{name} is not configured")
    return value


def _configuration_http_error(exc: ConfigurationError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=str(exc),
    )


def _pipeline_error_details(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "resource_exhausted" in lowered or "quota" in lowered or "rate limit" in lowered:
        return {
            "type": "provider_quota",
            "message": (
                "Gemini API quota exceeded. Switch AI_PROVIDER=ollama for the local demo, "
                "or check Gemini billing and rate limits before retrying."
            ),
        }
    return {"type": type(exc).__name__, "message": message[:1000]}


def _supabase_request(
    method: str,
    path: str,
    access_token: str,
    *,
    body: dict[str, Any] | None = None,
) -> requests.Response:
    try:
        base_url = _setting("SUPABASE_URL").rstrip("/")
        anon_key = _setting("SUPABASE_ANON_KEY")
    except ConfigurationError as exc:
        raise _configuration_http_error(exc) from exc
    try:
        return requests.request(
            method,
            f"{base_url}{path}",
            headers={
                "apikey": anon_key,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            },
            json=body,
            timeout=15,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Campaign storage service unavailable",
        ) from exc


def _require_storage(response: requests.Response, message: str) -> list[dict[str, Any]]:
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail=message)
    try:
        payload = response.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="Storage returned invalid JSON") from exc
    if not isinstance(payload, list):
        raise HTTPException(status_code=502, detail="Storage returned an invalid record set")
    return payload


def _update_run(
    token: str,
    run_id: UUID,
    *,
    status_value: str | None = None,
    current_agent: str | None = None,
    completed_agents: list[str] | None = None,
    progress: int | None = None,
    error_details: dict[str, Any] | None = None,
    started_at: str | None = None,
    completed_at: str | None = None,
) -> None:
    body: dict[str, Any] = {}
    if status_value is not None:
        body["status"] = status_value
    if current_agent is not None:
        body["current_agent"] = current_agent
    if completed_agents is not None:
        body["completed_agents"] = completed_agents
    if progress is not None:
        body["progress"] = progress
    if error_details is not None:
        body["error_details"] = error_details
    if started_at is not None:
        body["started_at"] = started_at
    if completed_at is not None:
        body["completed_at"] = completed_at
    response = _supabase_request(
        "PATCH",
        f"/rest/v1/campaign_runs?id=eq.{run_id}",
        token,
        body=body,
    )
    if response.status_code >= 400:
        raise RuntimeError("Unable to persist campaign run state")


def _run_pipeline(
    token: str,
    run_id: UUID,
    campaign_id: UUID,
    brief: str,
    brand_context: str | None,
    market_context: str | None,
) -> None:
    agents = ["research_agent", "strategy_agent", "content_agent", "visual_agent", "media_planner_agent"]
    completed_agents: list[str] = []
    logger.info("Campaign pipeline started: campaign_id=%s run_id=%s agents=%d", campaign_id, run_id, len(agents))
    try:
        logger.info("Background worker updating run to running: run_id=%s", run_id)
        _update_run(
            token,
            run_id,
            status_value="running",
            progress=0,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        campaign_update = _supabase_request(
            "PATCH",
            f"/rest/v1/campaigns?id=eq.{campaign_id}",
            token,
            body={"status": "running"},
        )
        if campaign_update.status_code >= 400:
            raise RuntimeError("Unable to mark campaign running")
        logger.info("Loading campaign agent graph: run_id=%s", run_id)
        from agents.orchestrator.orchestrator import chain
        logger.info("Campaign agent graph loaded: run_id=%s", run_id)

        query = brief
        if brand_context:
            query += f"\nBrand context:\n{brand_context}"
        if market_context:
            query += f"\nMarket context:\n{market_context}"

        state: dict[str, Any] = {"user_query": query}
        for update in chain.stream(state, stream_mode="updates"):
            for agent_name, agent_output in update.items():
                if agent_name not in agents:
                    continue
                state.update(agent_output)
                output_key = {
                    "research_agent": ("research", "research_report"),
                    "strategy_agent": ("strategy", "campaign_strategy"),
                    "content_agent": ("content", "content_assets"),
                    "visual_agent": ("visuals", "visual_assets"),
                    "media_planner_agent": ("media_plan", "media_plan"),
                }[agent_name]
                output_type, state_key = output_key
                output = state.get(state_key)
                logger.info(
                    "Agent output received: campaign_id=%s run_id=%s agent=%s output_type=%s",
                    campaign_id,
                    run_id,
                    agent_name,
                    output_type,
                )
                payload = output.model_dump(mode="json") if hasattr(output, "model_dump") else output
                saved = _supabase_request(
                    "POST",
                    "/rest/v1/campaign_outputs",
                    token,
                    body={"run_id": str(run_id), "output_type": output_type, "payload": payload},
                )
                if saved.status_code >= 400:
                    raise RuntimeError(f"Unable to persist {output_type} output")
                completed_agents.append(agent_name)
                _update_run(
                    token,
                    run_id,
                    current_agent=agent_name,
                    completed_agents=completed_agents,
                    progress=round(len(completed_agents) / len(agents) * 100),
                )
                logger.info(
                    "Agent output persisted: campaign_id=%s run_id=%s agent=%s progress=%d%%",
                    campaign_id,
                    run_id,
                    agent_name,
                    round(len(completed_agents) / len(agents) * 100),
                )

        now = datetime.now(timezone.utc).isoformat()
        _update_run(
            token,
            run_id,
            status_value="completed",
            current_agent=None,
            progress=100,
            completed_at=now,
        )
        campaign_update = _supabase_request(
            "PATCH",
            f"/rest/v1/campaigns?id=eq.{campaign_id}",
            token,
            body={"status": "completed", "failure_details": None},
        )
        if campaign_update.status_code >= 400:
            raise RuntimeError("Unable to mark campaign completed")
        logger.info("Campaign pipeline completed: campaign_id=%s run_id=%s", campaign_id, run_id)
    except Exception as exc:
        error_details = _pipeline_error_details(exc)
        logger.exception("Campaign pipeline failed: campaign_id=%s run_id=%s", campaign_id, run_id)
        try:
            _update_run(
                token,
                run_id,
                status_value="failed",
                error_details=error_details,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )
            _supabase_request(
                "PATCH",
                f"/rest/v1/campaigns?id=eq.{campaign_id}",
                token,
                body={"status": "failed", "failure_details": error_details},
            )
        except (requests.RequestException, RuntimeError):
            pass


def _require_user(
    authorization: Annotated[str | None, Header()] = None,
) -> tuple[str, UUID]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
        )

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
        )

    try:
        response = requests.get(
            f"{_setting('SUPABASE_URL').rstrip('/')}/auth/v1/user",
            headers={
                "apikey": _setting("SUPABASE_ANON_KEY"),
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )
    except ConfigurationError as exc:
        raise _configuration_http_error(exc) from exc
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        ) from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired bearer token",
        )

    try:
        user_id = UUID(response.json()["id"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service returned an invalid user",
        ) from exc
    return token, user_id


app = FastAPI(title="Campaign Strategist API", version="0.1.0")
app.mount(
    "/media",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "media")),
    name="media",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGINS", "http://localhost:3000"
        ).split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, Any]:
    configured = {
        "supabase": bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_ANON_KEY")),
        "ollama": os.getenv("AI_PROVIDER", "ollama").lower() == "ollama",
        "tavily": os.getenv("RESEARCH_MODE", "offline").lower() == "tavily"
        and bool(os.getenv("TAVILY_API_KEY")),
        "image_generation": os.getenv("VISUAL_MODE", "fixture").lower() == "cloudflare"
        and bool(os.getenv("CLOUDFLARE_WORKER_URL")),
        "offline_research": os.getenv("RESEARCH_MODE", "offline").lower() == "offline",
        "fixture_visuals": os.getenv("VISUAL_MODE", "fixture").lower() == "fixture",
    }
    return {
        "status": "ok",
        "configured": configured,
        "provider": os.getenv("AI_PROVIDER", "ollama").lower(),
    }


@app.post("/campaigns", response_model=Campaign, status_code=status.HTTP_201_CREATED)
def create_campaign(
    payload: CampaignCreate,
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> Campaign:
    token, user_id = auth
    response = _supabase_request(
        "POST",
        "/rest/v1/campaigns",
        token,
        body={**payload.model_dump(), "owner_id": str(user_id)},
    )
    rows = _require_storage(response, "Campaign storage request failed")
    if not rows:
        raise HTTPException(status_code=502, detail="Campaign storage returned no record")
    return Campaign.model_validate(rows[0])


@app.get("/campaigns", response_model=list[Campaign])
def list_campaigns(
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> list[Campaign]:
    token, user_id = auth
    response = _supabase_request(
        "GET",
        f"/rest/v1/campaigns?owner_id=eq.{user_id}&order=created_at.desc",
        token,
    )
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail="Campaign storage request failed")
    return [Campaign.model_validate(row) for row in response.json()]


@app.get("/campaigns/{campaign_id}", response_model=Campaign)
def get_campaign(
    campaign_id: UUID,
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> Campaign:
    token, _ = auth
    response = _supabase_request(
        "GET",
        f"/rest/v1/campaigns?id=eq.{campaign_id}&limit=1",
        token,
    )
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail="Campaign storage request failed")
    rows = response.json()
    if not rows:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return Campaign.model_validate(rows[0])


@app.patch("/campaigns/{campaign_id}", response_model=Campaign)
def update_campaign(
    campaign_id: UUID,
    payload: CampaignUpdate,
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> Campaign:
    token, _ = auth
    fields = payload.model_dump(exclude_unset=True)
    if not fields:
        return get_campaign(campaign_id, auth)
    response = _supabase_request(
        "PATCH",
        f"/rest/v1/campaigns?id=eq.{campaign_id}",
        token,
        body=fields,
    )
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail="Campaign storage request failed")
    rows = response.json()
    if not rows:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return Campaign.model_validate(rows[0])


@app.delete("/campaigns/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    campaign_id: UUID,
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> None:
    token, _ = auth
    response = _supabase_request(
        "DELETE",
        f"/rest/v1/campaigns?id=eq.{campaign_id}",
        token,
    )
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail="Campaign storage request failed")
    if response.status_code == 200 and response.json():
        return
    if response.status_code in (204, 200):
        return
    raise HTTPException(status_code=404, detail="Campaign not found")


@app.post(
    "/campaigns/{campaign_id}/runs",
    response_model=CampaignRun,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_campaign_run(
    campaign_id: UUID,
    background_tasks: BackgroundTasks,
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> CampaignRun:
    token, _ = auth
    logger.info("Campaign run requested: campaign_id=%s", campaign_id)
    campaign_response = _supabase_request(
        "GET",
        f"/rest/v1/campaigns?id=eq.{campaign_id}&limit=1",
        token,
    )
    campaigns = _require_storage(campaign_response, "Campaign storage request failed")
    if not campaigns:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign = campaigns[0]
    active_response = _supabase_request(
        "GET",
        f"/rest/v1/campaign_runs?campaign_id=eq.{campaign_id}&status=in.(queued,running)&limit=1",
        token,
    )
    active_runs = _require_storage(active_response, "Run storage request failed")
    if active_runs:
        logger.info("Reusing active campaign run: campaign_id=%s run_id=%s", campaign_id, active_runs[0]["id"])
        return CampaignRun.model_validate(active_runs[0])

    run_response = _supabase_request(
        "POST",
        "/rest/v1/campaign_runs",
        token,
        body={"campaign_id": str(campaign_id), "status": "queued"},
    )
    runs = _require_storage(run_response, "Unable to create campaign run")
    if not runs:
        raise HTTPException(status_code=502, detail="Run storage returned no record")
    run = CampaignRun.model_validate(runs[0])
    logger.info("Campaign run queued: campaign_id=%s run_id=%s", campaign_id, run.id)
    campaign_update = _supabase_request(
        "PATCH",
        f"/rest/v1/campaigns?id=eq.{campaign_id}",
        token,
        body={"status": "queued", "failure_details": None},
    )
    if campaign_update.status_code >= 400:
        raise HTTPException(status_code=502, detail="Unable to queue campaign")
    background_tasks.add_task(
        _run_pipeline,
        token,
        run.id,
        campaign_id,
        campaign["brief"],
        campaign.get("brand_context"),
        campaign.get("market_context"),
    )
    logger.info("Background campaign worker scheduled: campaign_id=%s run_id=%s", campaign_id, run.id)
    return run


@app.get("/campaigns/{campaign_id}/runs", response_model=list[CampaignRun])
def list_campaign_runs(
    campaign_id: UUID,
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> list[CampaignRun]:
    token, _ = auth
    response = _supabase_request(
        "GET",
        f"/rest/v1/campaign_runs?campaign_id=eq.{campaign_id}&order=created_at.desc",
        token,
    )
    runs = _require_storage(response, "Run storage request failed")
    return [CampaignRun.model_validate(run) for run in runs]


@app.get("/campaigns/{campaign_id}/runs/{run_id}", response_model=CampaignRun)
def get_campaign_run(
    campaign_id: UUID,
    run_id: UUID,
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> CampaignRun:
    token, _ = auth
    response = _supabase_request(
        "GET",
        f"/rest/v1/campaign_runs?id=eq.{run_id}&campaign_id=eq.{campaign_id}&limit=1",
        token,
    )
    runs = _require_storage(response, "Run storage request failed")
    if not runs:
        raise HTTPException(status_code=404, detail="Campaign run not found")
    return CampaignRun.model_validate(runs[0])


@app.get("/campaigns/{campaign_id}/outputs", response_model=list[CampaignOutput])
def get_campaign_outputs(
    campaign_id: UUID,
    auth: Annotated[tuple[str, UUID], Depends(_require_user)],
) -> list[CampaignOutput]:
    token, _ = auth
    runs_response = _supabase_request(
        "GET",
        f"/rest/v1/campaign_runs?campaign_id=eq.{campaign_id}&select=id",
        token,
    )
    runs = _require_storage(runs_response, "Run storage request failed")
    if not runs:
        return []
    run_ids = ",".join(str(run["id"]) for run in runs)
    response = _supabase_request(
        "GET",
        f"/rest/v1/campaign_outputs?run_id=in.({run_ids})&order=created_at.asc",
        token,
    )
    outputs = _require_storage(response, "Output storage request failed")
    return [CampaignOutput.model_validate(output) for output in outputs]
