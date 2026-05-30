"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth, UserButton } from "@clerk/nextjs";

const links = [
  { href: "/archetypes", label: "Archetypes" },
  { href: "/evaluate", label: "Evaluate" },
  { href: "/about", label: "About" },
  { href: "/library", label: "Library" },
  { href: "/api-docs", label: "API" },
];

export default function Nav() {
  const pathname = usePathname();
  const { isSignedIn } = useAuth();

  return (
    <nav className="nav">
      <Link href="/" className="nav-brand">
        YUYAY
      </Link>
      <div className="nav-links">
        {links.map(({ href, label }) => (
          <Link
            key={href}
            href={href}
            className={`nav-link${pathname === href ? " active" : ""}`}
          >
            {label}
          </Link>
        ))}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
        {isSignedIn ? (
          <UserButton />
        ) : (
          <>
            <Link href="/sign-in" className="btn btn-ghost">
              Sign In
            </Link>
            <Link href="/sign-up" className="btn btn-primary">
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
