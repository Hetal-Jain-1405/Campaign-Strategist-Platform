"use client";

import { use, useCallback, useEffect, useMemo, useState } from "react";
import { Download, Image as ImageIcon, RefreshCw, Target } from "lucide-react";
import { AppShell } from "@/components/campaign-app";
import {
  getAccessToken,
  getApiUrl,
  getCampaign,
  getCampaignOutputs,
  listCampaignRuns,
  startCampaignRun,
  type Campaign,
  type CampaignOutput,
  type CampaignRun,
} from "@/lib/api";

const tabs = ["Overview", "Strategy", "Research", "Content", "Visuals", "Media Plan"];
const outputForTab: Record<string, CampaignOutput["output_type"] | undefined> = {
  Strategy: "strategy",
  Research: "research",
  Content: "content",
  Visuals: "visuals",
  "Media Plan": "media_plan",
};

type ResultsPageProps = { params: Promise<{ campaignId: string }> };

export default function Results({ params }: ResultsPageProps) {
  const { campaignId } = use(params);
  const [campaign, setCampaign] = useState<Campaign>();
  const [outputs, setOutputs] = useState<CampaignOutput[]>([]);
  const [run, setRun] = useState<CampaignRun>();
  const [activeTab, setActiveTab] = useState("Overview");
  const [error, setError] = useState("");
  const [retrying, setRetrying] = useState(false);
  const token = getAccessToken();

  const load = useCallback(async () => {
    if (!token) {
      setError("Sign in is required to view this campaign.");
      return;
    }
    try {
      const [campaignData, outputData, runs] = await Promise.all([
        getCampaign(token, campaignId),
        getCampaignOutputs(token, campaignId),
        listCampaignRuns(token, campaignId),
      ]);
      setCampaign(campaignData);
      setOutputs(outputData);
      setRun(runs[0]);
      setError("");
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Unable to load campaign results.");
    }
  }, [campaignId, token]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    if (!run || !["queued", "running"].includes(run.status)) return;
    const timer = setInterval(() => void load(), 3000);
    return () => clearInterval(timer);
  }, [load, run]);

  const selectedOutput = useMemo(
    () => outputs.find((output) => output.output_type === outputForTab[activeTab]),
    [activeTab, outputs],
  );

  async function retry() {
    setRetrying(true);
    try {
      const nextRun = await startCampaignRun(token, campaignId);
      setRun(nextRun);
      await load();
    } catch (retryError) {
      setError(retryError instanceof Error ? retryError.message : "Unable to retry campaign.");
    } finally {
      setRetrying(false);
    }
  }

  const title = campaign?.name ?? "Campaign workspace";
  return (
    <AppShell>
      <div className="content-wrap">
        <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
          <div>
            <p className="eyebrow">Campaign workspace</p>
            <h1 className="text-3xl font-bold tracking-[-.04em] text-[#172033]">{title}</h1>
            <p className="mt-2 text-sm text-slate-500">
              {run?.status === "completed" ? "Your persisted campaign intelligence is ready to review." : "Your campaign outputs appear here as the agents finish."}
            </p>
          </div>
          <button className="secondary-button" onClick={() => window.print()}>
            <Download size={15} /> Export campaign
          </button>
        </div>

        <div className="mt-9 flex gap-1 overflow-x-auto border-b border-slate-200">
          {tabs.map((tab) => (
            <button key={tab} onClick={() => setActiveTab(tab)} className={`whitespace-nowrap border-b-2 px-3 py-3 text-xs font-semibold ${activeTab === tab ? "border-[#635bff] text-[#635bff]" : "border-transparent text-slate-400"}`}>
              {tab}
            </button>
          ))}
        </div>

        {error && (
          <div className="mt-6 flex items-center justify-between rounded-xl bg-red-50 p-4 text-sm text-red-700">
            <span>{error}</span>
            {run?.status === "failed" && <button onClick={() => void retry()} disabled={retrying} className="font-semibold underline">{retrying ? "Retrying..." : "Retry run"}</button>}
          </div>
        )}
        {run && ["queued", "running"].includes(run.status) && (
          <div className="mt-6 rounded-xl bg-[#faf9ff] p-4 text-sm text-[#635bff]">
            Agent pipeline {run.progress}% complete{run.current_agent ? ` — ${run.current_agent.replace("_", " ")}` : ""}. This page refreshes automatically.
          </div>
        )}

        {activeTab === "Overview" ? (
          <Overview campaign={campaign} outputs={outputs} run={run} />
        ) : selectedOutput ? (
          <OutputSection output={selectedOutput} />
        ) : (
          <EmptyOutput tab={activeTab} />
        )}
      </div>
    </AppShell>
  );
}

