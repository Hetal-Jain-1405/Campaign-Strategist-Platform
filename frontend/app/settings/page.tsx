"use client";
import { useState } from "react";
import { AppShell, SectionTitle } from "@/components/campaign-app";
export default function SettingsPage() {
  const [saved, setSaved] = useState(false);
  return (
    <AppShell>
      <div className="content-wrap max-w-3xl">
        <SectionTitle
          eyebrow="Manage"
          title="Settings"
          description="Keep your workspace profile and preferences up to date."
        />
        <div className="mt-8 space-y-5">
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="font-bold text-[#172033]">Profile</h2>
            <div className="mt-5 grid gap-5 sm:grid-cols-2">
              <label className="field-label">
                Full name
                <input className="form-input mt-2" defaultValue="Alex Morgan" />
              </label>
              <label className="field-label">
                Email address
                <input
                  className="form-input mt-2"
                  defaultValue="alex@northstar.co"
                  type="email"
                />
              </label>
            </div>
          </section>
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="font-bold text-[#172033]">Workspace preferences</h2>
            <label className="mt-5 flex items-center justify-between gap-4 text-sm text-slate-600">
              Weekly campaign digest
              <input
                type="checkbox"
                defaultChecked
                className="h-4 w-4 accent-[#635bff]"
              />
            </label>
            <label className="mt-5 flex items-center justify-between gap-4 text-sm text-slate-600">
              Agent completion notifications
              <input
                type="checkbox"
                defaultChecked
                className="h-4 w-4 accent-[#635bff]"
              />
            </label>
          </section>
          <div className="flex items-center justify-end gap-4">
            <span className="text-xs text-emerald-600">
              {saved ? "Settings saved" : ""}
            </span>
            <button onClick={() => setSaved(true)} className="primary-button">
              Save changes
            </button>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
