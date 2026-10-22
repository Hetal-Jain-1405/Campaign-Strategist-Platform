"use client";

import { use, useEffect, useState } from "react";
import {
  Copy,
  Camera,
  Download,
  Image as ImageIcon,
  Maximize2,
  Target,
  X,
} from "lucide-react";
import { AppShell } from "@/components/campaign-app";
import { getCampaign, type Campaign } from "@/lib/api";
import { campaignResponse } from "@/lib/campaign-response";

const tabs = [
  "Overview",
  "Strategy",
  "Research",
  "Content Assets",
  "Visual Assets",
  "Media Plan",
];

const campaignAssets = [
  {
    id: "campaign-visual-01",
    label: "Campaign Visual 01",
    title: "Coffee, community, and a reason to gather",
    platform: "Instagram",
    aspectRatio: "1:1",
    description:
      "A stylish reusable iced coffee tumbler filled with an iced oat latte on a sunlit campus study desk with notebooks and greenery.",
    sourceContentReference: "Your daily iced latte shouldn't cost the earth.",
    imageUrl: "/campaign-assets/campaign-visual-01.png",
  },
  {
    id: "campaign-visual-02",
    label: "Campaign Visual 02",
    title: "A warm moment worth sharing",
    platform: "TikTok",
    aspectRatio: "9:16",
    description:
      "A vibrant and modern eco-friendly campus coffee bar showcasing reusable tumblers, cold brew decanters, and lush plants.",
    sourceContentReference:
      "POV: You found the campus coffee spot that actually matches your eco-values.",
    imageUrl: "/campaign-assets/campaign-visual-02.png",
  },
  {
    id: "campaign-visual-03",
    label: "Campaign Visual 03",
    title: "Make space for good ideas",
    platform: "Blog",
    aspectRatio: "16:9",
    description:
      "A minimalist editorial flat lay featuring a reusable ceramic travel mug, organic coffee beans, a journal, and botanical foliage.",
    sourceContentReference:
      "Beyond the Cup: How College Students Can Sip More Sustainably",
    imageUrl: "/campaign-assets/campaign-visual-03.png",
  },
];

type CampaignAsset = (typeof campaignAssets)[number];

type ResultsPageProps = {
  params: Promise<{ campaignId: string }>;
};

