"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  FolderKanban,
  HelpCircle,
  LayoutDashboard,
  Plus,
  Settings,
  Sparkles,
} from "lucide-react";

export function Logo() {
  return (
    <Link href="/dashboard" className="flex items-center gap-2.5">
      <span className="logo-mark">
        <Sparkles size={15} strokeWidth={2.5} />
      </span>
      <span className="text-[15px] font-semibold tracking-[-0.02em] text-[#172033]">
        Campaign Strategist
      </span>
    </Link>
  );
}

export function AuthShell({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-[#f8fafc] px-6 py-8">
      <div className="mx-auto max-w-6xl">
        <Logo />
        {children}
      </div>
    </main>
  );
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const nav = [
    ["/dashboard", "Dashboard", LayoutDashboard],
    ["/campaigns/new", "Create campaign", Plus],
    ["/settings", "Settings", Settings],
  ] as const;
  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="px-5 pb-9 pt-7">
          <Logo />
        </div>
        <div className="px-3">
          <p className="nav-label">Workspace</p>
          <nav className="space-y-1" aria-label="Main navigation">
            {nav.map(([href, label, Icon]) => (
              <Link
                key={href}
                href={href}
                className={`nav-item ${pathname === href ? "nav-active" : ""}`}
              >
                <Icon size={17} />
                {label}
              </Link>
            ))}
          </nav>
          <Link href="/campaigns/new" className="create-nav">
            <span className="flex h-6 w-6 items-center justify-center rounded-md bg-white/15">
              <Plus size={15} />
            </span>
            Create campaign
          </Link>
          <p className="nav-label mt-9">Manage</p>
          <nav className="space-y-1">
            <button className="nav-item">
              <HelpCircle size={17} />
              Help center
            </button>
            <button className="nav-item">
              <BarChart3 size={17} />
              Insights
            </button>
          </nav>
        </div>
        <div className="mt-auto border-t border-slate-100 px-3 pb-5 pt-4">
          <div className="profile-row">
            <div className="avatar">AM</div>
            <div className="min-w-0 text-left">
              <p className="truncate text-[12px] font-semibold text-[#172033]">
                Alex Morgan
              </p>
              <p className="truncate text-[11px] text-slate-400">
                alex@northstar.co
              </p>
            </div>
          </div>
        </div>
      </aside>
      <section className="main-area">
        <header className="topbar">
          <div className="text-[12px] text-slate-400">
            Workspace /{" "}
            <span className="font-medium text-slate-600">
              {pathname.includes("campaigns")
                ? "Campaigns"
                : pathname.slice(1) || "Dashboard"}
            </span>
          </div>
          <div className="top-avatar">AM</div>
        </header>
        {children}
      </section>
    </main>
  );
}

export function SectionTitle({
  eyebrow,
  title,
  description,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
}) {
  return (
    <div>
      {eyebrow && <p className="eyebrow">{eyebrow}</p>}
      <h1 className="text-3xl font-bold tracking-[-.04em] text-[#172033]">
        {title}
      </h1>
      {description && (
        <p className="mt-2 text-sm text-slate-500">{description}</p>
      )}
    </div>
  );
}

export function ButtonLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  return (
    <Link href={href} className="primary-button">
      {children}
    </Link>
  );
}
