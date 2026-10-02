/** Construye la URL del endpoint de saludo. Función pura: testeable sin navegador. */
export function saludoUrl(name) {
  const clean = (name ?? "").trim();
  if (clean === "") {
    return "/api/saludo";
  }
  return `/api/saludo?${new URLSearchParams({ name: clean }).toString()}`;
}
