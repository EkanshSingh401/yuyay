import ArchetypeGrid from "./ArchetypeGrid";

interface Archetype {
  name: string;
  function: string;
  gifts: string[] | string;
  shadow: string[] | string;
}

async function getArchetypes(): Promise<Archetype[]> {
  try {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/v1/archetypes/`,
      { next: { revalidate: 3600 } }
    );
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export default async function ArchetypesPage() {
  const archetypes = await getArchetypes();

  return (
    <main className="pt-nav">
      <section
        style={{
          padding: "5rem 0 4rem",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <div className="container">
          <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>
            The Co-Creation Wheel
          </span>
          <h1
            style={{
              fontSize: "clamp(2.2rem, 5vw, 4rem)",
              marginBottom: "1.2rem",
            }}
          >
            Twelve Archetypes
          </h1>
          <p
            style={{
              fontSize: "1.1rem",
              color: "var(--secondary)",
              maxWidth: "580px",
              lineHeight: 1.85,
            }}
          >
            Each archetype represents a unique dimension of human potential —
            with gifts to cultivate and shadows to transcend.
          </p>
        </div>
      </section>

      {archetypes.length === 0 ? (
        <section style={{ padding: "6rem 0", textAlign: "center" }}>
          <div className="container">
            <p style={{ color: "var(--muted)", fontSize: "1rem" }}>
              Unable to load archetypes. The API may be temporarily unavailable.
            </p>
          </div>
        </section>
      ) : (
        <ArchetypeGrid archetypes={archetypes} />
      )}
    </main>
  );
}