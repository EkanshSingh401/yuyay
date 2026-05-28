import type { Metadata } from "next";
import { Playfair_Display, EB_Garamond } from "next/font/google";
import Nav from "./components/Nav";
import Footer from "./components/Footer";
import "./globals.css";

const playfair = Playfair_Display({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  style: ["normal", "italic"],
  variable: "--font-playfair",
  display: "swap",
});

const garamond = EB_Garamond({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  style: ["normal", "italic"],
  variable: "--font-garamond",
  display: "swap",
});

export const metadata: Metadata = {
  title: "YUYAY Intelligence — UN Office of the Future",
  description:
    "A multi-dimensional intelligence framework evaluating alignment across 12 archetype dimensions. Developed by Mitchell Gold for the UN Office of the Future.",
  keywords: ["YUYAY", "UN", "intelligence framework", "archetypes", "evaluation", "Mitchell Gold"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${playfair.variable} ${garamond.variable}`}>
      <body>
        <Nav />
        {children}
        <Footer />
      </body>
    </html>
  );
}
