interface Archetype {
  name: string;
  function: string;
  gifts: string[] | string;
  shadow: string[] | string;
}

async function getArchetypes(): Promise<Archetype[]> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1/archetypes/`,
    { next: { revalidate: 3600 } }
  );
  if (!res.ok) return [];
  return res.json();
}

export default async function ArchetypesPage() {
  const archetypes = await getArchetypes();

  return (
    <main style={{ paddingTop: "6rem", minHeight: "100vh" }}>
      {/* Header */}
      <section
        style={{
          padding: "4rem 3rem 3rem",
          borderBottom: "1px solid var(--border)",
          maxWidth: "1200px",
          margin: "0 auto",
        }}
      >
        <p
          style={{
            fontSize: "0.75rem",
            letterSpacing: "0.3em",
            textTransform: "uppercase",
            color: "var(--accent-gold)",
            marginBottom: "1rem",
          }}
        >
          The Framework
        </p>
        <h1
          style={{
            fontSize: "clamp(2rem, 5vw, 4rem)",
            color: "var(--foreground)",
            marginBottom: "1rem",
          }}
        >
          12 Archetypes
        </h1>
        <p
          style={{
            fontSize: "1.1rem",
            color: "var(--text-muted)",
            maxWidth: "600px",
            lineHeight: 1.8,
          }}
        >
          Each archetype represents a unique dimension of human potential —
          with gifts to cultivate and shadows to transcend.
        </p>
      </section>

      {/* Archetypes Grid */}
      <section
        style={{
          padding: "3rem",
          maxWidth: "1200px",
          margin: "0 auto",
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
          gap: "1px",
          background: "var(--border)",
        }}
      >
        {archetypes.map((archetype, index) => (
          <div
            key={archetype.name}
            style={{
              background: "var(--surface)",
              padding: "2.5rem",
              position: "relative",
              transition: "background 0.2s",
            }}
          >
            {/* Number */}
            <span
              style={{
                position: "absolute",
                top: "1.5rem",
                right: "1.5rem",
                fontSize: "0.7rem",
                color: "var(--border)",
                letterSpacing: "0.1em",
              }}
            >
              {String(index + 1).padStart(2, "0")}
            </span>

            {/* Name */}
            <h2
              style={{
                fontSize: "1.3rem",
                color: "var(--accent-gold)",
                marginBottom: "0.5rem",
                fontWeight: 400,
              }}
            >
              {archetype.name}
            </h2>

            {/* Function */}
            <p
              style={{
                fontSize: "0.85rem",
                color: "var(--text-muted)",
                marginBottom: "1.5rem",
                fontStyle: "italic",
                lineHeight: 1.6,
              }}
            >
              {archetype.function}
            </p>

            {/* Gifts */}
            <div style={{ marginBottom: "1rem" }}>
              <p
                style={{
                  fontSize: "0.65rem",
                  letterSpacing: "0.2em",
                  textTransform: "uppercase",
                  color: "var(--success)",
                  marginBottom: "0.5rem",
                }}
              >
                Gifts
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem" }}>
                {(typeof archetype.gifts === "string"
                  ? archetype.gifts.split(",")
                  : archetype.gifts
                ).map((gift) => (
                  <span
                    key={gift}
                    style={{
                      fontSize: "0.75rem",
                      padding: "0.2rem 0.6rem",
                      border: "1px solid rgba(74, 222, 128, 0.2)",
                      borderRadius: "2px",
                      color: "var(--text-muted)",
                    }}
                  >
                    {gift.trim()}
                  </span>
                ))}
              </div>
            </div>

            {/* Shadow */}
            <div>
              <p
                style={{
                  fontSize: "0.65rem",
                  letterSpacing: "0.2em",
                  textTransform: "uppercase",
                  color: "var(--warning)",
                  marginBottom: "0.5rem",
                }}
              >
                Shadow
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem" }}>
                {(typeof archetype.shadow === "string"
                  ? archetype.shadow.split(",")
                  : archetype.shadow
                ).map((shadow) => (
                  <span
                    key={shadow}
                    style={{
                      fontSize: "0.75rem",
                      padding: "0.2rem 0.6rem",
                      border: "1px solid rgba(251, 146, 60, 0.2)",
                      borderRadius: "2px",
                      color: "var(--text-muted)",
                    }}
                  >
                    {shadow.trim()}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
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