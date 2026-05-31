"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_API_URL ?? "";

interface Session {
  id: string;
  status: string;
  total_responses: number;
}

interface SessionDetail {
  id: string;
  status: string;
  total_responses: number;
  responses: Record<string, string>;
}

export default function SessionsPage() {
  const { getToken } = useAuth();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selected, setSelected] = useState<SessionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const token = await getToken();
        const res = await fetch(`${API}/api/v1/sessions/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Failed to load sessions.");
        setSessions(await res.json());
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load sessions.");
      } finally {
        setLoading(false);
      }
    })();
  }, [getToken]);

  const loadDetail = async (id: string) => {
    setDetailLoading(true);
    try {
      const token = await getToken();
      const res = await fetch(`${API}/api/v1/sessions/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Failed to load session.");
      setSelected(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load session.");
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <main className="pt-nav">
      {/* Header */}
      <section style={{ padding: "5rem 0 4rem", borderBottom: "1px solid var(--border)" }}>
        <div className="container">
          <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>
            History
          </span>
          <h1 style={{ fontSize: "clamp(2rem, 4.5vw, 3.5rem)", marginBottom: "1.2rem" }}>
            Your Evaluations
          </h1>
          <p style={{ color: "var(--secondary)", lineHeight: 1.85, fontSize: "1.1rem", maxWidth: "560px" }}>
            Review your past YUYAY evaluation sessions and their results.
          </p>
        </div>
      </section>

      <section style={{ padding: "4rem 0 6rem" }}>
        <div className="container" style={{ display: "grid", gridTemplateColumns: selected ? "1fr 1.5fr" : "1fr", gap: "3rem" }}>

          {/* Sessions list */}
          <div>
            {loading && (
              <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>Loading sessions…</p>
            )}
            {error && (
              <p style={{ color: "var(--red)", fontSize: "0.9rem" }}>{error}</p>
            )}
            {!loading && sessions.length === 0 && (
              <div>
                <p style={{ color: "var(--muted)", marginBottom: "1.5rem", lineHeight: 1.7 }}>
                  No evaluations yet.
                </p>
                <Link href="/evaluate" className="btn btn-primary">
                  Start Your First Evaluation
                </Link>
              </div>
            )}
            {sessions.map((s) => (
              <div
                key={s.id}
                onClick={() => loadDetail(s.id)}
                style={{
                  padding: "1.5rem 2rem",
                  borderBottom: "1px solid var(--border)",
                  cursor: "pointer",
                  background: selected?.id === s.id ? "var(--surface)" : "transparent",
                  transition: "background 0.15s ease",
                }}
                onMouseEnter={(e) => { if (selected?.id !== s.id) (e.currentTarget as HTMLElement).style.background = "var(--surface)"; }}
                onMouseLeave={(e) => { if (selected?.id !== s.id) (e.currentTarget as HTMLElement).style.background = "transparent"; }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.4rem" }}>
                  <span style={{ fontSize: "0.72rem", color: "var(--muted)", fontFamily: "var(--font-garamond)", letterSpacing: "0.05em" }}>
                    {s.id.slice(0, 8)}…
                  </span>
                  <span className={s.status === "complete" ? "tag tag-green" : "tag tag-gold"}>
                    {s.status}
                  </span>
                </div>
                <p style={{ fontSize: "0.88rem", color: "var(--secondary)" }}>
                  {s.total_responses} responses
                </p>
              </div>
            ))}
          </div>

          {/* Session detail */}
          {selected && (
            <div style={{ borderLeft: "1px solid var(--border)", paddingLeft: "3rem" }}>
              {detailLoading ? (
                <p style={{ color: "var(--muted)", fontSize: "0.9rem" }}>Loading…</p>
              ) : (
                <>
                  <span className="eyebrow" style={{ marginBottom: "1.5rem" }}>
                    Session Detail
                  </span>
                  <p style={{ fontSize: "0.75rem", color: "var(--muted)", marginBottom: "2rem", letterSpacing: "0.05em" }}>
                    ID: {selected.id}
                  </p>
                  <div style={{ border: "1px solid var(--border)" }}>
                    {Object.entries(selected.responses).map(([id, answer], i) => (
                      <div
                        key={id}
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          padding: "0.9rem 1.2rem",
                          borderBottom: i < Object.keys(selected.responses).length - 1 ? "1px solid var(--border)" : undefined,
                        }}
                      >
                        <span style={{ fontSize: "0.82rem", color: "var(--muted)" }}>
                          Question {id}
                        </span>
                        <span className={answer === "YES" ? "tag tag-green" : answer === "NO" ? "tag tag-red" : "tag tag-gold"}>
                          {answer}
                        </span>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}