#!/usr/bin/env python3
"""Comportamiento de check_map: globs y códigos de salida."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_map  # noqa: E402

MAPA_SECRETOS = {
    "sensibles": [{"tipo": "secretos", "rutas": [".env", ".env.local"]}],
}


class TestCheckMap(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        (self.raiz / "docs").mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def escribir(self, data: object) -> None:
        (self.raiz / "docs" / "mapa-agentes.json").write_text(
            json.dumps(data), encoding="utf-8"
        )

    def test_env_anidado_es_sensible(self) -> None:
        self.escribir(MAPA_SECRETOS)
        codigo, texto = check_map.revisar(self.raiz, ["server/.env"])
        self.assertEqual(codigo, 2)
        self.assertIn("secretos", texto)
        self.assertIn("server/.env", texto)

    def test_archivo_normal_no_es_sensible(self) -> None:
        self.escribir(MAPA_SECRETOS)
        codigo, texto = check_map.revisar(self.raiz, ["app/page.tsx"])
        self.assertEqual(codigo, 0)
        self.assertIn("sin rutas sensibles", texto)

    def test_env_example_no_es_sensible(self) -> None:
        self.escribir(MAPA_SECRETOS)
        codigo, _ = check_map.revisar(
            self.raiz, [".env.example", "server/.env.example"]
        )
        self.assertEqual(codigo, 0)

    def test_json_invalido_sale_1(self) -> None:
        (self.raiz / "docs" / "mapa-agentes.json").write_text("{", encoding="utf-8")
        codigo, texto = check_map.revisar(self.raiz, ["app/page.tsx"])
        self.assertEqual(codigo, 1)
        self.assertIn("JSON", texto)

    def test_mapa_ausente_sale_1(self) -> None:
        codigo, texto = check_map.revisar(self.raiz, ["app/page.tsx"])
        self.assertEqual(codigo, 1)
        self.assertIn("no hay", texto)

    def test_glob_doble_asterisco(self) -> None:
        self.escribir(
            {"sensibles": [{"tipo": "auth", "rutas": ["app/api/auth/**"]}]}
        )
        codigo, texto = check_map.revisar(self.raiz, ["app/api/auth/route.ts"])
        self.assertEqual(codigo, 2)
        self.assertIn("auth", texto)
        otro, _ = check_map.revisar(self.raiz, ["app/page.tsx"])
        self.assertEqual(otro, 0)

    def test_main_propaga_el_codigo(self) -> None:
        self.escribir(MAPA_SECRETOS)
        proc = subprocess.run(
            [
                sys.executable,
                str(Path(check_map.__file__).resolve()),
                "--raiz",
                str(self.raiz),
                "server/.env",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("server/.env", proc.stdout)


if __name__ == "__main__":
    unittest.main()
