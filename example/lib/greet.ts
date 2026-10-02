/** Saludo personalizado en español. */
export function greet(name: string | null | undefined): string {
  const trimmed = (name ?? "").trim();
  const display = trimmed === "" ? "mundo" : trimmed;
  return `Hola, ${display}`;
}
