"""Tests de comportamiento real para greet()."""

from greet import greet


def test_nombre_normal() -> None:
    assert greet("Ana") == "Hola, Ana"


def test_none_saluda_mundo() -> None:
    assert greet(None) == "Hola, mundo"


def test_vacio_saluda_mundo() -> None:
    assert greet("") == "Hola, mundo"


def test_solo_espacios_saluda_mundo() -> None:
    assert greet("   ") == "Hola, mundo"


def test_recorta_espacios() -> None:
    assert greet("  Ana  ") == "Hola, Ana"
