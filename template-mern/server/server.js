import express from "express";
import { fileURLToPath } from "url";
import { greet } from "./lib/greet.js";

export const app = express();

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.get("/api/saludo", (req, res) => {
  const raw = req.query.name;
  const name = Array.isArray(raw) ? raw[0] : raw;
  // Se devuelve el nombre tal cual en JSON; escapar al mostrar es trabajo del client.
  res.json({ saludo: greet(name ?? null) });
});

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const port = Number(process.env.PORT ?? 3001);
  app.listen(port, () => console.log(`API en http://localhost:${port}`));
}
