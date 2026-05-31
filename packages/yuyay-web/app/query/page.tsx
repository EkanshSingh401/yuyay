"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";

const API = process.env.NEXT_PUBLIC_API_URL ?? "";

interface QueryResult {
  provider: string;
  model: string;
  response: string;
  coherence_score: number;
  flags: string[];
  total_tokens: number;
  latency_ms: number;
  estimated_cost_usd: number;
  summary: string;
}

type Phase = "idle" | "loading" | "results" | "error";

const PROVIDERS = [
  { value: "anthropic", label: "Anthropic Claude", model: "claude-sonnet-4-6" },
  { value: "openai", label: "OpenAI GPT", model: "gpt-4" },
  { value: "google", label: "Google Gemini", model: "gemini-pro" },
];

export default function QueryPage() {
  const { getToken } = useAuth();
  const [prompt, setPrompt] = useState("");
  const [provider, setProvider] = useState("anthropic");
  const [phase, setPhase] = useState<Phase>("idle");
  const [result, setResult] = useState<QueryResult | null>(null);
  const [errorMsg, setErrorMsg] = useState("");

  const selectedProvider = PROVIDERS.find((p) => p.value === provider)!;

  const handleSubmit = async () => {
    if (!prompt.trim()) return;
    setPhase("loading");
    setResult(null);
    try {
      const token = await getToken();
      const res = await fetch(`${API}/api/v1/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          prompt,
          provider,
          model: selectedProvider.model,
          api_key: "",
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail ?? "Query failed.");
      }
      const data: QueryResult = await res.json();
      setResult(data);
      setPhase("results");
    } catch (e) {
      setErrorMsg(e instanceof Error ? e.message : "An unknown error occurred.");
      setPhase("error");
    }
  };

  return (
    <main className="pt-nav">
      {/* Header */}
      <section style={{ padding: "5rem 0 4rem", borderBottom: "1px solid var(--border)" }}>
        <div className="container-narrow">
          <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>
            FIOS Intelligence
          </span>
          <h1 style={{ fontSize: "clamp(2rem, 4.5vw, 3.5rem)", marginBottom: "1.2rem" }}>
            Query the Framework
          </h1>
          <p style={{ color: "var(--secondary)", lineHeight: 1.85, fontSize: "1.1rem", maxWidth: "560px" }}>
            Send any question through FIOS — the Foundational Intelligent OS. Your query
            is enriched with the full YUYAY framework context before being sent to the
            selected LLM provider.
          </p>
        </div>
      </section>

      {/* Query Form */}
      <section style={{ padding: "4rem 0" }}>
        <div className="container-narrow">
          {/* Provider selector */}
          <div style={{ marginBottom: "2rem" }}>
            <p style={{ fontSize: "0.68rem", letterSpacing: "0.22em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "1rem" }}>
              Provider
            </p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.6rem" }}>
              {PROVIDERS.map((p) => (
                <button
                  key={p.value}
                  type="button"
                  className={provider === p.value ? "answer-btn sel-po" : "answer-btn"}
                  onClick={() => setProvider(p.value)}
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

          {/* Prompt input */}
          <div style={{ marginBottom: "1.5rem" }}>
            <p style={{ fontSize: "0.68rem", letterSpacing: "0.22em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "1rem" }}>
              Your Question
            </p>
            <textarea
              className="input"
              rows={5}
              placeholder="What is the highest purpose of technology? How can we build systems that serve humanity?"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              style={{ resize: "vertical", fontFamily: "var(--font-garamond)", lineHeight: 1.7 }}
            />
          </div>

          <button
            className="btn btn-primary"
            onClick={handleSubmit}
            disabled={!prompt.trim() || phase === "loading"}
            style={{ opacity: prompt.trim() && phase !== "loading" ? 1 : 0.4, cursor: prompt.trim() && phase !== "loading" ? "pointer" : "not-allowed" }}
          >
            {phase === "loading" ? "Querying…" : "Send Query"}
          </button>
        </div>
      </section>

      {/* Error */}
      {phase === "error" && (
        <section style={{ padding: "2rem 0" }}>
          <div className="container-narrow">
            <p style={{ color: "var(--red)", lineHeight: 1.7 }}>{errorMsg}</p>
          </div>
        </section>
      )}

      {/* Results */}
      {phase === "results" && result && (
        <section style={{ padding: "4rem 0 6rem", borderTop: "1px solid var(--border)" }}>
          <div className="container-narrow">
            <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>
              Response
            </span>

            {/* Meta */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(5, 1fr)",
                gap: 0,
                border: "1px solid var(--border)",
                marginBottom: "2rem",
              }}
            >
              {[
                { label: "Provider", value: `${result.provider}` },
                { label: "Coherence", value: `${result.coherence_score}/100` },
                { label: "Tokens", value: `${result.total_tokens}` },
                { label: "Latency", value: `${result.latency_ms.toFixed(0)}ms` },
                { label: "Cost", value: `$${result.estimated_cost_usd.toFixed(6)}` },
              ].map((m, i) => (
                <div
                  key={m.label}
                  style={{
                    padding: "1.5rem",
                    textAlign: "center",
                    borderRight: i < 4 ? "1px solid var(--border)" : undefined,
                  }}
                >
                  <div
                    style={{
                      fontFamily: "var(--font-playfair)",
                      fontSize: "1.1rem",
                      color: "var(--gold)",
                      lineHeight: 1,
                      marginBottom: "0.4rem",
                    }}
                  >
                    {m.value}
                  </div>
                  <div
                    style={{
                      fontSize: "0.68rem",
                      letterSpacing: "0.2em",
                      textTransform: "uppercase",
                      color: "var(--muted)",
                    }}
                  >
                    {m.label}
                  </div>
                </div>
              ))}
            </div>

            {/* Response text */}
            <div style={{ padding: "2rem 2.5rem", border: "1px solid var(--border)", background: "var(--surface)", marginBottom: "2rem" }}>
              <p style={{ fontSize: "1.05rem", color: "var(--secondary)", lineHeight: 1.9, whiteSpace: "pre-wrap" }}>
                {result.response}
              </p>
            </div>

            {/* Flags */}
            {result.flags.length > 0 && (
              <div>
                <p style={{ fontSize: "0.62rem", letterSpacing: "0.22em", textTransform: "uppercase", color: "var(--amber)", marginBottom: "0.8rem" }}>
                  Missing YUYAY concepts
                </p>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem" }}>
                  {result.flags.map((f) => (
                    <span key={f} className="tag tag-amber">{f}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>
      )}
    </main>
  );
}