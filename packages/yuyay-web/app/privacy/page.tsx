export default function PrivacyPage() {
  return (
    <main className="pt-nav">
      <section style={{ padding: "5rem 0 4rem", borderBottom: "1px solid var(--border)" }}>
        <div className="container-narrow">
          <span className="eyebrow" style={{ marginBottom: "1.2rem" }}>Legal</span>
          <h1 style={{ fontSize: "clamp(2rem, 4.5vw, 3.5rem)", marginBottom: "1.2rem" }}>
            Privacy Policy
          </h1>
          <p style={{ color: "var(--secondary)", lineHeight: 1.85 }}>
            Last updated: June 2026
          </p>
        </div>
      </section>

      <section style={{ padding: "4rem 0 6rem" }}>
        <div className="container-narrow" style={{ maxWidth: "720px" }}>
          {[
            {
              title: "1. Information We Collect",
              body: "We collect information you provide when creating an account (via Clerk authentication), including your email address. When you use the evaluation or query features, we store your session responses and LLM query history associated with your account."
            },
            {
              title: "2. How We Use Your Information",
              body: "Your data is used solely to provide the YUYAY Intelligence Platform service — to store your evaluation sessions, display your query history, and compute analytics. We do not sell your data to third parties."
            },
            {
              title: "3. LLM Providers",
              body: "Queries you submit are sent to third-party LLM providers (Anthropic, OpenAI, Google) to generate responses. Each provider's privacy policy governs how they handle query data. We do not store your API keys."
            },
            {
              title: "4. Data Storage",
              body: "Your data is stored in a PostgreSQL database hosted on Railway (US West region). Authentication is managed by Clerk. We use Sentry for error monitoring, which may capture anonymized diagnostic information."
            },
            {
              title: "5. Data Retention",
              body: "Evaluation sessions and query records are retained for the duration of your account. You may request deletion of your data by contacting us."
            },
            {
              title: "6. Cookies",
              body: "We use cookies solely for authentication purposes via Clerk. We do not use advertising or tracking cookies."
            },
            {
              title: "7. Contact",
              body: "For privacy-related requests, contact the UN Office of the Future via the website."
            },
          ].map((section) => (
            <div key={section.title} style={{ marginBottom: "2.5rem" }}>
              <h2 style={{ fontSize: "1.1rem", fontWeight: 600, marginBottom: "0.8rem" }}>
                {section.title}
              </h2>
              <p style={{ color: "var(--secondary)", lineHeight: 1.85 }}>
                {section.body}
              </p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
