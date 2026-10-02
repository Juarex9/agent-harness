import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Plantilla Harness",
  description: "Proyecto Next.js mínimo compatible con el harness de IA",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
