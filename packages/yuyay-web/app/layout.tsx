import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "YUYAY Intelligence — UN Office of the Future",
  description:
    "A multi-dimensional intelligence framework for evaluating alignment across 12 archetype dimensions. Developed for the UN Office of the Future.",
  keywords: ["YUYAY", "UN", "intelligence framework", "evaluation", "archetypes"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}