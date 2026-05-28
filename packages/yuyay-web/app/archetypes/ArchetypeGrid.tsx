"use client";

interface Archetype {
  name: string;
  function: string;
  gifts: string[] | string;
  shadow: string[] | string;
}

function splitField(v: string[] | string): string[] {
  if (Array.isArray(v)) return v.map((s) => s.trim()).filter(Boolean);
  return v.split(",").map((s) => s.trim()).filter(Boolean);
}

export default function ArchetypeGrid({
  archetypes,
}: {
  archetypes: Archetype[];
}) {
  return (
    <section
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
        gap: 0,
        borderBottom: "1px solid var(--border)",
      }}
    >
      {archetypes.map((archetype, index) => {
        const gifts = splitField(archetype.gifts);
        const shadows = splitField(archetype.shadow);

        return (
          <article
            key={archetype.name}
            style={{
              padding: "2.5rem",
              borderRight: "1px solid var(--border)",
              borderBottom: "1px solid var(--border)",
              position: "relative",
              transition: "background 0.2s ease",
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLElement).style.background =
                "var(--surface)";
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLElement).style.background =
                "transparent";
            }}
          >
            <span
              style={{
                position: "absolute",
                top: "1.4rem",
                right: "1.6rem",
                fontFamily: "var(--font-garamond)",
                fontSize: "0.65rem",
                letterSpacing: "0.1em",
                color: "var(--border-2)",
              }}
            >
              {String(index + 1).padStart(2, "0")}
            </span>

            <h2
              style={{
                fontFamily: "var(--font-playfair)",
                fontSize: "1.35rem",
                color: "var(--gold)",
                marginBottom: "0.4rem",
                fontWeight: 400,
              }}
            >
              {archetype.name}
            </h2>

            <p
              style={{
                fontSize: "0.92rem",
                color: "var(--muted)",
                fontStyle: "italic",
                lineHeight: 1.6,
                marginBottom: "1.5rem",
              }}
            >
              {archetype.function}
            </p>

            <hr className="rule" style={{ marginBottom: "1.4rem" }} />

            <div style={{ marginBottom: "1rem" }}>
              <p
                style={{
                  fontSize: "0.62rem",
                  letterSpacing: "0.22em",
                  textTransform: "uppercase",
                  color: "var(--green)",
                  marginBottom: "0.55rem",
                  opacity: 0.85,
                }}
              >
                Gifts
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "0.35rem" }}>
                {gifts.map((g) => (
                  <span key={g} className="tag tag-green">
                    {g}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <p
                style={{
                  fontSize: "0.62rem",
                  letterSpacing: "0.22em",
                  textTransform: "uppercase",
                  color: "var(--amber)",
                  marginBottom: "0.55rem",
                  opacity: 0.85,
                }}
              >
                Shadow
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "0.35rem" }}>
                {shadows.map((s) => (
                  <span key={s} className="tag tag-amber">
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </article>
        );
      })}
    </section>
  );
}