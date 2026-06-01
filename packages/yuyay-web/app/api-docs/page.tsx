const DOCS_URL = "https://yuyay-production-2e45.up.railway.app/docs";

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
              marginBottom: "1.75rem",
            }}
          >
            Interactive REST API documentation for the YUYAY Intelligence API.
            All endpoints, request schemas, and response formats. Deployed on
            Railway.
          </p>
          <a
            href={DOCS_URL}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              fontSize: "0.88rem",
              color: "var(--gold)",
              letterSpacing: "0.04em",
              textDecoration: "none",
              opacity: 0.85,
              transition: "opacity 0.15s ease",
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLElement).style.opacity = "1";
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLElement).style.opacity = "0.85";
            }}
          >
            Open in new tab →
          </a>
        </div>
      </section>

      {/* ── Embedded Swagger UI ──────────────────────────────────── */}
      <iframe
        src={DOCS_URL}
        className="docs-frame"
        title="YUYAY Intelligence API — Swagger UI"
      />
    </main>
  );
}
