# Campaign Strategist Platform — Authoritative Roadmap

Last updated: 2026-10-23

This file is the handoff document for the project. An agent should be able to
understand what works, what does not, and what to do next without reading the
code first.

## Target demo

A local user should be able to:

1. Create an account and sign in with Supabase Auth.
2. Submit a campaign brief plus optional brand and market context.
3. Start the five-agent pipeline.
4. Watch persisted research, strategy, content, visual, and media-planning progress.
5. Refresh the browser and retain the signed-in workspace.
6. Re-open campaigns from a Supabase-backed dashboard.
7. Review completed, partial, failed, and retryable results.

The intended default is a local Ollama text model (`gemma4:12b`) with thinking
disabled. Tavily research and Cloudflare image generation are optional. The
offline demo uses empty research-tool results and checked-in fixture images.

## Executive status

| Area | Status | Meaning |
| --- | --- | --- |
| Supabase schema/RLS/storage | **DONE** | Applied to the configured `campaignAI` project and advisor-checked. |
| Provider abstraction | **DONE** | All five agents use `AI_PROVIDER=ollama|gemini`. |
| Offline integrations | **DONE** | `RESEARCH_MODE=offline` and `VISUAL_MODE=fixture` work without optional services. |
| Backend HTTP API | **DONE** | Health, auth guard, campaign CRUD, run creation, polling, and outputs exist. |
| Background pipeline persistence | **IMPLEMENTED, NEEDS FULL RUN TEST** | Agent transitions and typed JSON outputs are persisted; a real Ollama run still needs verification. |
| Frontend API wiring | **DONE** | Authenticated dashboard, campaign creation, progress polling, and persisted results use the backend. |
| Frontend authentication | **NOT DONE** | Login/signup are still UI-only; no Supabase browser client/session is wired. |
| Dashboard | **DONE** | Loads authenticated campaigns, status filters, counts, empty/loading/error states, and links to workspaces. |
| Results | **DONE** | Polls active runs, renders persisted output categories and fixture image paths, and supports failed-run retry. |
| Frontend build | **DONE** | Builds with pinned pnpm and Next.js 16.4.2. |
| Complete browser demo | **READY FOR LOCAL INTEGRATION RUN** | Code path is wired; local Supabase credentials and Ollama are still required for a real run. |

## What can be run today

### 1. Backend dependency and syntax checks

Requirements: Python 3.12+ and `uv`.

```bash
cd backend
uv sync
uv run python -m compileall -q .
```

### 2. Offline Phase 3 agent smoke test

This constructs all five agents and checks fixture image resolution. It does
not call Ollama, Tavily, Gemini, Cloudflare, or Supabase.

```bash
cd backend
AI_PROVIDER=ollama \
RESEARCH_MODE=offline \
VISUAL_MODE=fixture \
uv run python smoke_test.py
```

Expected output includes:

```text
Configured agents: research, strategy, content, visual, media_planner
Fixture visual: /media/campaigns/<fixture>.png
```

### 3. Backend API locally

Copy `backend/.env_example` to `backend/.env` and set:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `AI_PROVIDER=ollama`
- `OLLAMA_MODEL=gemma4:12b`
- `OLLAMA_BASE_URL=http://localhost:11434`
- `RESEARCH_MODE=offline`
- `VISUAL_MODE=fixture`
- `FRONTEND_ORIGINS=http://localhost:3000`

Then run:

```bash
cd backend
uv run uvicorn api:app --reload
```

Check the non-secret health report:

```bash
curl http://localhost:8000/health
```

Unauthenticated campaign requests should return `401`:

```bash
curl http://localhost:8000/campaigns
```

### 4. Backend API smoke checks

The current focused checks validate compilation, health, fixture media delivery,
and authentication guards:

```bash
cd backend
uv run python -m compileall -q .
uv run python smoke_test.py
```

The complete authenticated API flow cannot be run until a real Supabase access
token is available.

## What cannot be run end-to-end yet

The complete local browser demo is **not available yet**. These are the actual
blocking items, in priority order:

1. **Real local integration run**
   - Configure frontend and backend Supabase environment variables.
   - Start Ollama and pull `gemma4:12b`.
   - Sign up, create one campaign, and verify all five persisted outputs.

2. **Optional backend hardening**
   - Add an authenticated integration test suite.
   - Verify concurrent retry behavior against Supabase.
   - Verify failure recovery after worker/process interruption.

3. **Optional showcase polish**
   - Replace the generic persisted JSON renderer with richer typed presentation cards.
   - Add copy/download actions for individual content assets.

4. **Production worker consideration**
   - Move long jobs from FastAPI `BackgroundTasks` to a durable worker before production use.

5. **Real Ollama pipeline verification**
   - Install Ollama.
   - Pull `gemma4:12b`.
   - Confirm the model supports the structured Pydantic responses used by all
     five agents.
   - Run one complete campaign with offline research and fixture visuals.
   - Verify five output records and final `completed` statuses in Supabase.

## Completed implementation

### Phase 0 — Environment and contracts: DONE

