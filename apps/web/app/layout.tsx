import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/Navbar";

export const metadata: Metadata = {
  title: "NikahLens — Privacy-Conscious Matrimonial Discovery Engine",
  description: "A deterministic matrimonial profile discovery and search engine with transparent match reasoning.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 antialiased">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="border-t border-zinc-200 dark:border-zinc-800 py-6 text-center text-xs text-zinc-500">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
            <span>NikahLens © 2026 • Privacy-Conscious Matrimonial Discovery</span>
            <span className="text-[11px] text-zinc-400">
              Zero opaque scores • Transparent Match Reasoning • Safe & Ethical
            </span>
          </div>
        </footer>
      </body>
    </html>
  );
}
