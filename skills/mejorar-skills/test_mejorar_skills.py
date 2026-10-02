#!/usr/bin/env python3
"""Señales, retros y el PR draft no llaman a gh ni aflojan controles sin confirmación."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import abrir_pr  # noqa: E402
import retro  # noqa: E402
import senales  # noqa: E402


class Resultado:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


REPO = json.dumps(
    {"nameWithOwner": "acme/app", "defaultBranchRef": {"name": "main"}}
)


class TestSenales(unittest.TestCase):
    def test_retros_despues_de_la_marca(self) -> None:
        comentarios = [
            {"body": "vieja", "created_at": "2026-09-01T00:00:00Z", "user": {"login": "a"}},
            {
                "body": "listo\n<!-- mejorar-skills: consolidado -->",
                "created_at": "2026-09-02T00:00:00Z",
                "user": {"login": "a"},
            },
            {
                "body": "nueva",
                "created_at": "2026-09-03T00:00:00Z",
                "user": {"login": "b"},
                "html_url": "https://github.com/acme/app/issues/1#issuecomment-9",
            },
        ]
        nuevas = senales.retros_nuevas(comentarios)
        self.assertEqual(len(nuevas), 1)
        self.assertEqual(nuevas[0]["body"], "nueva")

    def test_la_rama_por_defecto_no_entra_y_el_resto_se_agrupa(self) -> None:
        runs = [
            {
                "headBranch": "main",
                "workflowName": "CI",
                "displayTitle": "en main",
                "createdAt": "2026-10-01T00:00:00Z",
                "url": "http://ci/main",
            },
            {
                "headBranch": "feat/a",
                "workflowName": "CI",
                "displayTitle": "uno",
                "createdAt": "2026-10-01T00:00:00Z",
                "url": "http://ci/1",
            },
            {
                "headBranch": "feat/b",
                "workflowName": "CI",
                "displayTitle": "dos",
                "createdAt": "2026-10-02T00:00:00Z",
                "url": "http://ci/2",
            },
            {
                "headBranch": "feat/c",
                "workflowName": "Docs",
                "displayTitle": "docs",
                "createdAt": "2026-09-01T00:00:00Z",
                "url": "http://ci/viejo",
            },
        ]
        grupos = senales.fallas_de_agentes(runs, "main", "2026-09-15T00:00:00Z")
        self.assertNotIn("main", {run["headBranch"] for lista in grupos.values() for run in lista})
        self.assertEqual(len(grupos["CI"]), 2)
        self.assertNotIn("Docs", grupos)
        texto = senales._texto_fallas(grupos)
        self.assertIn("2 falla(s) en 2 rama(s)", texto)

    def test_gh_sin_auth_sale_1(self) -> None:
        def runner(cmd: list[str]) -> subprocess.CompletedProcess[str]:
            return Resultado(returncode=1, stderr="auth")  # type: ignore[return-value]

        codigo, texto = senales.juntar(desde="2026-09-01T00:00:00Z", runner=runner, git=runner)
        self.assertEqual(codigo, 1)
        self.assertIn("auth", texto)


class TestRetro(unittest.TestCase):
    def _runner(self, issues: str, llamadas: list[list[str]]):
        def runner(cmd: list[str]) -> subprocess.CompletedProcess[str]:
            llamadas.append(list(cmd))
            if cmd[:3] == ["gh", "repo", "view"]:
                return Resultado(stdout=REPO)  # type: ignore[return-value]
            if cmd[:3] == ["gh", "issue", "list"]:
                return Resultado(stdout=issues)  # type: ignore[return-value]
            if cmd[:3] == ["gh", "issue", "create"]:
                return Resultado(stdout="https://github.com/acme/app/issues/7\n")  # type: ignore[return-value]
            return Resultado()  # type: ignore[return-value]

        return runner

    def test_sin_confirmar_no_crea_el_issue(self) -> None:
        llamadas: list[list[str]] = []
        codigo, texto = retro.enviar(
            "desvío: ninguno", False, self._runner("[]", llamadas)
        )
        self.assertEqual(codigo, 0)
        self.assertIn(senales.TITULO, texto)
        self.assertIn("desvío: ninguno", texto)
        self.assertFalse(any(cmd[:3] == ["gh", "issue", "create"] for cmd in llamadas))

    def test_con_confirmar_crea_fija_y_comenta(self) -> None:
        llamadas: list[list[str]] = []
        codigo, _ = retro.enviar(
            "desvío: el mapa", True, self._runner("[]", llamadas)
        )
        self.assertEqual(codigo, 0)
        self.assertEqual(llamadas[2][:3], ["gh", "issue", "create"])
        self.assertEqual(llamadas[3][:3], ["gh", "issue", "pin"])
        self.assertEqual(llamadas[4][:3], ["gh", "issue", "comment"])

    def test_issue_existente_solo_comenta(self) -> None:
        llamadas: list[list[str]] = []
        lista = json.dumps([{"number": 3, "title": senales.TITULO}])
        codigo, texto = retro.enviar(
            "desvío: ninguno", False, self._runner(lista, llamadas)
        )
        self.assertEqual(codigo, 0)
        self.assertIn("#3", texto)
        self.assertTrue(any(cmd[:3] == ["gh", "issue", "comment"] for cmd in llamadas))
        self.assertFalse(any(cmd[:3] == ["gh", "issue", "create"] for cmd in llamadas))


def _estado(**cambios: object) -> abrir_pr.EstadoGit:
    base = abrir_pr.EstadoGit(
        porcelain="",
        rama="mejorar-skills/2026-10-02",
        commits_delante=1,
        archivos_del_diff=["skills/verify-check/SKILL.md"],
        skills_tocadas={"skills/verify-check/SKILL.md": "linea\n" * 10},
        textos={
            "skills/crear-issue/crear_issue.py": "if not confirmar:\n    return 0\n",
            "skills/check-map/check_map.py": "return 2\n",
            "agents/reviewer.md": "corre check-map y crear-issue\n",
        },
    )
    for clave, valor in cambios.items():
        setattr(base, clave, valor)
    return base


class TestAbrirPr(unittest.TestCase):
    def test_sin_confirmar_no_arma_comandos(self) -> None:
        codigo, texto, comandos = abrir_pr.evaluar(
            "Ajustar verify-check",
            "| mapa | #1 | script |",
            "(ninguna)",
            "(ninguno)",
            False,
            _estado(),
            "2026-10-02",
        )
        self.assertEqual(codigo, 0)
        self.assertIn("## Patrones encontrados", texto)
        self.assertIn("## Preguntas para el equipo", texto)
        self.assertIn("## Descartado", texto)
        self.assertEqual(comandos, [])

    def test_sucio_no_hace_push(self) -> None:
        codigo, _, comandos = abrir_pr.evaluar(
            "t", "p", "q", "d", True, _estado(porcelain=" M README.md"), "2026-10-02"
        )
        self.assertEqual(codigo, 1)
        self.assertFalse(any("push" in parte for cmd in comandos for parte in cmd))

    def test_skill_larga_no_hace_push(self) -> None:
        estado = _estado(
            skills_tocadas={"skills/verify-check/SKILL.md": "x\n" * 121},
            archivos_del_diff=["skills/verify-check/SKILL.md"],
        )
        codigo, texto, comandos = abrir_pr.evaluar(
            "t", "p", "q", "d", True, estado, "2026-10-02"
        )
        self.assertEqual(codigo, 1)
        self.assertIn("120", texto)
        self.assertFalse(any(cmd[0:2] == ["git", "push"] for cmd in comandos))
        self.assertFalse(any(cmd[0:3] == ["gh", "pr", "create"] for cmd in comandos))

    def test_invariante_ausente_no_hace_push(self) -> None:
        textos = {
            "skills/crear-issue/crear_issue.py": "return 0\n",
            "skills/check-map/check_map.py": "return 2\n",
            "agents/reviewer.md": "corre check-map y crear-issue\n",
        }
        codigo, texto, comandos = abrir_pr.evaluar(
            "t", "p", "q", "d", True, _estado(textos=textos), "2026-10-02"
        )
        self.assertEqual(codigo, 1)
        self.assertIn("if not confirmar", texto)
        self.assertFalse(any(cmd[0:2] == ["git", "push"] for cmd in comandos))

    def test_con_confirmar_abre_draft_sin_merge(self) -> None:
        codigo, _, comandos = abrir_pr.evaluar(
            "Ajustar verify-check", "p", "q", "d", True, _estado(), "2026-10-02"
        )
        self.assertEqual(codigo, 0)
        self.assertEqual(comandos[0][:3], ["git", "push", "-u"])
        pr = comandos[1]
        self.assertEqual(pr[:3], ["gh", "pr", "create"])
        self.assertIn("--draft", pr)
        self.assertIn("-R", pr)
        self.assertIn("Juarex9/agent-harness", pr)
        self.assertNotIn("merge", pr)

    def test_rama_nueva_no_pushea(self) -> None:
        estado = _estado(rama="main", commits_delante=0, archivos_del_diff=[])
        codigo, _, comandos = abrir_pr.evaluar(
            "t", "p", "q", "d", True, estado, "2026-10-02"
        )
        self.assertEqual(codigo, 1)
        self.assertEqual(comandos, [["git", "switch", "-c", "mejorar-skills/2026-10-02", "origin/main"]])


if __name__ == "__main__":
    unittest.main()
