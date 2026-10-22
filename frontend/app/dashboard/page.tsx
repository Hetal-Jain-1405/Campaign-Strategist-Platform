"use client";
import { useMemo, useState } from "react";
import {
  ArrowUpRight,
  Check,
  Clock3,
  FolderKanban,
  Plus,
  Search,
  Sparkles,
  Target,
} from "lucide-react";
import Link from "next/link";
import { AppShell, SectionTitle } from "@/components/campaign-app";
import { demoCampaigns } from "@/lib/api";
export default function Dashboard() {
  const [q, setQ] = useState("");
  const [filter, setFilter] = useState("All");
  const items = useMemo(
    () =>
      demoCampaigns.filter(
        (c) =>
          (filter === "All" || c.status === filter) &&
          `${c.title} ${c.brief}`.toLowerCase().includes(q.toLowerCase()),
      ),
    [q, filter],
  );
  return (
    <AppShell>
      <div className="content-wrap">
        <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
          <SectionTitle
            eyebrow="Tuesday, June 18, 2024"
            title="Good morning, Alex"
            description="Your next great campaign starts here."
          />
          <Link href="/campaigns/new" className="primary-button">
            <Plus size={17} /> Create campaign
          </Link>
        </div>
        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon purple">
              <FolderKanban size={17} />
            </div>
            <p>Total campaigns</p>
            <strong>12</strong>
            <span className="stat-note positive">↑ 3 this month</span>
          </div>
          <div className="stat-card">
            <div className="stat-icon green">
              <Check size={17} />
            </div>
            <p>Completed</p>
            <strong>8</strong>
            <span className="stat-note">67% of total</span>
          </div>
          <div className="stat-card">
            <div className="stat-icon amber">
              <Clock3 size={17} />
            </div>
            <p>In progress</p>
            <strong>2</strong>
            <span className="stat-note">2 drafts waiting</span>
          </div>
          <div className="stat-card">
            <div className="stat-icon blue">
              <Sparkles size={17} />
            </div>
            <p>Last campaign</p>
            <strong>Jun 14</strong>
            <span className="stat-note">Summer at Daylight</span>
          </div>
        </section>
        <section className="library-section">
          <div className="library-heading">
            <div>
              <h2>Your campaigns</h2>
              <p>Explore, refine, and bring your best ideas to life.</p>
            </div>
            <Link href="/campaigns/new" className="text-button">
              New brief <ArrowUpRight size={15} />
            </Link>
          </div>
          <div className="toolbar">
            <div className="search-wrap">
              <Search size={16} />
              <input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="Search campaigns..."
                aria-label="Search campaigns"
              />
            </div>
            <div className="filter-pills">
              {["All", "Completed", "In progress", "Draft"].map((x) => (
                <button
                  key={x}
                  onClick={() => setFilter(x)}
                  className={filter === x ? "filter-active" : ""}
                >
                  {x}
                </button>
              ))}
            </div>
          </div>
          <div className="campaign-grid">
            {items.map((c, i) => (
              <Link
                href={`/campaigns/${c.id}/results`}
                key={c.id}
                className="campaign-card"
              >
                <div
                  className={`campaign-art bg-gradient-to-br ${["from-violet-200 via-fuchsia-100 to-amber-100", "from-sky-100 via-cyan-50 to-emerald-100", "from-lime-100 via-emerald-50 to-yellow-100"][i]}`}
                >
                  <div className="relative z-10 flex h-full items-center justify-center">
                    <Target
                      size={35}
                      strokeWidth={1.35}
                      className="text-[#635BFF]/75"
                    />
                  </div>
                </div>
                <div className="p-4">
                  <div className="mb-2 flex items-start justify-between gap-2">
                    <h3 className="text-[14px] font-semibold text-[#172033]">
                      {c.title}
                    </h3>
                    <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] text-emerald-700">
                      {c.status}
                    </span>
                  </div>
                  <p className="mb-4 line-clamp-2 min-h-[38px] text-[12px] leading-[1.55] text-slate-500">
                    {c.brief}
                  </p>
                  <div className="flex justify-between border-t border-slate-100 pt-3 text-[11px] text-slate-400">
                    <span>{c.date}</span>
                    <span className="flex items-center gap-1">
                      <Target size={12} />
                      {c.objective}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </AppShell>
  );
}
