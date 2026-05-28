const BASE = "https://yuyay-production-2e45.up.railway.app";

const endpoints = [
  {
    method: "GET",
    path: "/api/v1/health",
    auth: false,
    description: "Health check. Returns API status and version.",
    response: `{ "status": "ok", "version": "0.1.0" }`,
  },
  {
    method: "GET",
    path: "/api/v1/archetypes/",
    auth: false,
    description:
      "Returns all twelve archetypes with name, function, gifts, and shadow dimensions.",
    response: `[{ "name": "...", "function": "...", "gifts": "...", "shadow": "..." }, ...]`,
  },
  {
    method: "GET",
    path: "/api/v1/transformers/",
    auth: false,
    description: "Returns all transformer questions used in the evaluation questionnaire.",
    response: `[{ "id": "1a", "question": "..." }, ...]`,
  },
  {
    method: "POST",
    path: "/api/v1/auth/login",
    auth: false,
    description:
      "Authenticates a user and returns a JWT access token. Send as multipart/form-data.",
    response: `{ "access_token": "<jwt>", "token_type": "bearer" }`,
  },
  {
    method: "POST",
    path: "/api/v1/evaluate",
    auth: true,
    description:
      'Processes a set of YES/NO/PO responses and returns counts, flags, and a summary. Send as JSON with an Authorization: Bearer <token> header.',
    response: `{ "session_id": "...", "yes_count": 7, "no_count": 1, "po_count": 2, "total": 10, "flags": ["3b"], "summary": "..." }`,
  },
  {
    method: "POST",
    path: "/api/v1/compare",
    auth: true,
    description:
      "Queries multiple LLM providers concurrently with the same prompt and scores each response for YUYAY coherence.",
    response: `{ "prompt": "...", "results": [...], "best_provider": "openai" }`,
  },
];

const methodColor: Record<string, string> = {
  GET: "var(--green)",
  POST: "var(--gold)",
};

