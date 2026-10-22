## Local API

Install dependencies and start the FastAPI server from this directory:

```bash
uv sync
uv run uvicorn api:app --reload
```

The API is available at `http://localhost:8000`. `GET /health` reports
configuration status without returning secret values. Campaign endpoints
require a Supabase access token:

The local prototype streams model message chunks to the backend terminal, and
logs pipeline progress. During a run, watch for:

```text
--- research Ollama output ---
...live model output...
[research] token stream ended
LLM response received: agent=research duration_ms=...
Agent output persisted: ... progress=20%
```

The stream is for local demo visibility only and is not stored in Supabase.
When a local Ollama model returns JSON text instead of LangGraph's parsed
`structured_response` event, the demo adapter parses the streamed top-level
JSON object and continues the pipeline. It logs this as
`Using streamed JSON fallback`.
Set `LOG_LEVEL=DEBUG` for additional framework logs, or leave the default
`INFO` level for the campaign/LLM lifecycle logs.

```bash
curl http://localhost:8000/health
curl -H "Authorization: Bearer <supabase-access-token>" \
  http://localhost:8000/campaigns
```

Start a campaign run with `POST /campaigns/{campaign_id}/runs`, then poll
`GET /campaigns/{campaign_id}/runs` or
`GET /campaigns/{campaign_id}/runs/{run_id}`. Agent outputs are available from
`GET /campaigns/{campaign_id}/outputs` as they are persisted.

Copy `.env_example` to `.env` and provide the Supabase URL and publishable
key before using campaign endpoints. The CLI smoke test remains available:

```bash
uv run python main.py
```

### Offline demo mode

The default local configuration avoids optional external integrations:

- `AI_PROVIDER=ollama` with `OLLAMA_MODEL=gemma4:12b`
- `RESEARCH_MODE=offline` (the research agent records research gaps instead of calling Tavily)
- `VISUAL_MODE=fixture` (the visual agent uses images already in `backend/media/campaigns`)

After starting Ollama and pulling the model, verify all five agents and the
fixture image path without running the pipeline:

```bash
uv run python smoke_test.py
```

Set `RESEARCH_MODE=tavily` and `VISUAL_MODE=cloudflare` only when the
corresponding credentials and services are available.

Gemini uses the `GEMINI_API_KEY` and `GEMINI_MODEL` settings, but free-tier
quota is shared by the Google project. If a run reports `Gemini API quota
exceeded`, use `AI_PROVIDER=ollama` for the local demo or enable billing/
quota in Google AI Studio before retrying.