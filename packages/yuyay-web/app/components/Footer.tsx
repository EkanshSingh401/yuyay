import Link from "next/link";

export default function Footer() {
  return (
    <footer className="footer">
      <span>YUYAY Intelligence Framework © 2026</span>
      <span>UN Office of the Future · Mitchell Gold</span>
      <Link href="/privacy" style={{ color: "var(--muted)", fontSize: "0.85rem" }}>
        Privacy Policy
      </Link>
    </footer>
  );
}
