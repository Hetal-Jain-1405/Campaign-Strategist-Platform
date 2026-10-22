"use client";

import { use, useEffect, useState } from "react";
import { Check, Circle, LoaderCircle, Sparkles } from "lucide-react";
import { AppShell } from "@/components/campaign-app";

const agents = [
  "Research",
  "Strategy",
  "Content",
  "Creative",
  "Media Planning",
  "Validation",
];

const AGENT_DURATION_MS = 20 * 1000;

type ProgressPageProps = {
  params: Promise<{ campaignId: string }>;
};

export default function ProgressPage({ params }: ProgressPageProps) {
  const { campaignId } = use(params);
  const [completedAgents, setCompletedAgents] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCompletedAgents((current) =>
        current < agents.length ? current + 1 : current,
      );
    }, AGENT_DURATION_MS);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (completedAgents !== agents.length) {
      return;
    }

    const timer = setTimeout(() => {
      window.location.href = `/campaigns/${campaignId}/results`;
    }, 700);

    return () => clearTimeout(timer);
  }, [campaignId, completedAgents]);

  const progressPercent = Math.round((completedAgents / agents.length) * 100);

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
            <span className="text-slate-400">{progressPercent}%</span>
          </div>

          <div className="mb-8 h-2 overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full bg-[#635bff] transition-all duration-500"
              style={{ width: `${progressPercent}%` }}
            />
          </div>

          <div className="space-y-3">
            {agents.map((agent, index) => {
              const isComplete = index < completedAgents;
              const isRunning = index === completedAgents;

              return (
                <div
                  key={agent}
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
                  <span className="flex-1 text-sm font-medium text-slate-700">
                    {agent} agent
                  </span>
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
