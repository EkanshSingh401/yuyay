"use client";

interface Resource {
  category: string;
  items: { label: string; href: string; note: string }[];
}

const resources: Resource[] = [
  {
    category: "Code & Software",
    items: [
      {
        label: "yuyay on TestPyPI",
        href: "https://test.pypi.org/project/yuyay/",
        note: "Python library, FIOS orchestration, archetypes, transformer questions, and evaluation engine.",
      },
      {
        label: "GitHub Repository",
        href: "https://github.com/mitchell-gold/yuyay",
        note: "Source code for the yuyay library, the FastAPI backend, and this Next.js frontend.",
      },
    ],
  },
  {
    category: "API & Documentation",
    items: [
      {
        label: "REST API, Swagger UI",
        href: "https://yuyay-production-2e45.up.railway.app/docs",
        note: "Interactive documentation for all YUYAY Intelligence API endpoints.",
      },
      {
        label: "REST API, ReDoc",
        href: "https://yuyay-production-2e45.up.railway.app/redoc",
        note: "Alternative API reference in ReDoc format.",
      },
      {
        label: "OpenAPI Specification",
        href: "https://yuyay-production-2e45.up.railway.app/openapi.json",
        note: "Machine-readable OpenAPI 3.x schema for the YUYAY Intelligence API.",
      },
    ],
  },
  {
    category: "United Nations Frameworks",
    items: [
      {
        label: "SDG 17, Partnerships for the Goals",
        href: "https://sdgs.un.org/goals/goal17",
        note: "The 17th Sustainable Development Goal: strengthening global partnerships and means of implementation.",
      },
      {
        label: "UNDRIP, UN Declaration on Indigenous Peoples",
        href: "https://www.un.org/development/desa/indigenouspeoples/wp-content/uploads/sites/19/2018/11/UNDRIP_E_web.pdf",
        note: "The landmark 2007 declaration establishing the collective rights of indigenous peoples worldwide.",
      },
      {
        label: "UN Office for Partnerships",
        href: "https://www.un.org/en/unpf",
        note: "The UN body facilitating partnerships with civil society, business, and philanthropic sectors.",
      },
    ],
  },
  {
    category: "Standards & Governance",
    items: [
      {
        label: "ISO 26000, Social Responsibility",
        href: "https://www.iso.org/iso-26000-social-responsibility.html",
        note: "International guidance standard on social responsibility, covering seven core subjects.",
      },
      {
        label: "ISO 26000 Overview (PDF)",
        href: "https://www.iso.org/files/live/sites/isoorg/files/store/en/PUB100260.pdf",
        note: "Free ISO summary document describing the ISO 26000 framework and its application.",
      },
    ],
  },
  {
    category: "Methodological Frameworks",
    items: [
      {
        label: "Edward de Bono, Lateral Thinking",
        href: "https://www.debono.com/lateral-thinking",
        note: "The official de Bono Group resource on lateral thinking, the intellectual foundation of the PO provocation operator.",
      },
      {
        label: "PO: Beyond Yes and No (Book)",
        href: "https://en.wikipedia.org/wiki/Po_(lateral_thinking)",
        note: "Edward de Bono's concept of PO as a formal thinking tool for transcending binary logic.",
      },
      {
        label: "The Co-Creation Wheel",
        href: "/archetypes",
        note: "The twelve-archetype map of human potential at the centre of the YUYAY framework.",
      },
    ],
  },
];

export default function LibraryPage() {
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
            Resources
          </span>
          <h1
            style={{
              fontSize: "clamp(2.2rem, 5vw, 4rem)",
              marginBottom: "1.2rem",
            }}
          >
            Library
          </h1>
          <p
            style={{
              fontSize: "1.1rem",
              color: "var(--secondary)",
              maxWidth: "560px",
              lineHeight: 1.85,
            }}
          >
            Foundational references, source code, and documentation for
            the YUYAY Intelligence Framework and its theoretical lineage.
          </p>
        </div>
      </section>

      {/* ── Resources ────────────────────────────────────────────── */}
      <section style={{ padding: "4rem 0 6rem" }}>
        <div className="container">
          {resources.map((group, gi) => (
            <div
              key={group.category}
              style={{
                marginBottom: gi < resources.length - 1 ? "4rem" : 0,
              }}
            >
              {/* Category heading */}
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "1.5rem",
                  marginBottom: "1.5rem",
                }}
              >
                <span className="eyebrow">{group.category}</span>
                <div
                  style={{
                    flex: 1,
                    height: "1px",
                    background: "var(--border)",
                  }}
                />
              </div>

              {/* Items */}
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: 0,
                  border: "1px solid var(--border)",
                }}
              >
                {group.items.map((item, ii) => (
                  <a
                    key={item.label}
                    href={item.href}
                    target={item.href.startsWith("http") ? "_blank" : undefined}
                    rel={
                      item.href.startsWith("http")
                        ? "noopener noreferrer"
                        : undefined
                    }
                    style={{
                      display: "grid",
                      gridTemplateColumns: "1fr auto",
                      alignItems: "center",
                      gap: "2rem",
                      padding: "1.4rem 1.8rem",
                      borderBottom:
                        ii < group.items.length - 1
                          ? "1px solid var(--border)"
                          : undefined,
                      transition: "background 0.15s ease",
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
                    <div>
                      <p
                        style={{
                          fontFamily: "var(--font-playfair)",
                          fontSize: "1.05rem",
                          color: "var(--gold)",
                          marginBottom: "0.25rem",
                          lineHeight: 1.35,
                        }}
                      >
                        {item.label}
                      </p>
                      <p
                        style={{
                          fontSize: "0.88rem",
                          color: "var(--muted)",
                          lineHeight: 1.6,
                        }}
                      >
                        {item.note}
                      </p>
                    </div>

                    {/* Arrow */}
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 16 16"
                      fill="none"
                      style={{ flexShrink: 0, opacity: 0.35 }}
                      aria-hidden
                    >
                      <path
                        d="M3 8h10M9 4l4 4-4 4"
                        stroke="currentColor"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