- Supabase project and MCP connection confirmed.
- Backend environment variables documented.
- Campaign, run, output, status, and error contracts added.
- Provider factory added with `AI_PROVIDER=ollama|gemini`.
- Ollama defaults to `gemma4:12b` with `reasoning=False`.
- Gemini remains selectable with `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
- `/health` reports configuration booleans without returning secrets.

### Phase 1 — Supabase foundation: DONE

Applied to project `campaignAI`:

- `profiles` linked to `auth.users`.
- `campaigns` with owner, brief, brand/market context, status, timestamps,
  and failure details.
- `campaign_runs` with current agent, completed agents, progress, timestamps,
  and error details.
- `campaign_outputs` with typed output categories and JSON payloads.
- Private `campaign-images` storage bucket.
- Owner-based RLS for profiles, campaigns, runs, outputs, and image objects.
- Auth user trigger creates a profile.
- Security advisor issue fixed by revoking API execution on the profile trigger.

### Phase 2 — Backend API and jobs: IMPLEMENTED

Implemented in the backend:

- `GET /health`
- `POST /campaigns`
- `GET /campaigns`
- `GET /campaigns/{campaign_id}`
- `PATCH /campaigns/{campaign_id}`
- `DELETE /campaigns/{campaign_id}`
- `POST /campaigns/{campaign_id}/runs`
- `GET /campaigns/{campaign_id}/runs`
- `GET /campaigns/{campaign_id}/runs/{run_id}`
- `GET /campaigns/{campaign_id}/outputs`
- `GET /media/...` for local fixture/generated media
- CORS for local Next.js.
- Supabase bearer-token validation through `/auth/v1/user`.
- Owner authorization delegated to Supabase RLS and owner filters.
- Background LangGraph execution.
- Per-agent output persistence.
- Queued → running → completed/failed transitions.
- Active-run reuse to avoid duplicate retries.
- Explicit storage, authentication, validation, and pipeline errors.
- CLI smoke-test entry point remains available through `main.py`.

Remaining Phase 2 hardening:

- Add a real authenticated integration test suite.
- Verify concurrent retry behavior against Supabase.
- Verify failure recovery after worker/process interruption.
- Consider moving long jobs from FastAPI `BackgroundTasks` to a durable worker
  before production use. This is acceptable for the local prototype.

### Phase 3 — Ollama and offline integrations: IMPLEMENTED, NEEDS FULL RUN

Implemented:

- All five agents use the provider factory.
- Research tool is independent of the text provider.
- `RESEARCH_MODE=offline|tavily`.
- `VISUAL_MODE=fixture|cloudflare`.
- Fixture visuals are selected from `backend/media/campaigns`.
- Cloudflare credentials are only required in `cloudflare` mode.
- `backend/smoke_test.py` constructs all five agents and checks a fixture.

Remaining:

- Run the full five-agent pipeline with Ollama and validate every Pydantic
  output against its schema.
- Improve offline research output so the final report explicitly records
  research gaps rather than relying only on model behavior.
- Verify media-plan output references only persisted content and visual assets.

## Phase 4 — Frontend integration: PARTIAL

Already wired:

- Supabase browser client, real email/password auth, session restoration, and sign-out.
- Protected application shell and backend access-token handoff.
- Typed frontend API client for campaigns, runs, and outputs.
- New-campaign form submits name, brief, brand context, and market context.
- New campaign calls the backend and starts a real run.
- Progress page polls persisted backend run state.
- Dashboard loads campaigns and real status counts with loading, empty, and error states.
- Results page polls runs, renders persisted outputs, renders fixture visuals, and retries failures.

Still required for a completed real run:

1. Configure frontend `.env.example` values locally.
2. Run one campaign with Ollama and verify all five output categories.
3. Add frontend `.env.example` documenting:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Keep frontend dependencies installed and passing `pnpm build`.

## Phase 5 — Showcase polish and reliability: NOT STARTED

Required after Phase 4:

- Scannable executive summary, strategy, content cards, visual gallery, and
  media-plan timeline.
- Copy/download actions.
- Stable image delivery for both fixture and generated images.
- Documented seed path instead of hard-coded dashboard campaigns.
- Backend tests for auth, ownership, run transitions, provider selection, and
  serialization.
- Frontend checks for auth redirects, campaign creation, progress, and results.
- One clean-machine runbook covering Ollama, Supabase, environment, and start
  commands.

## Exact definition of “complete local demo”

Do not mark the project demo-ready until all of the following are true:

- `uv run python smoke_test.py` passes.
- Ollama is running with `gemma4:12b`.
- A real user can sign up and sign in through the browser.
- Refreshing the browser preserves the session.
- A user can create a campaign from the UI.
- The backend creates exactly one active run for a retry.
- The UI polls real persisted progress.
- All five output categories appear in Supabase.
- Results render persisted data rather than demo constants.
- Fixture images render in the results page.
- Failed runs show an error and can be retried.
- A second user cannot read or mutate the first user’s campaigns.
- `pnpm build` passes.
- A clean-machine runbook completes the flow without manual database edits.

## Recommended next execution order

1. Install/enable `pnpm` and verify the frontend build baseline.
2. Add Supabase browser client, real login/signup, session restoration, and
   route protection.
3. Replace dashboard demo data with authenticated API data.
4. Replace result demo data with persisted API outputs.
5. Add frontend failure/loading/retry states.
6. Run a complete Ollama campaign with offline research and fixture visuals.
7. Add authenticated backend and frontend regression tests.
8. Write and execute the clean-machine local runbook.
9. Only then mark Phase 3/4/5 and the showcase outcome complete.

## Deliberate non-goals

- Production deployment and autoscaling.
- Team collaboration and role-based permissions.
- Billing, quotas, and usage metering.
- Fine-grained agent editing/approval workflows.
- Replacing image generation with Ollama.
