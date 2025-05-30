"""
Pruebas unitarias para el módulo peaks.py

Autor: Ashley Yael Montiel Vargas
Fecha: [Fecha actual]
"""

# =============================================================================
# IMPORTS
# =============================================================================
import pytest
import os
import logging
import pandas as pd
from unittest.mock import patch, mock_open
from src.peaks import lectura_peaks, extraer_secuencias

# =============================================================================
# TEST
# =============================================================================

class TestLecturaPeaks:
    """Pruebas para la función lectura_peaks()"""

    CABECERA = "TF_name\tPeak_start\tPeak_end\n"

    @pytest.fixture
    def archivo_valido(self, tmp_path):
        """Crea un TSV con picos válidos para varios TFs."""
        contenido = (
            self.CABECERA +
            "TF1\t100\t200\n" +
            "TF2\t150\t250\n" +
            "TF1\t300\t400\n"
        )
        ruta = tmp_path / "picos_validos.tsv"
        ruta.write_text(contenido, encoding="utf-8")
        return str(ruta)

    @pytest.fixture
    def archivo_errores(self, tmp_path):
        """Crea un TSV con distintos errores de formato y coordenadas."""
        contenido = (
            self.CABECERA +
            "TF1\t100\t50\n" +      # start >= end
            "TF2\t-10\t20\n" +      # start < 0
            "TF3\tabc\tdef\n" +     # no numérico
            "\t\t\n" +              # campos vacíos
            "TF4\t300\t400\n"       # válido
        )
        ruta = tmp_path / "picos_erroneos.tsv"
        ruta.write_text(contenido, encoding="utf-8")
        return str(ruta)
    
    @pytest.fixture
    def archivo_sin_columnas(self, tmp_path):
        """Crea un TSV sin las columnas Peak_start o Peak_end."""
        contenido = "TF_name\tOtra\nTF1\tdato\n"
        ruta = tmp_path / "picos_sin_columnas.tsv"
        ruta.write_text(contenido, encoding="utf-8")
        return str(ruta)

    def test_lectura_exito(self, archivo_valido, caplog):
        """Lee correctamente un archivo de picos bien formado."""
        caplog.set_level(logging.INFO)
        coords = lectura_peaks(archivo_valido)

        # Deben existir TF1 y TF2
        assert set(coords.keys()) == {"TF1", "TF2"}
        # TF1 tiene dos picos
        assert coords["TF1"] == [(100, 200), (300, 400)]
        # TF2 tiene un pico
        assert coords["TF2"] == [(150, 250)]
        # Mensaje de resumen
        assert "Picos válidos" in caplog.text

    def test_archivo_inexistente(self, tmp_path):
        """Lanza FileNotFoundError si el archivo no existe."""
        ruta = tmp_path / "no_existe.tsv"
        with pytest.raises(FileNotFoundError) as exc:
            lectura_peaks(str(ruta))
        assert str(ruta) in str(exc.value)
        assert "Archivo de picos no encontrado" in str(exc.value)

    def test_columnas_faltantes(self, archivo_sin_columnas):
        """Lanza ValueError al faltar columnas obligatorias."""
        with pytest.raises(ValueError) as exc:
            lectura_peaks(archivo_sin_columnas)
        msg = str(exc.value)
        assert "Columnas faltantes" in msg
        assert "Peak_start" in msg and "Peak_end" in msg

    def test_manejo_errores(self, archivo_errores, caplog):
        """Procesa el TSV con errores y filtra solo TF4 válido."""
        caplog.set_level(logging.WARNING)
        coords = lectura_peaks(archivo_errores)

        # Solo TF4 debe permanecer
        assert set(coords.keys()) == {"TF4"}
        assert coords["TF4"] == [(300, 400)]

        registro = caplog.text.lower()
        # Deben registrarse advertencias para cada tipo de error
        assert "start >= end" in registro
        assert "coordenadas inválidas" in registro or "error de formato" in registro
        assert "campos vacíos" in registro

    def test_archivo_vacio(self, tmp_path):
        """Lanza ValueError si el archivo está vacío."""
        vacio = tmp_path / "vacio.tsv"
        vacio.write_text("", encoding="utf-8")
        with pytest.raises(ValueError) as exc:
            lectura_peaks(str(vacio))
        # Según implementación, puede mencionar formato o columnas faltantes
        assert "Columnas faltantes" in str(exc.value) or "archivo vacío" in str(exc.value).lower()

class TestExtraerSecuencias:
    """Pruebas para la función extraer_secuencias()"""

    @pytest.fixture
    def genoma(self):
        """Retorna una secuencia de 50 bases."""
        return "ACGT" * 12 + "AA"

    @pytest.fixture
    def coords_validas(self):
        """Coordenadas válidas dentro de rango."""
        return {
            "TF1": [(0, 4), (8, 12)],  # ACGT, ACGT
            "TF2": [(4, 8)]            # ACGT
        }

    @pytest.fixture
    def coords_invalidas(self):
        """Coordenadas fuera de rango o invertidas."""
        return {
            "TF1": [(-1, 3), (10, 5), (48, 55)],
            "TF2": [(0, 100)]
        }

    def test_extraccion_valida(self, genoma, coords_validas, caplog):
        """Extrae correctamente todas las secuencias válidas."""
        caplog.set_level(logging.INFO)
        seqs = extraer_secuencias(coords_validas, genoma)
        assert seqs["TF1"] == ["ACGT", "ACGT"]
        assert seqs["TF2"] == ["ACGT"]
        assert "válidos" in caplog.text.lower()

    def test_coordenadas_invalidas(self, genoma, coords_invalidas, caplog):
        """Omitir coordenadas inválidas y registrar advertencia."""
        caplog.set_level(logging.WARNING)
        seqs = extraer_secuencias(coords_invalidas, genoma)
        assert seqs["TF1"] == []
        assert seqs["TF2"] == []
        log = caplog.text.lower()
        assert "coordenadas inválidas" in log
        assert "inválidos" in log

    def test_secuencia_vacia(self):
        """Si el genoma está vacío, no extrae nada."""
        seqs = extraer_secuencias({"TF1": [(0, 4)]}, "")
        assert seqs["TF1"] == []

    def test_limites_genoma(self, genoma):
        """Extrae secuencias en los extremos del genoma sin error."""
        coords = {"TF1": [(0, 4), (46, 50)]}
        seqs = extraer_secuencias(coords, genoma)
        assert seqs["TF1"] == ["ACGT", genoma[46:50]]







