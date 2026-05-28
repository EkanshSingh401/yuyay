"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/archetypes", label: "Archetypes" },
  { href: "/evaluate", label: "Evaluate" },
  { href: "/about", label: "About" },
  { href: "/library", label: "Library" },
  { href: "/api-docs", label: "API" },
];

export default function Nav() {
  const pathname = usePathname();

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
    </nav>
  );
}
