import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Kiln — Autonomous Software Factory",
  description: "Build, attack, repair, and independently verify software.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
