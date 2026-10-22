"use client";
import Link from "next/link";
import { useState } from "react";
import { Eye, EyeOff, Sparkles } from "lucide-react";
import { AuthShell } from "@/components/campaign-app";
export default function LoginPage() {
  const [show, setShow] = useState(false);
  const [error, setError] = useState("");
  function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    if (!String(d.get("email")).includes("@") || !d.get("password"))
      setError("Enter a valid email and password.");
    else window.location.href = "/dashboard";
  }
  return (
    <AuthShell>
      <div className="mx-auto mt-20 max-w-md rounded-3xl border border-slate-200 bg-white p-8 shadow-sm sm:p-12">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-[#eeecff] text-[#635bff]">
          <Sparkles size={22} />
        </div>
        <div className="mt-6 text-center">
          <p className="eyebrow">Welcome back</p>
          <h1 className="text-3xl font-bold tracking-[-.04em] text-[#172033]">
            Sign in to your workspace
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Pick up where your next great campaign begins.
          </p>
        </div>
        <form onSubmit={submit} className="mt-8 space-y-5">
          <label className="block text-sm font-medium text-slate-700">
            Email address
            <input
              name="email"
              type="email"
              required
              placeholder="you@company.com"
              className="form-input mt-2"
            />
          </label>
          <label className="block text-sm font-medium text-slate-700">
            Password
            <div className="relative mt-2">
              <input
                name="password"
                type={show ? "text" : "password"}
                required
                className="form-input"
              />
              <button
                type="button"
                onClick={() => setShow(!show)}
                className="absolute right-3 top-3 text-slate-400"
                aria-label="Show password"
              >
                {show ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </label>
          <div className="flex justify-end">
            <Link href="#" className="text-xs font-semibold text-[#635bff]">
              Forgot password?
            </Link>
          </div>
          {error && (
            <p role="alert" className="text-xs text-red-600">
              {error}
            </p>
          )}
          <button className="primary-button w-full justify-center py-3">
            Sign In
          </button>
        </form>
        <p className="mt-7 text-center text-sm text-slate-500">
          New to Campaign Strategist?{" "}
          <Link href="/signup" className="font-semibold text-[#635bff]">
            Create an account
          </Link>
        </p>
      </div>
    </AuthShell>
  );
}
