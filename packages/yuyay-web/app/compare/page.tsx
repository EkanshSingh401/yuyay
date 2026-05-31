"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";

const API = process.env.NEXT_PUBLIC_API_URL ?? "";

interface CompareResult {
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

interface CompareResponse {
  prompt: string;
  results: CompareResult[];
  best_provider: string;
}

type Phase = "idle" | "loading" | "results" | "error";

const PROVIDERS = [
  { value: "anthropic", label: "Anthropic Claude", model: "claude-sonnet-4-6" },
  { value: "openai", label: "OpenAI GPT", model: "gpt-4" },
  { value: "google", label: "Google Gemini", model: "gemini-pro" },
  { value: "mock", label: "Mock", model: "mock-model" },
];

export default function ComparePage() {
  const { getToken } = useAuth();
  const [prompt, setPrompt] = useState("");
  const [selectedProviders, setSelectedProviders] = useState<string[]>(["anthropic", "google"]);
  const [phase, setPhase] = useState<Phase>("idle");
  const [result, setResult] = useState<CompareResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState("");

  const toggleProvider = (value: string) => {
    setSelectedProviders((prev) =>
      prev.includes(value) ? prev.filter((p) => p !== value) : [...prev, value]
    );
  };

  const handleSubmit = async () => {
    if (!prompt.trim() || selectedProviders.length === 0) return;
    setPhase("loading");
    setResult(null);
    try {
      const token = await getToken();
      const providers = selectedProviders.map((p) => ({
        provider: p,
        model: PROVIDERS.find((pr) => pr.value === p)!.model,
        api_key: "",
      }));
      const res = await fetch(`${API}/api/v1/compare`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ prompt, providers }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail ?? "Comparison failed.");
      }
      const data: CompareResponse = await res.json();
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
            Multi-Provider Analysis
          </span>
          <h1 style={{ fontSize: "clamp(2rem, 4.5vw, 3.5rem)", marginBottom: "1.2rem" }}>
            Compare Providers
          </h1>
          <p style={{ color: "var(--secondary)", lineHeight: 1.85, fontSize: "1.1rem", maxWidth: "560px" }}>
            Send the same query to multiple LLM providers simultaneously. FIOS evaluates
            each response against YUYAY coherence metrics and identifies the best answer.
          </p>
        </div>
      </section>

      {/* Form */}
      <section style={{ padding: "4rem 0" }}>
        <div className="container-narrow">
          {/* Provider selector */}
          <div style={{ marginBottom: "2rem" }}>
            <p style={{ fontSize: "0.68rem", letterSpacing: "0.22em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "1rem" }}>
              Select Providers
            </p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.6rem" }}>
              {PROVIDERS.map((p) => {
                const sel = selectedProviders.includes(p.value);
                return (
                  <button
                    key={p.value}
                    type="button"
                    className={sel ? "answer-btn sel-po" : "answer-btn"}
                    onClick={() => toggleProvider(p.value)}
                  >
                    {p.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Prompt */}
          <div style={{ marginBottom: "1.5rem" }}>
            <p style={{ fontSize: "0.68rem", letterSpacing: "0.22em", textTransform: "uppercase", color: "var(--gold)", marginBottom: "1rem" }}>
              Your Question
            </p>
            <textarea
              className="input"
              rows={5}
              placeholder="What is the highest purpose of technology?"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              style={{ resize: "vertical", fontFamily: "var(--font-garamond)", lineHeight: 1.7 }}
            />
          </div>

          <button
            className="btn btn-primary"
            onClick={handleSubmit}
            disabled={!prompt.trim() || selectedProviders.length === 0 || phase === "loading"}
            style={{ opacity: prompt.trim() && selectedProviders.length > 0 && phase !== "loading" ? 1 : 0.4 }}
          >
            {phase === "loading" ? `Querying ${selectedProviders.length} providers…` : "Compare Providers"}
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
        <section style={{ padding: "2rem 0 6rem", borderTop: "1px solid var(--border)" }}>
          <div className="container">
            <div style={{ marginBottom: "2rem" }}>
              <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>Results</span>
              <p style={{ color: "var(--muted)", fontSize: "0.88rem" }}>
                Best provider: <span style={{ color: "var(--gold)" }}>{result.best_provider}</span>
              </p>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: `repeat(${result.results.length}, 1fr)`, gap: "1.5rem" }}>
              {result.results.map((r) => (
                <div
                  key={r.provider}
                  style={{
                    border: "1px solid var(--border)",
                    background: r.provider === result.best_provider ? "var(--surface-2)" : "var(--surface)",
                    padding: "2.5rem 2rem",
                    position: "relative",
                  }}
                >
                  {r.provider === result.best_provider && (
                    <span className="tag tag-amber" style={{
                      position: "absolute",
                      top: "1rem",
                      right: "1rem",
                    }}>
                      Best
                    </span>
                  )}
                  <h3 style={{ fontSize: "1rem", color: "var(--gold)", marginBottom: "0.3rem", fontWeight: 400 }}>
                    {r.provider}
                  </h3>
                  <p style={{ fontSize: "0.75rem", color: "var(--muted)", marginBottom: "1.5rem" }}>
                    {r.model}
                  </p>

                  <div
                    style={{
                      display: "grid",
                      gridTemplateColumns: "repeat(4, 1fr)",
                      gap: 0,
                      border: "1px solid var(--border)",
                      marginBottom: "1.5rem",
                    }}
                  >
                    {[
                      { label: "Coherence", value: `${r.coherence_score}/100` },
                      { label: "Tokens", value: r.total_tokens },
                      { label: "Latency", value: `${r.latency_ms.toFixed(0)}ms` },
                      { label: "Cost", value: `$${r.estimated_cost_usd.toFixed(6)}` },
                    ].map((m, i) => (
                      <div
                        key={m.label}
                        style={{
                          padding: "1rem",
                          textAlign: "center",
                          borderRight: i < 3 ? "1px solid var(--border)" : undefined,
                        }}
                      >
                        <div
                          style={{
                            fontFamily: "var(--font-playfair)",
                            fontSize: "0.95rem",
                            color: "var(--fg)",
                            lineHeight: 1,
                            marginBottom: "0.25rem",
                          }}
                        >
                          {m.value}
                        </div>
                        <div
                          style={{
                            fontSize: "0.6rem",
                            letterSpacing: "0.18em",
                            textTransform: "uppercase",
                            color: "var(--muted)",
                          }}
                        >
                          {m.label}
                        </div>
                      </div>
                    ))}
                  </div>

                  <hr className="rule" style={{ marginBottom: "1.5rem" }} />

                  <p style={{ fontSize: "0.88rem", color: "var(--secondary)", lineHeight: 1.8, whiteSpace: "pre-wrap" }}>
                    {r.response}
                  </p>

                  {r.flags.length > 0 && (
                    <div style={{ marginTop: "1rem" }}>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: "0.35rem" }}>
                        {r.flags.map((f) => (
                          <span key={f} className="tag tag-amber">{f}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </main>
  );
}