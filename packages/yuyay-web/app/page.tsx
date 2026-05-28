import Link from "next/link";

export default function Home() {
  return (
    <main>
      {/* Navigation */}
      <nav
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          zIndex: 100,
          padding: "1.25rem 3rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderBottom: "1px solid var(--border)",
          background: "rgba(10, 14, 26, 0.95)",
          backdropFilter: "blur(10px)",
        }}
      >
        <span
          style={{
            fontSize: "1.1rem",
            letterSpacing: "0.15em",
            color: "var(--accent-gold)",
            fontFamily: "Georgia, serif",
          }}
        >
          YUYAY
        </span>
        <div style={{ display: "flex", gap: "2.5rem" }}>
          {[
            { href: "/archetypes", label: "Archetypes" },
            { href: "/evaluate", label: "Evaluate" },
            { href: "/about", label: "About" },
            { href: "/library", label: "Library" },
            { href: "/api-docs", label: "API" },
          ].map((link) => (
            <Link
              key={link.href}
              href={link.href}
              style={{
                fontSize: "0.85rem",
                letterSpacing: "0.1em",
                textTransform: "uppercase",
                color: "var(--text-muted)",
                transition: "color 0.2s",
              }}
            >
              {link.label}
            </Link>
          ))}
        </div>
      </nav>

      {/* Hero Section */}
      <section
        style={{
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          textAlign: "center",
          padding: "8rem 2rem 4rem",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Background gradient */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background:
              "radial-gradient(ellipse at 50% 40%, rgba(201,168,76,0.08) 0%, transparent 70%)",
            pointerEvents: "none",
          }}
        />

        <p
          style={{
            fontSize: "0.75rem",
            letterSpacing: "0.3em",
            textTransform: "uppercase",
            color: "var(--accent-gold)",
            marginBottom: "2rem",
          }}
        >
          UN Office of the Future
        </p>

        <h1
          style={{
            fontSize: "clamp(3rem, 8vw, 7rem)",
            fontWeight: 400,
            letterSpacing: "0.05em",
            lineHeight: 1.05,
            marginBottom: "1.5rem",
            color: "var(--foreground)",
          }}
        >
          YUYAY
          <br />
          <span style={{ color: "var(--accent-gold)" }}>Intelligence</span>
        </h1>

        <p
          style={{
            fontSize: "clamp(1rem, 2vw, 1.25rem)",
            color: "var(--text-muted)",
            maxWidth: "600px",
            marginBottom: "1rem",
            lineHeight: 1.8,
          }}
        >
          A multi-dimensional framework for evaluating alignment across
          12 archetype dimensions — integrating wisdom, compassion, and
          planetary consciousness into every decision.
        </p>

        <p
          style={{
            fontSize: "0.85rem",
            color: "var(--text-muted)",
            marginBottom: "3rem",
            letterSpacing: "0.05em",
          }}
        >
          Developed by Mitchell Gold · Integrating SDGs 17, ISO 26000, UNDRIP
        </p>

        <div style={{ display: "flex", gap: "1.5rem", flexWrap: "wrap", justifyContent: "center" }}>
          <Link
            href="/evaluate"
            style={{
              padding: "1rem 2.5rem",
              background: "var(--accent-gold)",
              color: "var(--background)",
              fontSize: "0.85rem",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              fontWeight: 600,
              borderRadius: "2px",
              transition: "background 0.2s",
            }}
          >
            Begin Evaluation
          </Link>
          <Link
            href="/archetypes"
            style={{
              padding: "1rem 2.5rem",
              border: "1px solid var(--border)",
              color: "var(--foreground)",
              fontSize: "0.85rem",
              letterSpacing: "0.15em",
              textTransform: "uppercase",
              borderRadius: "2px",
              transition: "border-color 0.2s",
            }}
          >
            Explore Archetypes
          </Link>
        </div>
      </section>

      {/* What is YUYAY section */}
      <section
        style={{
          padding: "6rem 2rem",
          maxWidth: "900px",
          margin: "0 auto",
          borderTop: "1px solid var(--border)",
        }}
      >
        <p
          style={{
            fontSize: "0.75rem",
            letterSpacing: "0.3em",
            textTransform: "uppercase",
            color: "var(--accent-gold)",
            marginBottom: "1.5rem",
          }}
        >
          The Framework
        </p>
        <h2
          style={{
            fontSize: "clamp(1.8rem, 4vw, 3rem)",
            marginBottom: "2rem",
            color: "var(--foreground)",
          }}
        >
          Intelligence that serves humanity
        </h2>
        <p
          style={{
            fontSize: "1.1rem",
            color: "var(--text-muted)",
            lineHeight: 2,
            marginBottom: "1.5rem",
          }}
        >
          YUYAY is a self-assessment framework that evaluates alignment
          across 12 dimensions of human potential — from Vision and Structure
          to Compassion and Planetary Stewardship. Rooted in the wisdom of
          Edward de Bono&apos;s PO lateral thinking, it provides a structured
          path to decisions that serve the highest purpose.
        </p>
        <p
          style={{
            fontSize: "1.1rem",
            color: "var(--text-muted)",
            lineHeight: 2,
          }}
        >
          Through 10 transformer questions — each answerable as YES, NO, or
          PO — individuals and organizations can evaluate whether their
          decisions demonstrate wisdom, compassion, and long-term thinking
          across the Co-Creation Wheel&apos;s 12 sectors.
        </p>
      </section>

      {/* Three pillars */}
      <section
        style={{
          padding: "4rem 2rem 8rem",
          maxWidth: "1100px",
          margin: "0 auto",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "1px",
            border: "1px solid var(--border)",
          }}
        >
          {[
            {
              number: "12",
              label: "Archetype Dimensions",
              description:
                "From the Seer to the Weaver — each archetype represents a unique gift and shadow in human potential.",
            },
            {
              number: "10",
              label: "Transformer Questions",
              description:
                "Self-reflection questions that evaluate wisdom, compassion, purpose, and planetary consciousness.",
            },
            {
              number: "3",
              label: "LLM Providers",
              description:
                "OpenAI, Anthropic, and Google — queried concurrently through the FIOS orchestration layer.",
            },
          ].map((pillar) => (
            <div
              key={pillar.number}
              style={{
                padding: "3rem 2.5rem",
                background: "var(--surface)",
                borderRight: "1px solid var(--border)",
              }}
            >
              <p
                style={{
                  fontSize: "3.5rem",
                  color: "var(--accent-gold)",
                  fontFamily: "Georgia, serif",
                  lineHeight: 1,
                  marginBottom: "0.5rem",
                }}
              >
                {pillar.number}
              </p>
              <p
                style={{
                  fontSize: "0.75rem",
                  letterSpacing: "0.2em",
                  textTransform: "uppercase",
                  color: "var(--foreground)",
                  marginBottom: "1rem",
                }}
              >
                {pillar.label}
              </p>
              <p
                style={{
                  fontSize: "0.9rem",
                  color: "var(--text-muted)",
                  lineHeight: 1.8,
                }}
              >
                {pillar.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer
        style={{
          borderTop: "1px solid var(--border)",
          padding: "2rem 3rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          color: "var(--text-muted)",
          fontSize: "0.8rem",
          letterSpacing: "0.05em",
        }}
      >
        <span>YUYAY Intelligence Framework © 2026</span>
        <span>UN Office of the Future · Mitchell Gold</span>
      </footer>
    </main>
  );
}