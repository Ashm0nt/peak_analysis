"""
Pruebas unitarias para el módulo genome.py

Autor: Ashley Yael Montiel Vargas
Fecha: [Fecha actual]
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
    with pytest.raises(FileNotFoundError) as e:
        cargar_genoma(str(tmp_path / "no_existente.fa"))
    assert "Archivo de genoma no encontrado" in str(e.value)

def test_sin_encabezado(tmp_path):
    f = tmp_path / "no_header.fa"
    f.write_text("ACGT\nACGT\n")
    with pytest.raises(ValueError) as e:
        cargar_genoma(str(f))
    assert "Formato FASTA inválido" in str(e.value)

def test_vacio_tras_encabezado(tmp_path):
    f = tmp_path / "empty.fa"
    f.write_text(">chr1\n", encoding="utf-8")
    with pytest.raises(ValueError) as e:
        cargar_genoma(str(f))
    assert "Archivo FASTA vacío" in str(e.value)

def test_encabezados_secundarios(tmp_path):
    f = tmp_path / "multi.fa"
    f.write_text(">chr1\nAAAA\n>sec\nCCCC\n", encoding="utf-8")
    seq = cargar_genoma(str(f))
    assert seq == "AAAACCCC"

def test_lower_to_upper(tmp_path):
    f = tmp_path / "lower.fa"
    f.write_text(">chr1\nacgt\n", encoding="utf-8")
    assert cargar_genoma(str(f)) == "ACGT"

def test_error_codificacion(tmp_path):
    f = tmp_path / "bad_encoding.fa"
    f.write_bytes(b'\xff\xfe\x00A')
    with pytest.raises(ValueError) as e:
        cargar_genoma(str(f))
    assert "Error de codificación" in str(e.value)

def test_permission_error(monkeypatch):
    monkeypatch.setattr(
        "builtins.open", lambda *args, **kw: (
            _ for _ in ()).throw(PermissionError("Permiso")))
    with pytest.raises(ValueError) as e:
        cargar_genoma("dummy.fa")
    assert "Permiso denegado" in str(e.value)
