
"""
Pruebas unitarias para el módulo io_utils.py

Este módulo valida el comportamiento de `escribir_fasta()` en distintos
escenarios:
  - Escritura exitosa de FASTA para múltiples TFs.
  - Creación automática del directorio de salida.
  - Omisión cuando no hay secuencias.
  - Formateo de líneas según `chars_por_linea`.
  - Manejo de errores al crear directorios y al escribir archivos.

Autor: Ashley Yael Montiel Vargas
Fecha: 2025-05-29
"""

# =============================================================================
# IMPORTS
# =============================================================================
import os
import sys
import logging
import pytest
from src.io_utils import escribir_fasta


# =============================================================================
# TEST
# =============================================================================

class TestEscribirFasta:
    """Pruebas para la función escribir_fasta()."""

    @pytest.fixture
    def secuencias_prueba(self):
        """
        Secuencias de prueba:
         - TF1: dos secuencias (40 y 20 bases)
         - TF2: una secuencia (100 bases)
         - TF3: ninguna secuencia
        """
        return {
            "TF1": ["ACGT" * 10, "TGCA" * 5],  # 40 y 20 bases
            "TF2": ["ATCG" * 25],               # 100 bases
            "TF3": []                           # Sin secuencias
        }

    def test_escritura_exitosa(self, secuencias_prueba, tmp_path, caplog):
        """Comprueba que se generen correctamente los archivos FASTA."""
        outdir = tmp_path / "output"
        caplog.set_level(logging.INFO)

        resultado = escribir_fasta(
            tf_secuencias=secuencias_prueba,
            output_dir=str(outdir),
            chars_por_linea=20
        )

        # Deben generarse dos archivos: TF1.fa y TF2.fa
        assert len(resultado) == 2
        rutas = set(os.path.basename(p) for p in resultado)
        assert {"TF1.fa", "TF2.fa"} <= rutas
        assert "TF3.fa" not in rutas

        # Verificar contenido de TF1.fa
        ruta_tf1 = next(p for p in resultado if p.endswith("TF1.fa"))
        lineas = open(ruta_tf1, encoding="utf-8").read().splitlines()
        assert lineas[0].startswith(">TF1_pico_1_len=40")
        assert any(len(l) <= 20 for l in lineas[1:])

        # Mensajes de log
        assert "Archivo generado" in caplog.text
        assert "2 secuencias" in caplog.text

    def test_creacion_directorio_automatico(self, secuencias_prueba, tmp_path):
        """Verifica que se cree el directorio de salida si no existe."""
        outdir = tmp_path / "nuevo"
        assert not outdir.exists()

        rutas = escribir_fasta(secuencias_prueba, str(outdir))
        assert outdir.exists()
        assert rutas  # Debe haber al menos un archivo generado

    def test_omitido_si_no_hay_secuencias(self, tmp_path, caplog):
        """Cuando el diccionario está vacío, no genera nada."""
        outdir = tmp_path / "vacio"
        caplog.set_level(logging.DEBUG)

        resultado = escribir_fasta({}, str(outdir))
        assert resultado == []
        assert "No hay secuencias" in caplog.text.lower()

    def test_formato_de_lineas_personalizado(self, tmp_path):
        """Comprueba que las líneas de secuencia respeten chars_por_linea."""
        outdir = tmp_path / "lineas"
        seq = {"TFX": ["ACGT" * 10]}  # 40 bases
        escribir_fasta(seq, str(outdir), chars_por_linea=10)

        lineas = [
            l.strip()
            for l in open(os.path.join(outdir, "TFX.fa"), encoding="utf-8")
            if not l.startswith(">")
        ]
        assert all(len(l) == 10 for l in lineas[:-1])
        assert len(lineas[-1]) <= 10

    def test_error_al_crear_directorio(self, secuencias_prueba, tmp_path, monkeypatch):
        """Simula fallo de permisos al crear el directorio."""
        # Forzar error en os.makedirs
        monkeypatch.setattr("os.makedirs", lambda *args, **kw: (_ for _ in ()).throw(OSError("permiso denegado")))

        with pytest.raises(RuntimeError) as exc:
            escribir_fasta(secuencias_prueba, "/ruta/no_valida")
        assert "No se pudo crear" in str(exc.value)

    def test_error_al_escribir_archivo(self, secuencias_prueba, tmp_path, monkeypatch):
        """Simula fallo de I/O al escribir un archivo FASTA."""
        outdir = tmp_path / "error"
        # Primero creamos el directorio
        outdir.mkdir()
        # Forzar error en open(...)
        monkeypatch.setattr("builtins.open", lambda *args, **kw: (_ for _ in ()).throw(IOError("error de disco")))

        with pytest.raises(IOError) as exc:
            escribir_fasta(secuencias_prueba, str(outdir))
        assert "error de disco" in str(exc.value)

    def test_cabeceras_correctas(self, secuencias_prueba, tmp_path):
        """Verifica que los headers de FASTA tengan el formato exacto."""
        outdir = tmp_path / "header"
        escribir_fasta(secuencias_prueba, str(outdir), chars_por_linea=50)

        ruta = os.path.join(str(outdir), "TF1.fa")
        headers = [l.strip() for l in open(ruta, encoding="utf-8") if l.startswith(">")]
        assert headers == [
            ">TF1_pico_1_len=40",
            ">TF1_pico_2_len=20"
        ]
