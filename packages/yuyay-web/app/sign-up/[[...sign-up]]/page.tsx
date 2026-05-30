import { SignUp } from "@clerk/nextjs";

export default function SignUpPage() {
  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        paddingTop: "4.5rem",
        background: "var(--bg)",
      }}
    >
      <SignUp />
    </main>
  );
}