export default function Results({ params }: ResultsPageProps) {
  const { campaignId } = use(params);
  const [activeTab, setActiveTab] = useState("Overview");
  const [campaign, setCampaign] = useState<Campaign>();
  const [previewAsset, setPreviewAsset] = useState<CampaignAsset>();

  useEffect(() => {
    setCampaign(getCampaign(campaignId));
  }, [campaignId]);

  const campaignTitle = campaign?.title ?? "Your new campaign";
  const campaignBrief =
    campaign?.brief ?? "Your campaign brief is being prepared.";

  return (
    <AppShell>
      <div className="content-wrap">
        <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
          <div>
            <p className="eyebrow">Campaign workspace</p>
            <h1 className="text-3xl font-bold tracking-[-.04em] text-[#172033]">
              {campaignTitle}
            </h1>
            <p className="mt-2 text-sm text-slate-500">
              Your AI-generated campaign strategy is ready to review.
            </p>
          </div>
          <button className="secondary-button">
            <Download size={15} /> Export campaign
          </button>
        </div>

        <div className="mt-9 flex gap-1 overflow-x-auto border-b border-slate-200">
          {tabs.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`whitespace-nowrap border-b-2 px-3 py-3 text-xs font-semibold ${
                activeTab === tab
                  ? "border-[#635bff] text-[#635bff]"
                  : "border-transparent text-slate-400"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeTab === "Overview" ? (
          <OverviewSection
            onPreview={setPreviewAsset}
            campaignTitle={campaignTitle}
            campaignBrief={campaignBrief}
          />
        ) : activeTab === "Visual Assets" ? (
          <VisualAssetsSection onPreview={setPreviewAsset} />
        ) : activeTab === "Strategy" ? (
          <StrategySection />
        ) : activeTab === "Research" ? (
          <ResearchSection />
        ) : activeTab === "Content Assets" ? (
          <ContentAssetsSection />
        ) : activeTab === "Media Plan" ? (
          <MediaPlanSection />
        ) : (
          <AgentEmptyState tab={activeTab} description="No data available." />
        )}
      </div>

      {previewAsset && (
        <ImagePreview
          asset={previewAsset}
          onClose={() => setPreviewAsset(undefined)}
        />
      )}
    </AppShell>
  );
}

function OverviewSection({
  campaignTitle,
  campaignBrief,
  onPreview,
}: {
  campaignTitle: string;
  campaignBrief: string;
  onPreview: (asset: CampaignAsset) => void;
}) {
  return (
    <section className="mt-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold tracking-[-.03em] text-[#172033]">
          Campaign Overview
        </h2>
        <p className="mt-2 text-sm text-slate-500">
          Your campaign at a glance — explore the visuals created for your
          campaign.
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-3">
        {campaignAssets.map((asset) => (
          <AssetCard key={asset.id} asset={asset} onPreview={onPreview} />
        ))}
      </div>

      <div className="mt-6 grid gap-5 lg:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
          <div className="flex items-center gap-3">
            <span className="rounded-xl bg-[#eeecff] p-2 text-[#635bff]">
              <Target size={18} />
            </span>
            <div>
              <h3 className="font-bold text-[#172033]">Campaign direction</h3>
              <p className="mt-1 text-xs text-slate-400">
                Generated campaign intelligence
              </p>
            </div>
          </div>
          <p className="mt-5 text-sm leading-6 text-slate-600">
            {campaignTitle} is ready to review across its strategy, content,
            visual assets, and media plan.
          </p>
          <div className="mt-6 border-t border-slate-100 pt-5">
            <p className="text-xs font-semibold uppercase tracking-[.08em] text-[#8b5cf6]">
              Campaign brief
            </p>
            <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-700">
              {campaignBrief}
            </p>
          </div>
        </div>

        <CampaignSnapshot campaignTitle={campaignTitle} />
      </div>
    </section>
  );
}

function VisualAssetsSection({
  onPreview,
}: {
  onPreview: (asset: CampaignAsset) => void;
}) {
  return (
    <section className="mt-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold tracking-[-.03em] text-[#172033]">
          Visual Assets
        </h2>
        <p className="mt-2 text-sm text-slate-500">
          Review the generated images and visual creatives for each platform.
        </p>
      </div>

      <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
        {campaignAssets.map((asset) => (
          <AssetCard key={asset.id} asset={asset} onPreview={onPreview} />
        ))}
      </div>
    </section>
  );
}

function StrategySection() {
  const strategy = campaignResponse.strategy_report;

  return (
    <section className="mt-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold tracking-[-.03em] text-[#172033]">
          Strategy
        </h2>
        <p className="mt-2 text-sm text-slate-500">
          Campaign direction and messaging from the Strategy Agent.
        </p>
      </div>

      <div className="space-y-5">
        <div className="rounded-2xl border border-[#c9c4ff] bg-[#faf9ff] p-6 shadow-sm">
          <p className="eyebrow">Campaign concept</p>
          <h3 className="mt-2 text-2xl font-bold text-[#172033]">
            {strategy.campaign_concept}
          </h3>
          <p className="mt-4 text-sm leading-6 text-slate-600">
            {strategy.key_message}
          </p>
        </div>
        <div className="grid gap-5 lg:grid-cols-2">
          <InfoCard title="Objective" text={strategy.campaign_objective} />
          <InfoCard title="Primary audience" text={strategy.primary_audience} />
          <InfoCard
            title="Brand positioning"
            text={strategy.brand_positioning}
          />
          <InfoCard
            title="Unique selling proposition"
            text={strategy.unique_selling_proposition}
          />
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="font-bold text-[#172033]">Messaging pillars</h3>
          <div className="mt-4 grid gap-3 md:grid-cols-3">
            {strategy.messaging_pillars.map((pillar) => (
              <p
                key={pillar}
                className="rounded-xl bg-[#f8fafc] p-4 text-sm leading-6 text-slate-600"
              >
                {pillar}
              </p>
            ))}
          </div>
          <div className="mt-5 flex flex-wrap gap-2">
            {strategy.brand_voice.map((voice) => (
              <span
                key={voice}
                className="rounded-full bg-[#eeecff] px-3 py-1 text-xs font-semibold text-[#635bff]"
              >
                {voice}
              </span>
            ))}
          </div>
          <p className="mt-5 rounded-xl bg-emerald-50 p-4 text-sm font-semibold text-emerald-800">
            Primary CTA: {strategy.primary_cta}
          </p>
        </div>
        <details className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <summary className="cursor-pointer text-sm font-bold text-[#172033]">
            Rationale, assumptions, risks, and information gaps
          </summary>
          <div className="mt-4 space-y-3 text-sm leading-6 text-slate-600">
            <p>{strategy.strategic_rationale}</p>
            <List items={strategy.evidence_and_assumptions} />
            <List items={strategy.risks_and_constraints} />
            <List items={strategy.information_gaps} />
          </div>
        </details>
      </div>
    </section>
  );
}

function InfoCard({ title, text }: { title: string; text: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-[.08em] text-[#8b5cf6]">
        {title}
      </p>
      <p className="mt-3 text-sm leading-6 text-slate-600">{text}</p>
    </div>
  );
}

function List({ items }: { items: readonly string[] }) {
  return (
    <ul className="list-disc space-y-1 pl-5">
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}

function ResearchSection() {
  const research = campaignResponse.research_report;
  return (
    <section className="mt-8 space-y-5">
      <SectionIntro
        title="Research"
        description="Evidence and audience insights from the Research Agent."
      />
      <InfoCard title="Research summary" text={research.research_summary} />
      <div className="grid gap-5 lg:grid-cols-2">
        {research.audience_insights.map((insight) => (
          <div
            key={insight.insight_type}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <p className="eyebrow">{insight.insight_type}</p>
            <p className="mt-2 text-sm leading-6 text-slate-700">
              {insight.description}
            </p>
            <p className="mt-3 text-xs leading-5 text-slate-500">
              {insight.supporting_evidence}
            </p>
            <SourceLinks urls={insight.source_urls} />
          </div>
        ))}
      </div>
      <div className="grid gap-5 lg:grid-cols-2">
        {research.campaign_opportunities.map((opportunity) => (
          <InfoCard
            key={opportunity.opportunity}
            title={opportunity.opportunity}
            text={`${opportunity.rationale} ${opportunity.recommended_direction}`}
          />
        ))}
      </div>
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="font-bold text-[#172033]">Sources</h3>
        <div className="mt-4 space-y-3">
          {research.sources.map((source) => (
            <a
              key={source.url}
              href={source.url}
              target="_blank"
              rel="noreferrer"
              className="block rounded-xl bg-[#f8fafc] p-4 hover:bg-[#eeecff]"
            >
              <p className="text-sm font-semibold text-[#635bff]">
                {source.title}
              </p>
              <p className="mt-1 text-xs text-slate-500">{source.publisher}</p>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

function SourceLinks({ urls }: { urls: readonly string[] }) {
  return (
    <div className="mt-4 flex flex-wrap gap-2">
      {urls.map((url) => (
        <a
          key={url}
          href={url}
          target="_blank"
          rel="noreferrer"
          className="text-xs font-semibold text-[#635bff] underline"
        >
          Source
        </a>
      ))}
    </div>
  );
}

function SectionIntro({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div>
      <h2 className="text-2xl font-bold tracking-[-.03em] text-[#172033]">
        {title}
      </h2>
      <p className="mt-2 text-sm text-slate-500">{description}</p>
    </div>
  );
}

function MediaPlanSection() {
  const mediaPlan = campaignResponse.media_plan;

  return (
    <section className="mt-8 space-y-5">
      <SectionIntro
        title="Media Plan"
        description="Channel strategy and proposed campaign schedule for Sip Consciously: Small Cups, Big Shift."
      />

      <div className="rounded-2xl border border-[#c9c4ff] bg-[#faf9ff] p-6 shadow-sm">
        <p className="eyebrow">Campaign duration</p>
        <p className="mt-2 text-2xl font-bold text-[#172033]">
          {mediaPlan.campaign_duration}
        </p>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          The schedule below is a proposed plan based on the supplied Media
          Planner response and campaign assets.
        </p>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="min-w-[760px]">
          <div className="grid grid-cols-4 gap-4 border-b border-slate-200 bg-[#f8fafc] p-4 text-xs font-semibold uppercase tracking-[.06em] text-slate-500">
            <span>Channel</span>
            <span>Purpose</span>
            <span>Recommended content</span>
            <span>Primary CTA</span>
          </div>
          {mediaPlan.channel_strategy.map((channel) => (
            <div
              key={channel.channel}
              className="grid grid-cols-4 gap-4 border-b border-slate-100 p-4 text-sm last:border-0"
            >
              <strong className="text-[#172033]">{channel.channel}</strong>
              <span className="leading-6 text-slate-600">
                {channel.purpose}
              </span>
              <span className="leading-6 text-slate-600">
                {channel.content}
              </span>
              <span className="leading-6 text-slate-600">
                {channel.call_to_action}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="font-bold text-[#172033]">Four-week schedule</h3>
        <div className="mt-4 space-y-3">
          {mediaPlan.schedule.map((phase) => (
            <div
              key={phase.phase}
              className="grid gap-2 rounded-xl bg-[#f8fafc] p-4 md:grid-cols-[130px_100px_1fr]"
            >
              <strong className="text-sm text-[#172033]">{phase.phase}</strong>
              <span className="text-sm font-semibold text-[#635bff]">
                {phase.timing}
              </span>
              <div className="text-sm leading-6 text-slate-600">
                <p>{phase.activities}</p>
                <p className="mt-1 text-xs text-slate-400">{phase.channels}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="font-bold text-[#172033]">Measurement plan</h3>
          <div className="mt-4 space-y-3">
            {mediaPlan.measurement_plan.map(([objective, measurement]) => (
              <div key={objective}>
                <p className="text-sm font-semibold text-slate-700">
                  {objective}
                </p>
                <p className="mt-1 text-sm text-slate-500">{measurement}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="font-bold text-[#172033]">Key recommendations</h3>
          <List items={mediaPlan.recommendations} />
        </div>
      </div>

      <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 text-sm leading-6 text-amber-900">
        No numerical channel allocation or confirmed budget breakdown was
        included in the supplied response, so none is displayed.
      </div>
    </section>
  );
}

function ContentAssetsSection() {
  const [copied, setCopied] = useState("");
  async function copy(label: string, value: string) {
    await navigator.clipboard.writeText(value);
    setCopied(label);
    window.setTimeout(() => setCopied(""), 1800);
  }

  return (
    <section className="mt-8 space-y-5">
      <SectionIntro
        title="Content Assets"
        description="Platform-specific captions, hooks, hashtags, and article content from the Content Agent."
      />
      {campaignResponse.content_assets.map((asset) =>
        asset.content_type === "blog" ? (
          <article
            key={asset.title}
            className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            <p className="eyebrow">Blog article</p>
            <h3 className="mt-2 text-xl font-bold text-[#172033]">
              {asset.title}
            </h3>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              {asset.introduction}
            </p>
            <div className="mt-5 space-y-4">
              {asset.sections.map((section) => (
                <p key={section} className="text-sm leading-7 text-slate-600">
                  {section}
                </p>
              ))}
            </div>
            <p className="mt-5 text-sm leading-7 text-slate-600">
              {asset.conclusion}
            </p>
            <button
              onClick={() =>
                copy(
                  "article",
                  [
                    asset.title,
                    asset.introduction,
                    ...asset.sections,
                    asset.conclusion,
                    asset.call_to_action,
                  ].join("\n\n"),
                )
              }
              className="secondary-button mt-5"
            >
              {copied === "article" ? "Copied" : "Copy article"}
            </button>
          </article>
        ) : (
          <article
            key={asset.hook}
            className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <p className="eyebrow">{asset.platform}</p>
              <span className="text-xs text-slate-400">Social post</span>
            </div>
            <h3 className="mt-2 text-xl font-bold text-[#172033]">
              {asset.hook}
            </h3>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              {asset.caption}
            </p>
            <p className="mt-4 text-sm font-semibold text-slate-700">
              CTA: {asset.call_to_action}
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              {asset.hashtags.map((hashtag) => (
                <span
                  key={hashtag}
                  className="rounded-full bg-[#eeecff] px-2.5 py-1 text-xs text-[#635bff]"
                >
                  {hashtag}
                </span>
              ))}
            </div>
            <div className="mt-5 flex flex-wrap gap-2">
              <button
                onClick={() => copy(`${asset.platform}-caption`, asset.caption)}
                className="secondary-button"
              >
                {copied === `${asset.platform}-caption`
                  ? "Copied"
                  : "Copy caption"}
              </button>
              <button
                onClick={() =>
                  copy(`${asset.platform}-hashtags`, asset.hashtags.join(" "))
                }
                className="secondary-button"
              >
                {copied === `${asset.platform}-hashtags`
                  ? "Copied"
                  : "Copy hashtags"}
              </button>
              <button
                onClick={() =>
                  copy(
                    `${asset.platform}-full`,
                    `${asset.hook}\n\n${asset.caption}\n\n${asset.call_to_action}\n\n${asset.hashtags.join(" ")}`,
                  )
                }
                className="primary-button"
              >
                {copied === `${asset.platform}-full`
                  ? "Copied"
                  : "Copy full post"}
              </button>
            </div>
          </article>
        ),
      )}
    </section>
  );
}

function AssetCard({
  asset,
  onPreview,
}: {
  asset: CampaignAsset;
  onPreview: (asset: CampaignAsset) => void;
}) {
  return (
    <article className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-lg">
      <button
        type="button"
        onClick={() => onPreview(asset)}
        className="group relative block aspect-square w-full overflow-hidden bg-slate-100 text-left"
        aria-label={`Preview ${asset.label}`}
      >
        <img
          src={asset.imageUrl}
          alt={asset.title}
          className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
        />
        <span className="absolute right-3 top-3 rounded-lg bg-white/90 p-2 text-slate-600 opacity-0 shadow-sm transition group-hover:opacity-100">
          <Maximize2 size={15} />
        </span>
      </button>
      <div className="p-4">
        <p className="text-[11px] font-semibold uppercase tracking-[.08em] text-[#8b5cf6]">
          {asset.label}
        </p>
        <h3 className="mt-2 text-sm font-semibold text-[#172033]">
          {asset.title}
        </h3>
        <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3">
          <span className="flex items-center gap-2 text-xs font-medium text-slate-600">
            <Camera size={15} className="text-[#635bff]" />
            {asset.platform}
          </span>
          <span className="text-[11px] text-emerald-600">Ready</span>
        </div>
      </div>
    </article>
  );
}

function CampaignSnapshot({ campaignTitle }: { campaignTitle: string }) {
  return (
    <aside className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="font-bold text-[#172033]">Campaign snapshot</h2>
      <div className="mt-5 space-y-4 text-sm">
        <div>
          <p className="text-xs text-slate-400">Status</p>
          <p className="mt-1 text-emerald-600">Validated</p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Channels</p>
          <p className="mt-1 text-slate-700">Instagram</p>
        </div>
      </div>
      <button
        onClick={() => navigator.clipboard?.writeText(campaignTitle)}
        className="secondary-button mt-8 w-full justify-center"
      >
        <Copy size={14} /> Copy campaign link
      </button>
    </aside>
  );
}

function AgentEmptyState({
  tab,
  description,
}: {
  tab: string;
  description: string;
}) {
  return (
    <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-10 text-center shadow-sm">
      <ImageIcon className="mx-auto text-[#635bff]" size={28} />
      <h2 className="mt-4 text-lg font-bold text-[#172033]">{tab}</h2>
      <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-500">
        {description}
      </p>
    </section>
  );
}

function ImagePreview({
  asset,
  onClose,
}: {
  asset: CampaignAsset;
  onClose: () => void;
}) {
  return (
    <div
      className="modal-backdrop"
      role="dialog"
      aria-modal="true"
      aria-label={`${asset.label} preview`}
      onClick={onClose}
    >
      <div
        className="relative max-h-[90vh] w-full max-w-3xl rounded-2xl bg-white p-3 shadow-2xl"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          type="button"
          onClick={onClose}
          className="modal-close rounded-lg bg-white p-2 shadow-sm"
          aria-label="Close image preview"
        >
          <X size={18} />
        </button>
        <img
          src={asset.imageUrl}
          alt={asset.title}
          className="max-h-[82vh] w-full rounded-xl object-contain"
        />
        <div className="flex items-center justify-between px-2 pb-1 pt-3">
          <p className="text-sm font-semibold text-[#172033]">{asset.label}</p>
          <p className="flex items-center gap-2 text-xs text-slate-500">
            <Camera size={14} className="text-[#635bff]" />
            {asset.platform}
          </p>
        </div>
      </div>
    </div>
  );
}
