"""
Pruebas unitarias para el módulo genome.py

Autor: Ashley Yael Montiel Vargas
Fecha: 2025-05-29

Este conjunto de pruebas valida que el modulo de genoma cumpla con sus 
funcionalidades.
"""

# =============================================================================
# IMPORTS
# =============================================================================
import pytest
import os
import logging
from src.genome import cargar_genoma

# =============================================================================
# TEST
# =============================================================================

def test_archivo_inexistente(tmp_path):
    """Comprueba que el archivo del genoma exista"""
    with pytest.raises(FileNotFoundError) as e:
        cargar_genoma(str(tmp_path / "no_existente.fa"))
    assert "Archivo de genoma no encontrado" in str(e.value)

def test_sin_encabezado(tmp_path):
    """
    Comprueba que el archivo sea válido (encabezado)
    Debe lanzar ValueError si el FASTA no comienza con '>'.
    """
    f = tmp_path / "no_header.fa"
    f.write_text("ACGT\nACGT\n")
    with pytest.raises(ValueError) as e:
        cargar_genoma(str(f))
    assert "Formato FASTA inválido" in str(e.value)

def test_vacio_tras_encabezado(tmp_path):
    """
    Comprueba que el archivo sea mas que el encabezado
    Debe lanzar ValueError con mensaje 'Archivo FASTA vacío'.
    """
    f = tmp_path / "empty.fa"
    f.write_text(">chr1\n", encoding="utf-8")
    with pytest.raises(ValueError) as e:
        cargar_genoma(str(f))
    assert "Archivo FASTA vacío" in str(e.value)

def test_encabezados_secundarios(tmp_path):
    """
    Manejo de multiples encabezados, se ignoran y se concatena la
    secuecnia
    """
    f = tmp_path / "multi.fa"
    f.write_text(">chr1\nAAAA\n>sec\nCCCC\n", encoding="utf-8")
    seq = cargar_genoma(str(f))
    assert seq == "AAAACCCC"

def test_lower_to_upper(tmp_path):
    """
    Convierte la secuencia a mayúsculas.
    """
    f = tmp_path / "lower.fa"
    f.write_text(">chr1\nacgt\n", encoding="utf-8")
    assert cargar_genoma(str(f)) == "ACGT"

def test_error_codificacion(tmp_path):
    """
    Debe lanzar ValueError con mensaje de codificación si falla utf-8.
    """
    f = tmp_path / "bad_encoding.fa"
    f.write_bytes(b'\xff\xfe\x00A')
    with pytest.raises(ValueError) as e:
        cargar_genoma(str(f))
    assert "Error de codificación" in str(e.value)

def test_permission_error(monkeypatch):
    """
    Maneja los permisos del archivo
    Captura PermissionError y lo convierte en ValueError.
    """
    monkeypatch.setattr(
        "builtins.open", lambda *args, **kw: (
            _ for _ in ()).throw(PermissionError("Permiso")))
    with pytest.raises(ValueError) as e:
        cargar_genoma("dummy.fa")
    assert "Permiso denegado" in str(e.value)
