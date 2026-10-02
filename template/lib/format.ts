/** Formato de moneda en español (Argentina). */
export function formatCurrency(value: number): string {
  if (!Number.isFinite(value)) {
    throw new Error("formatCurrency espera un número finito");
  }
  return new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
  }).format(value);
}
