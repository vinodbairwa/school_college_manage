import type { Metadata } from "next";
import { Bricolage_Grotesque, Figtree } from "next/font/google";
import "./globals.css";

const display = Bricolage_Grotesque({
  subsets: ["latin"],
  variable: "--font-display",
});

const body = Figtree({
  subsets: ["latin"],
  variable: "--font-body",
});

export const metadata: Metadata = {
  title: "EduNest Schools",
  description: "Public school and college websites powered by EduNest",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${body.variable}`}>{children}</body>
    </html>
  );
}
