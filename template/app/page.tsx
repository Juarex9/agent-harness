import { formatCurrency } from "@/lib/format";

export default function Home() {
  return (
    <main>
      <h1>Plantilla Harness</h1>
      <p>
        Proyecto Next.js mínimo que cumple el contrato del harness:{" "}
        <code>npm run check</code> corre lint, typecheck y tests.
      </p>
      <p data-testid="precio-ejemplo">
        Precio de ejemplo: {formatCurrency(1999.5)}
      </p>
    </main>
  );
}
