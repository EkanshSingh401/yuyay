export default function AboutPage() {
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
            The Framework
          </span>
          <h1
            style={{
              fontSize: "clamp(2.2rem, 5vw, 4rem)",
              marginBottom: "1.2rem",
            }}
          >
            About YUYAY
          </h1>
          <p
            style={{
              fontSize: "1.1rem",
              color: "var(--secondary)",
              lineHeight: 1.85,
            }}
          >
            A framework rooted in indigenous wisdom, systems thinking,
            and the conviction that intelligence must serve life.
          </p>
        </div>
      </section>

      {/* ── The Name ─────────────────────────────────────────────── */}
      <section
        style={{
          padding: "5.5rem 0",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div
          className="container"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1.8fr",
            gap: "5rem",
            alignItems: "start",
          }}
        >
          <div>
            <span className="eyebrow" style={{ marginBottom: "1rem" }}>
              Etymology
            </span>
            <h2
              style={{
                fontSize: "clamp(1.6rem, 3vw, 2.2rem)",
              }}
            >
              The Name
            </h2>
          </div>
          <div>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
                marginBottom: "1.4rem",
              }}
            >
              YUYAY comes from the Quechua language — the living tongue
              of the Andean peoples — where it carries the meaning of
              thought, knowledge, and wisdom held in relation to community
              and the natural world.
            </p>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
                marginBottom: "1.4rem",
              }}
            >
              Quechua was spoken across the Inca Empire, one of the most
              sophisticated civilisations in recorded history — one built
              on collective intelligence, reciprocity, and ecological
              stewardship. In naming this framework YUYAY, Mitchell Gold
              acknowledges that the intelligence the world needs is not
              new. It is ancient.
            </p>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
              }}
            >
              This choice of name also honours the United Nations
              Declaration on the Rights of Indigenous Peoples (UNDRIP),
              which YUYAY explicitly integrates as one of its foundational
              governance standards.
            </p>
          </div>
        </div>
      </section>

      {/* ── Mitchell Gold ────────────────────────────────────────── */}
      <section
        style={{
          padding: "5.5rem 0",
          borderBottom: "1px solid var(--border)",
          background: "var(--surface)",
        }}
      >
        <div
          className="container"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1.8fr",
            gap: "5rem",
            alignItems: "start",
          }}
        >
          <div>
            <span className="eyebrow" style={{ marginBottom: "1rem" }}>
              The Creator
            </span>
            <h2
              style={{
                fontSize: "clamp(1.6rem, 3vw, 2.2rem)",
              }}
            >
              Mitchell Gold
            </h2>
          </div>
          <div>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
                marginBottom: "1.4rem",
              }}
            >
              Mitchell Gold is a systems thinker, educator, and designer
              of frameworks for collective intelligence. His work sits at
              the intersection of organisational development, social
              innovation, and planetary governance — drawing on decades of
              direct engagement with communities, institutions, and
              decision-makers across five continents.
            </p>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
                marginBottom: "1.4rem",
              }}
            >
              The YUYAY framework emerged from a recognition that existing
              decision-making tools — however sophisticated — tend to
              optimise for efficiency rather than alignment. Mitchell set
              out to create something different: an evaluative lens that
              holds the full complexity of human potential, and asks
              whether any given decision honours it.
            </p>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
              }}
            >
              His work is undertaken in collaboration with the UN Office
              of the Future, an initiative dedicated to long-range
              thinking, civilisational resilience, and the design of
              institutions adequate to the challenges of the coming
              century.
            </p>
          </div>
        </div>
      </section>

      {/* ── UN Office of the Future ──────────────────────────────── */}
      <section
        style={{
          padding: "5.5rem 0",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div
          className="container"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1.8fr",
            gap: "5rem",
            alignItems: "start",
          }}
        >
          <div>
            <span className="eyebrow" style={{ marginBottom: "1rem" }}>
              Institution
            </span>
            <h2
              style={{
                fontSize: "clamp(1.6rem, 3vw, 2.2rem)",
              }}
            >
              UN Office of the Future
            </h2>
          </div>
          <div>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
                marginBottom: "1.4rem",
              }}
            >
              The UN Office of the Future operates as a strategic foresight
              and design initiative within the United Nations system. Its
              mandate is to develop frameworks, tools, and governance
              innovations capable of addressing the long-term challenges
              that current international institutions were not designed
              to handle.
            </p>
            <p
              style={{
                fontSize: "1.1rem",
                color: "var(--secondary)",
                lineHeight: 1.9,
              }}
            >
              YUYAY represents one of its flagship framework contributions
              — a practical instrument for evaluating whether decisions made
              by organisations, governments, and individuals are coherent
              with humanity&apos;s highest stated values and international
              commitments.
            </p>
          </div>
        </div>
      </section>

      {/* ── Methodology ──────────────────────────────────────────── */}
      <section style={{ padding: "5.5rem 0" }}>
        <div className="container" style={{ marginBottom: "3.5rem" }}>
          <span className="eyebrow" style={{ marginBottom: "1rem" }}>
            Methodology
          </span>
          <h2
            style={{
              fontSize: "clamp(1.6rem, 3vw, 2.2rem)",
              maxWidth: "480px",
            }}
          >
            Theoretical Foundations
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
              gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
              gap: 0,
            }}
          >
            {[
              {
                title: "Edward de Bono — PO",
                body: "The PO provocation operator — a tool for lateral thinking that suspends binary judgement and creates space for creative alternatives. PO is the third response in the YUYAY questionnaire: neither yes nor no, but a mark of movement.",
              },
              {
                title: "SDG 17 — Partnerships for the Goals",
                body: "The 17th Sustainable Development Goal calls for the global partnerships, coherent policy frameworks, and multi-stakeholder engagement necessary to achieve the remaining 16. YUYAY embeds SDG 17 as a structural commitment to relational and systemic thinking.",
              },
              {
                title: "ISO 26000 — Social Responsibility",
                body: "The international standard for organisational social responsibility defines core subjects including human rights, labour practices, environmental care, fair operating practices, consumer issues, and community involvement. YUYAY uses ISO 26000 as a benchmark for the Shadow dimensions of each archetype.",
              },
              {
                title: "UNDRIP — Indigenous Rights",
                body: "The United Nations Declaration on the Rights of Indigenous Peoples enshrines the rights of indigenous peoples to their lands, cultures, identities, and knowledge systems. YUYAY recognises indigenous epistemology — including Quechua concepts of reciprocity and relational knowledge — as foundational.",
              },
            ].map((item, i) => (
              <div
                key={item.title}
                style={{
                  padding: "2.8rem 2.5rem",
                  borderRight:
                    i < 3 ? "1px solid var(--border)" : undefined,
                }}
              >
                <h3
                  style={{
                    fontFamily: "var(--font-playfair)",
                    fontSize: "1.05rem",
                    color: "var(--gold)",
                    marginBottom: "1rem",
                    fontWeight: 400,
                    lineHeight: 1.35,
                  }}
                >
                  {item.title}
                </h3>
                <p
                  style={{
                    fontSize: "0.95rem",
                    color: "var(--muted)",
                    lineHeight: 1.85,
                  }}
                >
                  {item.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
