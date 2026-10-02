#!/usr/bin/env python3
"""crear_issue no llama a gh hasta --confirmar, y no crea con labels inexistentes."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crear_issue  # noqa: E402


class Resultado:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class TestCrearIssue(unittest.TestCase):
    def test_borrador_incluye_titulo_y_cuerpo(self) -> None:
        texto = crear_issue.armar_borrador("El QR falla", "Sin conexión no valida.", [])
        self.assertIn("El QR falla", texto)
        self.assertIn("Sin conexión no valida.", texto)

    def test_sin_confirmar_no_llama_a_gh(self) -> None:
        llamadas: list[list[str]] = []

        def runner(cmd: list[str]) -> subprocess.CompletedProcess[str]:
            llamadas.append(cmd)
            return Resultado()  # type: ignore[return-value]

        codigo, texto = crear_issue.crear(
            "El QR falla", "Sin conexión no valida.", [], False, runner
        )
        self.assertEqual(codigo, 0)
        self.assertIn("El QR falla", texto)
        self.assertIn("Sin conexión no valida.", texto)
        self.assertEqual(llamadas, [])

    def test_label_inexistente_no_crea_el_issue(self) -> None:
        llamadas: list[list[str]] = []

        def runner(cmd: list[str]) -> subprocess.CompletedProcess[str]:
            llamadas.append(cmd)
            return Resultado(stdout='[{"name":"bug"}]\n')  # type: ignore[return-value]

        codigo, texto = crear_issue.crear(
            "El QR falla",
            "Sin conexión no valida.",
            ["tipo:feature"],
            True,
            runner,
        )
        self.assertEqual(codigo, 1)
        self.assertIn("tipo:feature", texto)
        self.assertEqual(len(llamadas), 1)
        self.assertEqual(llamadas[0][:3], ["gh", "label", "list"])
        self.assertNotIn("issue", [parte for cmd in llamadas for parte in cmd])

    def test_con_confirmar_y_label_existente_crea(self) -> None:
        llamadas: list[list[str]] = []

        def runner(cmd: list[str]) -> subprocess.CompletedProcess[str]:
            llamadas.append(list(cmd))
            if cmd[1] == "label":
                return Resultado(stdout='[{"name":"bug"}]\n')  # type: ignore[return-value]
            return Resultado(stdout="https://github.com/acme/app/issues/12\n")  # type: ignore[return-value]

        codigo, texto = crear_issue.crear(
            "El QR falla", "Sin conexión no valida.", ["bug"], True, runner
        )
        self.assertEqual(codigo, 0)
        self.assertIn("Issue: #12", texto)
        self.assertEqual(llamadas[1][:3], ["gh", "issue", "create"])
        self.assertIn("--label", llamadas[1])
        self.assertIn("bug", llamadas[1])


if __name__ == "__main__":
    unittest.main()
