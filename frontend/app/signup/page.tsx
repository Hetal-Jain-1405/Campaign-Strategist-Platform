"use client";
import Link from "next/link";
import { useState } from "react";
import { Check, Eye, EyeOff, Sparkles } from "lucide-react";
import { AuthShell } from "@/components/campaign-app";
import { getSupabaseClient } from "@/lib/supabase";

export default function SignupPage() {
  const [show, setShow] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const password = String(formData.get("password"));
    if (
      !formData.get("name") ||
      !formData.get("email") ||
      !password ||
      !formData.get("confirm")
    )
      return setError("Please complete every field.");
    if (!String(formData.get("email")).includes("@"))
      return setError("Enter a valid email address.");
    if (password.length < 8)
      return setError("Password must be at least 8 characters.");
    if (password !== formData.get("confirm"))
      return setError("Passwords do not match.");
    if (!formData.get("terms")) return setError("Accept the terms to continue.");
    setError("");
    const { data: signupData, error: signupError } = await getSupabaseClient().auth.signUp({
      email: String(formData.get("email")),
      password,
      options: { data: { full_name: String(formData.get("name")) } },
    });
    if (signupError) {
      setError(signupError.message);
      return;
    }
    setSuccess(!signupData.session);
    if (signupData.session) window.location.href = "/dashboard";
  }
  return (
    <AuthShell>
      <div className="mx-auto mt-12 grid max-w-5xl overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm lg:grid-cols-2">
        <section className="hidden bg-[#f0efff] p-12 lg:block">
          <div className="flex h-full flex-col justify-between">
            <div>
              <span className="inline-flex rounded-xl bg-white p-3 text-[#635bff]">
                <Sparkles size={22} />
              </span>
              <h1 className="mt-10 max-w-sm text-4xl font-bold leading-tight tracking-[-.05em] text-[#172033]">
                Turn your ideas into campaigns that work.
              </h1>
              <p className="mt-5 max-w-sm text-sm leading-7 text-slate-600">
                One intelligent workspace for research, strategy, creative, and
                media planning.
              </p>
              <ul className="mt-10 space-y-5 text-sm text-slate-700">
                {[
                  "AI-powered research",
                  "Campaign strategy that stays focused",
                  "Creative generation for every channel",
                ].map((x) => (
                  <li key={x} className="flex items-center gap-3">
                    <span className="rounded-full bg-white p-1 text-emerald-600">
                      <Check size={13} />
                    </span>
                    {x}
                  </li>
                ))}
              </ul>
            </div>
            <div className="mt-12 flex items-end justify-center gap-3">
              <div className="h-20 w-20 rounded-full bg-white/80" />
              <div className="mb-8 h-28 w-28 rounded-[40%] bg-[#c9c4ff]" />
              <div className="h-14 w-14 rounded-full bg-[#a7f3d0]" />
            </div>
          </div>
        </section>
        <section className="p-8 sm:p-12">
          <p className="eyebrow">Get started</p>
          <h2 className="text-3xl font-bold tracking-[-.04em] text-[#172033]">
            Create your account
          </h2>
          <p className="mt-2 text-sm text-slate-500">
            Build better campaigns with your AI team.
          </p>
          <form onSubmit={submit} className="mt-8 space-y-4">
            {[
              ["name", "Full name", "Alex Morgan", "text"],
              ["email", "Email address", "you@company.com", "email"],
              ["password", "Password", "At least 8 characters", "password"],
              [
                "confirm",
                "Confirm password",
                "Repeat your password",
                "password",
              ],
            ].map(([id, label, placeholder, type]) => (
              <label
                key={id}
                className="block text-sm font-medium text-slate-700"
              >
                {label}
                <div className="relative mt-2">
                  <input
                    required
                    name={id}
                    type={type === "password" && show ? "text" : type}
                    placeholder={placeholder}
                    className="form-input"
                  />
                  {type === "password" && (
                    <button
                      type="button"
                      aria-label="Show password"
                      onClick={() => setShow(!show)}
                      className="absolute right-3 top-3 text-slate-400"
                    >
                      {show ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  )}
                </div>
              </label>
            ))}
            <label className="flex items-start gap-2 text-xs text-slate-500">
              <input
                name="terms"
                type="checkbox"
                className="mt-0.5 accent-[#635bff]"
              />
              I agree to the Terms of Service and Privacy Policy.
            </label>
            {error && (
              <p role="alert" className="text-xs text-red-600">
                {error}
              </p>
            )}
            {success && (
              <p className="rounded-lg bg-emerald-50 p-3 text-xs text-emerald-700">
                Account created.{" "}
                <Link className="font-semibold underline" href="/dashboard">
                  Continue to dashboard
                </Link>
              </p>
            )}
            <button className="primary-button w-full justify-center py-3">
              Create Account
            </button>
          </form>
          <p className="mt-6 text-center text-sm text-slate-500">
            Already have an account?{" "}
            <Link href="/login" className="font-semibold text-[#635bff]">
              Sign in
            </Link>
          </p>
        </section>
      </div>
    </AuthShell>
  );
}
