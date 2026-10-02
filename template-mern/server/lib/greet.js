/** Saludo personalizado en español (misma semántica que las otras plantillas). */
export function greet(name) {
  const trimmed = (name ?? "").trim();
  return `Hola, ${trimmed === "" ? "mundo" : trimmed}`;
}
