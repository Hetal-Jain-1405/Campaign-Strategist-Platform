"use client";
import { useState } from "react";
import { ArrowLeft, ChevronDown, Sparkles } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppShell, SectionTitle } from "@/components/campaign-app";
import { createCampaign, getAccessToken, startCampaignRun } from "@/lib/api";
export default function NewCampaign() {
  const router = useRouter();
  const [brief, setBrief] = useState("");
  const [name, setName] = useState("New campaign");
  const [brandContext, setBrandContext] = useState("");
  const [marketContext, setMarketContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!brief.trim() || loading) return;

    setLoading(true);
    setError("");

    try {
      const accessToken = getAccessToken();
      if (!accessToken) {
        throw new Error("Sign in is required before creating a campaign.");
      }
      const campaign = await createCampaign(accessToken, {
        name: name.trim() || "New campaign",
        brief: brief.trim(),
        brand_context: brandContext.trim() || undefined,
        market_context: marketContext.trim() || undefined,
      });
      await startCampaignRun(accessToken, campaign.id);
      router.push(`/campaigns/${campaign.id}/progress`);
    } catch (submissionError) {
      setLoading(false);
      setError(
        submissionError instanceof Error
          ? submissionError.message
          : "We could not start the campaign. Please try again.",
      );
    }
  }
  return (
    <AppShell>
      <div className="content-wrap max-w-4xl">
        <Link
          href="/dashboard"
          className="mb-8 flex items-center gap-2 text-xs text-slate-500"
        >
          <ArrowLeft size={14} /> Back to campaigns
        </Link>
        <SectionTitle
          eyebrow="New campaign"
          title="What are we building?"
          description="Give your AI team the context it needs to create something remarkable."
        />
        <form
          onSubmit={submit}
          className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-9"
        >
          <label className="field-label" htmlFor="brief">
            Campaign brief
          </label>
          <input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="form-input mb-4"
            placeholder="Campaign name"
            required
          />
          <textarea
            id="brief"
            value={brief}
            onChange={(e) => setBrief(e.target.value)}
            className="brief-input"
            placeholder="For Environment Day, I want to create a campaign for my coffee shop that attracts Gen Z college students..."
            required
          />
          <div className="mt-7 border-t border-slate-100 pt-6">
            <details>
              <summary className="flex cursor-pointer list-none items-center justify-between text-sm font-semibold text-slate-700">
                Advanced settings <ChevronDown size={16} />
              </summary>
              <div className="mt-5 grid gap-4 sm:grid-cols-2">
                <input
                  className="form-input"
                  placeholder="Brand or company name"
                  value={brandContext}
                  onChange={(e) => setBrandContext(e.target.value)}
                />
                <input
                  className="form-input"
                  placeholder="Primary market"
                  value={marketContext}
                  onChange={(e) => setMarketContext(e.target.value)}
                />
              </div>
            </details>
          </div>
          <div className="mt-8 flex justify-end">
            <button type="submit" disabled={loading} className="primary-button">
              {loading ? (
                "Starting your AI team..."
              ) : (
                <>
                  <Sparkles size={16} /> Generate campaign
                </>
              )}
            </button>
          </div>
          {error && (
            <p className="mt-4 text-right text-xs text-red-600">{error}</p>
          )}
        </form>
      </div>
    </AppShell>
  );
}