function Overview({ campaign, outputs, run }: { campaign?: Campaign; outputs: CampaignOutput[]; run?: CampaignRun }) {
  return (
    <section className="mt-8 space-y-6">
      <div className="grid gap-5 lg:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
          <div className="flex items-center gap-3"><span className="rounded-xl bg-[#eeecff] p-2 text-[#635bff]"><Target size={18} /></span><div><h2 className="font-bold text-[#172033]">Campaign brief</h2><p className="mt-1 text-xs text-slate-400">The context provided to your AI team</p></div></div>
          <p className="mt-5 whitespace-pre-wrap text-sm leading-6 text-slate-600">{campaign?.brief ?? "Loading brief..."}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="eyebrow">Pipeline status</p><p className="mt-2 text-2xl font-bold capitalize text-[#172033]">{run?.status ?? campaign?.status ?? "Loading"}</p>
          <p className="mt-2 text-sm text-slate-500">{outputs.length} output categories persisted</p>
          <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-[#635bff]" style={{ width: `${run?.progress ?? 0}%` }} /></div>
        </div>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {["strategy", "research", "content", "visuals", "media_plan"].map((type) => {
          const output = outputs.find((item) => item.output_type === type);
          return <div key={type} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-xs font-semibold uppercase tracking-[.08em] text-[#8b5cf6]">{type.replace("_", " ")}</p><p className="mt-3 text-sm text-slate-600">{output ? "Available to review" : "Waiting for agent"}</p></div>;
        })}
      </div>
    </section>
  );
}

function OutputSection({ output }: { output: CampaignOutput }) {
  return <section className="mt-8"><div className="mb-6"><h2 className="text-2xl font-bold capitalize tracking-[-.03em] text-[#172033]">{output.output_type.replace("_", " ")}</h2><p className="mt-2 text-sm text-slate-500">Persisted output from the {output.output_type.replace("_", " ")} agent.</p></div><div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><JsonValue value={output.payload} /></div></section>;
}

function JsonValue({ value, label }: { value: unknown; label?: string }) {
  if (value === null || value === undefined || value === "") return null;
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    const isImage = typeof value === "string" && (value.includes("/media/") || /\.(png|jpg|jpeg|webp)$/i.test(value));
    return <div className="mb-5">{label && <p className="mb-2 text-xs font-semibold uppercase tracking-[.08em] text-[#8b5cf6]">{label.replaceAll("_", " ")}</p>}{isImage ? <div><img src={getApiUrl(String(value))} alt={label ?? "Campaign visual"} className="max-h-96 rounded-xl object-contain" /><p className="mt-2 text-xs text-slate-400">{String(value)}</p></div> : <p className="whitespace-pre-wrap text-sm leading-6 text-slate-600">{String(value)}</p>}</div>;
  }
  if (Array.isArray(value)) return <div className="space-y-4">{value.map((item, index) => <div key={index} className="rounded-xl bg-[#f8fafc] p-4"><JsonValue value={item} /></div>)}</div>;
  if (typeof value === "object") return <div className="space-y-5">{Object.entries(value as Record<string, unknown>).map(([key, item]) => <JsonValue key={key} label={key} value={item} />)}</div>;
  return null;
}

function EmptyOutput({ tab }: { tab: string }) {
  return <div className="mt-8 rounded-2xl border border-dashed border-slate-200 p-10 text-center"><RefreshCw className="mx-auto text-slate-300" size={24} /><p className="mt-3 font-semibold text-[#172033]">No {tab.toLowerCase()} output yet</p><p className="mt-2 text-sm text-slate-500">This section will populate when the corresponding agent completes.</p></div>;
}
