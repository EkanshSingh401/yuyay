import Link from "next/link";

export default function Home() {
  return (
    <main className="pt-nav">

      {/* ── Hero ────────────────────────────────────────────────── */}
      <section
        style={{
          minHeight: "calc(100vh - 4.5rem)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          textAlign: "center",
          padding: "6rem 2rem 4rem",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Radial glow */}
        <div
          aria-hidden
          style={{
            position: "absolute",
            inset: 0,
            background:
              "radial-gradient(ellipse 60% 55% at 50% 42%, rgba(201,168,76,0.06) 0%, transparent 70%)",
            pointerEvents: "none",
          }}
        />

        <span className="eyebrow" style={{ marginBottom: "2.5rem" }}>
          UN Office of the Future · Framework Documentation
        </span>

        <h1
          style={{
            fontFamily: "var(--font-playfair)",
            fontSize: "clamp(5rem, 14vw, 12rem)",
            fontWeight: 400,
            letterSpacing: "0.06em",
            lineHeight: 0.95,
            color: "var(--fg)",
            marginBottom: "0.35em",
          }}
        >
          YUYAY
        </h1>

        <p
          style={{
            fontFamily: "var(--font-playfair)",
            fontSize: "clamp(1.4rem, 4vw, 2.8rem)",
            fontWeight: 400,
            fontStyle: "italic",
            color: "var(--gold)",
            letterSpacing: "0.04em",
            marginBottom: "2.5rem",
          }}
        >
          Intelligence
        </p>

        <div className="hero-rule" />

        <p
          style={{
            fontSize: "clamp(1rem, 2vw, 1.2rem)",
            color: "var(--secondary)",
            maxWidth: "580px",
            lineHeight: 1.85,
            marginBottom: "0.75rem",
          }}
        >
          A multi-dimensional framework evaluating alignment across{" "}
          twelve archetype dimensions, integrating wisdom, compassion,
          and planetary consciousness into every decision.
        </p>

        <p
          style={{
            fontSize: "0.8rem",
            color: "var(--muted)",
            letterSpacing: "0.08em",
            marginBottom: "3rem",
          }}
        >
          Developed by Mitchell Gold · Integrating SDGs 17, ISO 26000,
          UNDRIP
        </p>

        <div
          style={{
            display: "flex",
            gap: "1rem",
            flexWrap: "wrap",
            justifyContent: "center",
          }}
        >
          <Link href="/evaluate" className="btn btn-primary">
            Begin Evaluation
          </Link>
          <Link href="/archetypes" className="btn btn-ghost">
            Explore Archetypes
          </Link>
        </div>
      </section>

      {/* ── Stats bar ───────────────────────────────────────────── */}
      <div
        style={{
          borderTop: "1px solid var(--border)",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div
          className="container"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: 0,
          }}
        >
          {[
            { n: "12", label: "Archetype Dimensions" },
            { n: "10", label: "Transformer Questions" },
            { n: "3", label: "LLM Providers" },
          ].map((s, i) => (
            <div
              key={s.n}
              style={{
                padding: "2.5rem 2rem",
                textAlign: "center",
                borderRight:
                  i < 2 ? "1px solid var(--border)" : undefined,
              }}
            >
              <div className="stat-number">{s.n}</div>
              <div
                style={{
                  fontSize: "0.72rem",
                  letterSpacing: "0.18em",
                  textTransform: "uppercase",
                  color: "var(--muted)",
                  marginTop: "0.4rem",
                }}
              >
                {s.label}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── The Framework ────────────────────────────────────────── */}
      <section style={{ padding: "7rem 0" }}>
        <div
          className="container"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1.6fr",
            gap: "5rem",
            alignItems: "start",
          }}
        >
          <div>
            <span className="eyebrow" style={{ marginBottom: "1.5rem" }}>
              The Framework
            </span>
            <h2
              style={{
                fontSize: "clamp(1.8rem, 3.5vw, 2.6rem)",
                color: "var(--fg)",
              }}
            >
              Intelligence that serves humanity
            </h2>
          </div>
          <div>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
                marginBottom: "1.5rem",
              }}
            >
              YUYAY, from the Quechua word for knowledge, is a
              self-assessment framework built on twelve dimensions of
              human potential. From Vision and Structure to Compassion
              and Planetary Stewardship, every decision can be weighed
              against the full spectrum of what it means to act wisely
              in the world.
            </p>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
              }}
            >
              Through ten transformer questions, each answerable as
              YES, NO, or PO, individuals and organisations evaluate
              whether their decisions demonstrate the coherence,
              long-term thinking, and relational intelligence that the
              Co-Creation Wheel demands.
            </p>
          </div>
        </div>
      </section>

      {/* ── PO Lateral Thinking ──────────────────────────────────── */}
      <section
        style={{
          borderTop: "1px solid var(--border)",
          padding: "6rem 0",
          background: "var(--surface)",
        }}
      >
        <div className="container-narrow" style={{ textAlign: "center" }}>
          <span className="eyebrow" style={{ marginBottom: "1.5rem" }}>
            The Third Way
          </span>
          <h2
            style={{
              fontSize: "clamp(2rem, 4vw, 3rem)",
              marginBottom: "1.5rem",
            }}
          >
            Beyond Yes and No
          </h2>
          <p
            style={{
              fontSize: "1.15rem",
              color: "var(--secondary)",
              lineHeight: 1.95,
              maxWidth: "640px",
              marginInline: "auto",
              marginBottom: "1rem",
            }}
          >
            PO is a term coined by Edward de Bono to represent lateral
            thinking, a deliberate provocation that moves beyond binary
            logic. Where YES confirms and NO rejects, PO suspends
            judgement and opens a space for possibility.
          </p>
          <p
            style={{
              fontSize: "1.1rem",
              color: "var(--muted)",
              lineHeight: 1.85,
              maxWidth: "580px",
              marginInline: "auto",
            }}
          >
            In the YUYAY framework, PO marks the dimensions where deeper
            inquiry is warranted, where an answer exists not yet in
            full alignment, but in movement toward it.
          </p>
        </div>
      </section>

      {/* ── Three Pillars ────────────────────────────────────────── */}
      <section
        style={{
          borderTop: "1px solid var(--border)",
          padding: "6rem 0",
        }}
      >
        <div className="container" style={{ marginBottom: "3.5rem" }}>
          <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>
            The Architecture
          </span>
          <h2 style={{ fontSize: "clamp(1.8rem, 3.5vw, 2.6rem)" }}>
            How it works
          </h2>
        </div>

        <div
          style={{
            borderTop: "1px solid var(--border)",
            borderBottom: "1px solid var(--border)",
          }}
        >
          <div
            className="container"
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              gap: 0,
            }}
          >
            {[
              {
                n: "01",
                title: "Select an Archetype",
                body: "Each of the twelve dimensions, from the Seer and the Weaver to the Warrior and the Steward, represents a unique pattern of gifts and shadows in human potential.",
              },
              {
                n: "02",
                title: "Answer Ten Questions",
                body: "The transformer questions probe whether a decision embodies wisdom, compassion, purpose, systemic thinking, and planetary consciousness. Each answer is YES, NO, or PO.",
              },
              {
                n: "03",
                title: "Receive Your Report",
                body: "FIOS, the Framework Intelligence Orchestration System, evaluates responses across OpenAI, Anthropic, and Google concurrently, scoring coherence against the YUYAY framework.",
              },
            ].map((p, i) => (
              <div
                key={p.n}
                style={{
                  padding: "3rem 2.5rem",
                  borderRight:
                    i < 2 ? "1px solid var(--border)" : undefined,
                }}
              >
                <div
                  style={{
                    fontFamily: "var(--font-garamond)",
                    fontSize: "0.68rem",
                    letterSpacing: "0.2em",
                    color: "var(--gold)",
                    marginBottom: "1.2rem",
                    opacity: 0.8,
                  }}
                >
                  {p.n}
                </div>
                <h3
                  style={{
                    fontSize: "1.25rem",
                    fontFamily: "var(--font-playfair)",
                    marginBottom: "1rem",
                    color: "var(--fg)",
                  }}
                >
                  {p.title}
                </h3>
                <p
                  style={{
                    fontSize: "0.97rem",
                    color: "var(--muted)",
                    lineHeight: 1.85,
                  }}
                >
                  {p.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ─────────────────────────────────────────────────── */}
      <section
        style={{
          padding: "7rem 2rem",
          textAlign: "center",
          borderTop: "1px solid var(--border)",
        }}
      >
        <span className="eyebrow" style={{ marginBottom: "1.5rem" }}>
          Framework Assessment
        </span>
        <h2
          style={{
            fontSize: "clamp(1.8rem, 3.5vw, 2.8rem)",
            marginBottom: "1.2rem",
          }}
        >
          Begin your evaluation
        </h2>
        <p
          style={{
            color: "var(--muted)",
            maxWidth: "480px",
            marginInline: "auto",
            marginBottom: "2.5rem",
            lineHeight: 1.8,
          }}
        >
          Apply the YUYAY framework to any decision, initiative, or
          strategic question. The assessment takes approximately ten
          minutes.
        </p>
        <Link href="/evaluate" className="btn btn-primary">
          Start Assessment
        </Link>
      </section>
    </main>
  );
}
