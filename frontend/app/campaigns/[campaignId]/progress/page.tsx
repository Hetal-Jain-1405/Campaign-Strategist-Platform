"use client";

import { use, useEffect, useState } from "react";
import { Check, Circle, LoaderCircle, RefreshCw, Sparkles } from "lucide-react";
import { AppShell } from "@/components/campaign-app";
import {
  getAccessToken,
  getCampaignOutputs,
  listCampaignRuns,
  startCampaignRun,
  type CampaignOutput,
  type CampaignRun,
} from "@/lib/api";

const agents = [
  { key: "research_agent", label: "Research", outputType: "research" },
  { key: "strategy_agent", label: "Strategy", outputType: "strategy" },
  { key: "content_agent", label: "Content", outputType: "content" },
  { key: "visual_agent", label: "Creative", outputType: "visuals" },
  { key: "media_planner_agent", label: "Media Planning", outputType: "media_plan" },
];

type ProgressPageProps = {
  params: Promise<{ campaignId: string }>;
};

export default function ProgressPage({ params }: ProgressPageProps) {
  const { campaignId } = use(params);
  const [run, setRun] = useState<CampaignRun | null>(null);
  const [outputs, setOutputs] = useState<CampaignOutput[]>([]);
  const [error, setError] = useState("");
  const [retrying, setRetrying] = useState(false);

  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      setError("Sign in is required to view campaign progress.");
      return;
    }
    let cancelled = false;
    async function poll() {
      try {
        const [runs, campaignOutputs] = await Promise.all([
          listCampaignRuns(token, campaignId),
          getCampaignOutputs(token, campaignId),
        ]);
        const current = runs[0];
        if (!cancelled) {
          if (current) setRun(current);
          setOutputs(campaignOutputs);
        }
      } catch (pollError) {
        if (!cancelled) {
          setError(pollError instanceof Error ? pollError.message : "Unable to load campaign progress.");
        }
      }
    }
    void poll();
    const timer = setInterval(poll, 3000);
    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, [campaignId]);

  async function retryRun() {
    const token = getAccessToken();
    if (!token || retrying) return;
    setRetrying(true);
    setError("");
    try {
      const nextRun = await startCampaignRun(token, campaignId);
      setRun(nextRun);
    } catch (retryError) {
      setError(
        retryError instanceof Error
          ? retryError.message
          : "Unable to retry the campaign.",
      );
    } finally {
      setRetrying(false);
    }
  }

  useEffect(() => {
    if (!run || run.status !== "completed") {
      return;
    }

    const timer = setTimeout(() => {
      window.location.href = `/campaigns/${campaignId}/results`;
    }, 700);

    return () => clearTimeout(timer);
  }, [campaignId, run]);

  const completedAgents = run?.completed_agents.length ?? 0;
  const progressPercent = run?.progress ?? 0;

  return (
    <AppShell>
      <div className="content-wrap max-w-3xl">
        <div className="mb-12 text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-[#eeecff] text-[#635bff]">
            <Sparkles size={25} />
          </div>
          <p className="eyebrow mt-6">Campaign in progress</p>
          <h1 className="text-3xl font-bold tracking-[-.04em] text-[#172033]">
            Your AI campaign team is at work.
          </h1>
          <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-slate-500">
            We&apos;re turning your brief into research, strategy, creative, and
            a plan you can launch.
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-8 flex items-center justify-between text-sm">
            <span className="font-semibold text-slate-700">Agent progress</span>
            <span className="text-slate-400">
              {progressPercent}% · updates every 3s
            </span>
          </div>

          <div className="mb-8 h-2 overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full bg-[#635bff] transition-all duration-500"
              style={{ width: `${progressPercent}%` }}
            />
          </div>

          {error && <p className="mb-4 text-sm text-red-600">{error}</p>}
          {run?.status === "failed" && (
            <div className="mb-4 flex items-center justify-between rounded-xl bg-red-50 p-4 text-sm text-red-700">
              <span>
                This run failed. {run.error_details?.message
                  ? String(run.error_details.message)
                  : "You can retry the campaign."}
              </span>
              <button
                type="button"
                onClick={() => void retryRun()}
                disabled={retrying}
                className="ml-4 inline-flex shrink-0 items-center gap-2 font-semibold"
              >
                <RefreshCw size={14} className={retrying ? "animate-spin" : ""} />
                {retrying ? "Retrying..." : "Retry run"}
              </button>
            </div>
          )}
          <div className="space-y-3">
            {agents.map((agent, index) => {
              const output = outputs.find(
                (item) => item.output_type === agent.outputType,
              );
              const isComplete =
                output !== undefined ||
                run?.completed_agents.includes(agent.key) ||
                index < completedAgents;
              const isRunning =
                !isComplete &&
                (run?.current_agent === agent.key || index === completedAgents);

              return (
                <div
                  key={agent.key}
                  className="flex items-center gap-4 rounded-xl border border-slate-100 p-4"
                >
                  <span
                    className={`flex h-8 w-8 items-center justify-center rounded-full ${
                      isComplete
                        ? "bg-emerald-50 text-emerald-600"
                        : isRunning
                          ? "bg-[#eeecff] text-[#635bff]"
                          : "bg-slate-50 text-slate-300"
                    }`}
                  >
                    {isComplete ? (
                      <Check size={16} />
                    ) : isRunning ? (
                      <LoaderCircle size={16} className="animate-spin" />
                    ) : (
                      <Circle size={15} />
                    )}
                  </span>
                  <div className="min-w-0 flex-1">
                    <span className="block text-sm font-medium text-slate-700">
                      {agent.label} agent
                    </span>
                    {output && <OutputPreview output={output} />}
                  </div>
                  <span className="text-xs text-slate-400">
                    {isComplete
                      ? "Completed"
                      : isRunning
                        ? "Running"
                        : "Pending"}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </AppShell>
  );
}

function OutputPreview({ output }: { output: CampaignOutput }) {
  const payload = output.payload;
  const preview = previewText(payload);
  return (
    <p className="mt-2 line-clamp-2 text-xs leading-5 text-slate-500">
      <span className="font-semibold text-emerald-600">Output ready:</span>{" "}
      {preview}
    </p>
  );
}

function previewText(payload: unknown): string {
  if (typeof payload === "string") return payload;
  if (!payload || typeof payload !== "object") return "Structured output persisted.";
  const record = payload as Record<string, unknown>;
  const preferredKeys = [
    "research_summary",
    "campaign_concept",
    "campaign_objective",
    "campaign_duration",
    "assets",
    "recommended_channels",
    "campaign_phases",
  ];
  for (const key of preferredKeys) {
    const value = record[key];
    if (typeof value === "string") return value;
    if (Array.isArray(value) && value.length > 0) {
      return `${value.length} ${key.replaceAll("_", " ")} generated.`;
    }
  }
  const firstText = Object.values(record).find((value) => typeof value === "string");
  return typeof firstText === "string"
    ? firstText
    : "Structured output persisted.";
}
