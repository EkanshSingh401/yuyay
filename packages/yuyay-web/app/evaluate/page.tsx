"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";

const API = process.env.NEXT_PUBLIC_API_URL ?? "";

interface Transformer {
  id: string;
  question: string;
}

interface EvalResult {
  session_id: string;
  yes_count: number;
  no_count: number;
  po_count: number;
  total: number;
  flags: string[];
  summary: string;
}

type Answer = "YES" | "NO" | "PO";
type Phase = "loading" | "questions" | "submitting" | "results" | "error";

function AnswerButton({
  value,
  selected,
  onClick,
}: {
  value: Answer;
  selected: boolean;
  onClick: () => void;
}) {
  const cls = selected ? `answer-btn sel-${value.toLowerCase()}` : "answer-btn";
  return (
    <button type="button" className={cls} onClick={onClick}>
      {value}
    </button>
  );
}

export default function EvaluatePage() {
  const { getToken } = useAuth();
  const [questions, setQuestions] = useState<Transformer[]>([]);
  const [answers, setAnswers] = useState<Record<string, Answer>>({});
  const [phase, setPhase] = useState<Phase>("loading");
  const [result, setResult] = useState<EvalResult | null>(null);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    fetch(`${API}/api/v1/transformers/`)
      .then((r) => r.json())
      .then((data: Transformer[]) => {
        setQuestions(data);
        setPhase("questions");
      })
      .catch(() => {
        setErrorMsg("Unable to load questions. Please try again later.");
        setPhase("error");
      });
  }, []);

  const allAnswered =
    questions.length > 0 && questions.every((q) => answers[q.id]);

  const setAnswer = (id: string, val: Answer) => {
    setAnswers((prev) => ({ ...prev, [id]: val }));
  };

  const handleSubmit = async () => {
    if (!allAnswered) return;
    setPhase("submitting");
    try {
      const token = await getToken();
      const res = await fetch(`${API}/api/v1/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ responses: answers }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail ?? "Evaluation failed.");
      }
      const data: EvalResult = await res.json();
      setResult(data);
      setPhase("results");
    } catch (e) {
      setErrorMsg(e instanceof Error ? e.message : "An unknown error occurred.");
      setPhase("error");
    }
  };

  const restart = () => {
    setAnswers({});
    setResult(null);
    setPhase("questions");
    setErrorMsg("");
  };

  return (
    <main className="pt-nav">

      {/* ── Header ──────────────────────────────────────────────── */}
      <section
        style={{
          padding: "5rem 0 4rem",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div className="container-narrow">
          <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>
            Framework Assessment
          </span>
          <h1
            style={{
              fontSize: "clamp(2rem, 4.5vw, 3.5rem)",
              marginBottom: "1.2rem",
            }}
          >
            Evaluate Your Decision
          </h1>
          <p
            style={{
              color: "var(--secondary)",
              lineHeight: 1.85,
              fontSize: "1.1rem",
              maxWidth: "560px",
            }}
          >
            Answer each transformer question as honestly as possible. YES
            confirms alignment. NO marks a gap. PO, Edward de Bono&apos;s
            provocation operator, signals a dimension in movement, neither
            confirmed nor rejected.
          </p>
        </div>
      </section>

      {/* ── Loading ──────────────────────────────────────────────── */}
      {phase === "loading" && (
        <section style={{ padding: "5rem 0" }}>
          <div className="container-narrow" style={{ color: "var(--muted)", fontSize: "0.9rem" }}>
            Loading questions…
          </div>
        </section>
      )}

      {/* ── Error ────────────────────────────────────────────────── */}
      {phase === "error" && (
        <section style={{ padding: "5rem 0" }}>
          <div className="container-narrow">
            <p style={{ color: "var(--red)", marginBottom: "2rem", lineHeight: 1.7 }}>
              {errorMsg}
            </p>
            <button className="btn btn-ghost" onClick={restart}>
              Try Again
            </button>
          </div>
        </section>
      )}

      {/* ── Questionnaire ────────────────────────────────────────── */}
      {phase === "questions" && (
        <section style={{ padding: "4rem 0 2rem" }}>
          <div className="container-narrow">
            {questions.map((q, i) => (
              <div
                key={q.id}
                style={{
                  padding: "2.5rem 0",
                  borderBottom: "1px solid var(--border)",
                }}
              >
                <div style={{ display: "flex", gap: "1.5rem", alignItems: "flex-start" }}>
                  <span
                    style={{
                      fontFamily: "var(--font-garamond)",
                      fontSize: "0.68rem",
                      letterSpacing: "0.14em",
                      color: "var(--gold)",
                      opacity: 0.6,
                      paddingTop: "0.25rem",
                      minWidth: "2rem",
                      flexShrink: 0,
                    }}
                  >
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <div style={{ flex: 1 }}>
                    <p
                      style={{
                        fontSize: "1.05rem",
                        lineHeight: 1.75,
                        color: "var(--fg)",
                        marginBottom: "1.4rem",
                      }}
                    >
                      {q.question}
                    </p>
                    <div style={{ display: "flex", gap: "0.6rem" }}>
                      {(["YES", "NO", "PO"] as Answer[]).map((v) => (
                        <AnswerButton
                          key={v}
                          value={v}
                          selected={answers[q.id] === v}
                          onClick={() => setAnswer(q.id, v)}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Progress indicator */}
            {questions.length > 0 && (
              <div
                style={{
                  padding: "1.5rem 0",
                  display: "flex",
                  alignItems: "center",
                  gap: "1rem",
                }}
              >
                <div
                  style={{
                    flex: 1,
                    height: "2px",
                    background: "var(--border)",
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 0,
                      bottom: 0,
                      background: "var(--gold)",
                      width: `${(Object.keys(answers).length / questions.length) * 100}%`,
                      transition: "width 0.3s ease",
                    }}
                  />
                </div>
                <span
                  style={{
                    fontSize: "0.72rem",
                    color: "var(--muted)",
                    letterSpacing: "0.1em",
                    minWidth: "5rem",
                    textAlign: "right",
                  }}
                >
                  {Object.keys(answers).length} / {questions.length}
                </span>
              </div>
            )}

            <div style={{ padding: "2.5rem 0" }}>
              <button
                className="btn btn-primary"
                onClick={handleSubmit}
                disabled={!allAnswered}
                style={{
                  opacity: allAnswered ? 1 : 0.4,
                  cursor: allAnswered ? "pointer" : "not-allowed",
                }}
              >
                Submit Evaluation
              </button>
              {!allAnswered && (
                <p style={{ color: "var(--muted)", fontSize: "0.82rem", marginTop: "0.75rem" }}>
                  Answer all questions to continue.
                </p>
              )}
            </div>
          </div>
        </section>
      )}

      {/* ── Submitting ───────────────────────────────────────────── */}
      {phase === "submitting" && (
        <section style={{ padding: "5rem 0" }}>
          <div className="container-narrow" style={{ color: "var(--muted)" }}>
            Evaluating responses…
          </div>
        </section>
      )}

      {/* ── Results ──────────────────────────────────────────────── */}
      {phase === "results" && result && (
        <section style={{ padding: "4rem 0 6rem" }}>
          <div className="container-narrow">
            <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>
              Evaluation Complete
            </span>
            <h2
              style={{
                fontSize: "clamp(1.8rem, 3.5vw, 2.8rem)",
                marginBottom: "0.5rem",
              }}
            >
              Your Report
            </h2>
            <p
              style={{
                fontSize: "0.75rem",
                color: "var(--muted)",
                letterSpacing: "0.1em",
                marginBottom: "3rem",
              }}
            >
              Session ID: {result.session_id}
            </p>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, 1fr)",
                gap: 0,
                border: "1px solid var(--border)",
                marginBottom: "3rem",
              }}
            >
              {[
                { label: "YES", count: result.yes_count, color: "var(--green)" },
                { label: "NO", count: result.no_count, color: "var(--red)" },
                { label: "PO", count: result.po_count, color: "var(--gold)" },
              ].map((s, i) => (
                <div
                  key={s.label}
                  style={{
                    padding: "2rem",
                    textAlign: "center",
                    borderRight: i < 2 ? "1px solid var(--border)" : undefined,
                  }}
                >
                  <div
                    style={{
                      fontFamily: "var(--font-playfair)",
                      fontSize: "3rem",
                      color: s.color,
                      lineHeight: 1,
                      marginBottom: "0.4rem",
                    }}
                  >
                    {s.count}
                  </div>
                  <div
                    style={{
                      fontSize: "0.68rem",
                      letterSpacing: "0.2em",
                      textTransform: "uppercase",
                      color: "var(--muted)",
                    }}
                  >
                    {s.label}
                  </div>
                </div>
              ))}
            </div>

            <div
              style={{
                padding: "2rem 2.5rem",
                border: "1px solid var(--border)",
                marginBottom: "2rem",
                background: "var(--surface)",
              }}
            >
              <p
                style={{
                  fontSize: "0.62rem",
                  letterSpacing: "0.22em",
                  textTransform: "uppercase",
                  color: "var(--gold)",
                  marginBottom: "0.9rem",
                  opacity: 0.8,
                }}
              >
                Summary
              </p>
              <p style={{ fontSize: "1.05rem", color: "var(--secondary)", lineHeight: 1.85 }}>
                {result.summary}
              </p>
            </div>

            {result.flags.length > 0 && (
              <div style={{ marginBottom: "2.5rem" }}>
                <p
                  style={{
                    fontSize: "0.62rem",
                    letterSpacing: "0.22em",
                    textTransform: "uppercase",
                    color: "var(--amber)",
                    marginBottom: "0.8rem",
                    opacity: 0.85,
                  }}
                >
                  Dimensions for deeper inquiry
                </p>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem" }}>
                  {result.flags.map((f) => (
                    <span key={f} className="tag tag-amber">
                      {f}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <button className="btn btn-ghost" onClick={restart}>
              Begin New Evaluation
            </button>
          </div>
        </section>
      )}
    </main>
  );
}