export default function ApiDocsPage() {
  return (
    <main className="pt-nav">

      {/* ── Header ──────────────────────────────────────────────── */}
      <section
        style={{
          padding: "5rem 0 4rem",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div className="container">
          <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>
            Developer Reference
          </span>
          <h1
            style={{
              fontSize: "clamp(2.2rem, 5vw, 4rem)",
              marginBottom: "1.2rem",
            }}
          >
            API Documentation
          </h1>
          <p
            style={{
              fontSize: "1.1rem",
              color: "var(--secondary)",
              maxWidth: "580px",
              lineHeight: 1.85,
              marginBottom: "2rem",
            }}
          >
            REST API for the YUYAY Intelligence Framework. Base URL:{" "}
            <code
              style={{
                fontFamily: "monospace",
                fontSize: "0.95rem",
                color: "var(--gold)",
                background: "var(--surface)",
                padding: "0.1rem 0.4rem",
                borderRadius: "2px",
              }}
            >
              {BASE}
            </code>
          </p>
          <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
            <a
              href={`${BASE}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary"
            >
              Open Swagger UI
            </a>
            <a
              href={`${BASE}/redoc`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-ghost"
            >
              Open ReDoc
            </a>
          </div>
        </div>
      </section>

      {/* ── Authentication note ──────────────────────────────────── */}
      <section
        style={{
          padding: "3rem 0",
          borderBottom: "1px solid var(--border)",
          background: "var(--surface)",
        }}
      >
        <div className="container-narrow">
          <p
            style={{
              fontSize: "0.68rem",
              letterSpacing: "0.22em",
              textTransform: "uppercase",
              color: "var(--gold)",
              marginBottom: "0.75rem",
              opacity: 0.8,
            }}
          >
            Authentication
          </p>
          <p
            style={{
              fontSize: "1rem",
              color: "var(--secondary)",
              lineHeight: 1.85,
              marginBottom: "1rem",
            }}
          >
            Protected endpoints require a JWT token obtained from{" "}
            <code
              style={{
                fontFamily: "monospace",
                fontSize: "0.9rem",
                color: "var(--fg)",
              }}
            >
              POST /api/v1/auth/login
            </code>
            . Submit credentials as{" "}
            <code
              style={{
                fontFamily: "monospace",
                fontSize: "0.9rem",
                color: "var(--fg)",
              }}
            >
              multipart/form-data
            </code>{" "}
            and include the returned token as:
          </p>
          <pre
            style={{
              background: "var(--surface-2)",
              border: "1px solid var(--border-2)",
              padding: "1rem 1.4rem",
              fontSize: "0.85rem",
              color: "var(--secondary)",
              fontFamily: "monospace",
              lineHeight: 1.7,
              overflowX: "auto",
              borderRadius: "1px",
            }}
          >
            {`Authorization: Bearer <your_access_token>`}
          </pre>
        </div>
      </section>

      {/* ── Endpoints ────────────────────────────────────────────── */}
      <section style={{ padding: "4rem 0 6rem" }}>
        <div className="container">
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "1.5rem",
              marginBottom: "2rem",
            }}
          >
            <span className="eyebrow">Endpoints</span>
            <div
              style={{ flex: 1, height: "1px", background: "var(--border)" }}
            />
          </div>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 0,
              border: "1px solid var(--border)",
            }}
          >
            {endpoints.map((ep, i) => (
              <div
                key={ep.path}
                style={{
                  padding: "2rem 2.2rem",
                  borderBottom:
                    i < endpoints.length - 1
                      ? "1px solid var(--border)"
                      : undefined,
                }}
              >
                {/* Method + Path */}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "1rem",
                    marginBottom: "0.75rem",
                    flexWrap: "wrap",
                  }}
                >
                  <span
                    style={{
                      fontFamily: "monospace",
                      fontSize: "0.72rem",
                      letterSpacing: "0.12em",
                      color: methodColor[ep.method] ?? "var(--fg)",
                      fontWeight: 700,
                      minWidth: "3rem",
                    }}
                  >
                    {ep.method}
                  </span>
                  <code
                    style={{
                      fontFamily: "monospace",
                      fontSize: "0.95rem",
                      color: "var(--fg)",
                    }}
                  >
                    {ep.path}
                  </code>
                  {ep.auth && (
                    <span
                      style={{
                        fontSize: "0.62rem",
                        letterSpacing: "0.14em",
                        textTransform: "uppercase",
                        color: "var(--amber)",
                        border: "1px solid rgba(224,144,80,0.3)",
                        padding: "0.1rem 0.45rem",
                        borderRadius: "1px",
                      }}
                    >
                      Auth Required
                    </span>
                  )}
                </div>

                {/* Description */}
                <p
                  style={{
                    fontSize: "0.95rem",
                    color: "var(--muted)",
                    lineHeight: 1.75,
                    marginBottom: "1rem",
                    maxWidth: "680px",
                  }}
                >
                  {ep.description}
                </p>

                {/* Sample response */}
                <pre
                  style={{
                    background: "var(--surface)",
                    border: "1px solid var(--border-2)",
                    padding: "0.9rem 1.2rem",
                    fontSize: "0.78rem",
                    color: "var(--secondary)",
                    fontFamily: "monospace",
                    lineHeight: 1.65,
                    overflowX: "auto",
                    borderRadius: "1px",
                  }}
                >
                  {ep.response}
                </pre>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Embedded Swagger ─────────────────────────────────────── */}
      <section
        style={{
          borderTop: "1px solid var(--border)",
        }}
      >
        <div
          className="container"
          style={{
            padding: "2.5rem 3rem 1.5rem",
          }}
        >
          <span className="eyebrow" style={{ marginBottom: "0.8rem" }}>
            Interactive Console
          </span>
          <p
            style={{
              fontSize: "0.9rem",
              color: "var(--muted)",
              marginBottom: "1.2rem",
            }}
          >
            Live Swagger UI, try any endpoint directly in the browser.
          </p>
        </div>
        <iframe
          src={`${BASE}/docs`}
          className="docs-frame"
          title="YUYAY API, Swagger UI"
        />
      </section>
    </main>
  );
}
