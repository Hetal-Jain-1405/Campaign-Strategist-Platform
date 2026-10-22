export type CampaignStatus =
  | "draft"
  | "queued"
  | "running"
  | "completed"
  | "failed";

export type Campaign = {
  id: string;
  owner_id: string;
  name: string;
  brief: string;
  brand_context: string | null;
  market_context: string | null;
  status: CampaignStatus;
  failure_details: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
};

export type CampaignRun = {
  id: string;
  campaign_id: string;
  status: "queued" | "running" | "completed" | "failed";
  current_agent: string | null;
  completed_agents: string[];
  progress: number;
  started_at: string | null;
  completed_at: string | null;
  error_details: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
};

export type CampaignOutput = {
  id: string;
  run_id: string;
  output_type: "research" | "strategy" | "content" | "visuals" | "media_plan";
  payload: unknown;
  created_at: string;
  updated_at: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function getApiUrl(path: string): string {
  return `${API_URL}${path}`;
}

export type DemoCampaign = {
  id: string;
  title: string;
  brief: string;
  status: "Completed" | "In progress" | "Draft";
  date: string;
  objective: string;
};

export const demoCampaigns: DemoCampaign[] = [
  {
    id: "daylight",
    title: "Summer at Daylight",
    brief: "A warm, community-first launch for Daylight Coffee seasonal menu.",
    status: "Completed",
    date: "Jun 14, 2024",
    objective: "Brand awareness",
  },
  {
    id: "movement",
    title: "Move with intention",
    brief: "Positioning and content system for a mindful movement studio.",
    status: "In progress",
    date: "Jun 11, 2024",
    objective: "Drive sign-ups",
  },
  {
    id: "growing",
    title: "Good things, growing",
    brief: "An optimistic brand campaign for a new generation of home gardeners.",
    status: "Completed",
    date: "Jun 05, 2024",
    objective: "Product launch",
  },
];

export function getAccessToken(): string {
  if (typeof window === "undefined") return "";
  return window.localStorage.getItem("campaign-access-token") ?? "";
}

async function request<T>(
  path: string,
  accessToken: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...init?.headers,
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail =
      body && typeof body.detail === "string"
        ? body.detail
        : "The campaign service request failed.";
    throw new Error(detail);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export function listCampaigns(accessToken: string): Promise<Campaign[]> {
  return request<Campaign[]>("/campaigns", accessToken);
}

export function createCampaign(
  accessToken: string,
  input: {
    name: string;
    brief: string;
    brand_context?: string;
    market_context?: string;
  },
): Promise<Campaign> {
  return request<Campaign>("/campaigns", accessToken, {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function getCampaign(
  accessToken: string,
  campaignId: string,
): Promise<Campaign> {
  return request<Campaign>(`/campaigns/${campaignId}`, accessToken);
}

export function startCampaignRun(
  accessToken: string,
  campaignId: string,
): Promise<CampaignRun> {
  return request<CampaignRun>(`/campaigns/${campaignId}/runs`, accessToken, {
    method: "POST",
  });
}

export function getCampaignRun(
  accessToken: string,
  campaignId: string,
  runId: string,
): Promise<CampaignRun> {
  return request<CampaignRun>(
    `/campaigns/${campaignId}/runs/${runId}`,
    accessToken,
  );
}

export function listCampaignRuns(
  accessToken: string,
  campaignId: string,
): Promise<CampaignRun[]> {
  return request<CampaignRun[]>(`/campaigns/${campaignId}/runs`, accessToken);
}

export function getCampaignOutputs(
  accessToken: string,
  campaignId: string,
): Promise<CampaignOutput[]> {
  return request<CampaignOutput[]>(
    `/campaigns/${campaignId}/outputs`,
    accessToken,
  );
}
