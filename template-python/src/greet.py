"""Saludo personalizado en español."""

_MUNDO = "mundo"


def greet(name: str | None) -> str:
    """Devuelve 'Hola, <nombre>'. Sin nombre, vacío o solo espacios: 'Hola, mundo'."""
    clean = (name or "").strip()
    return f"Hola, {clean if clean else _MUNDO}"
