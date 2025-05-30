

# =============================================================================
# IMPORTS
# =============================================================================
import pytest
from pathlib import Path
import textwrap
import os

# =============================================================================
# ARCHIVOS
# =============================================================================
@pytest.fixture(scope="module")
def test_data_dir(tmp_path_factory):
    """Fixture que crea y retorna un directorio con datos de prueba"""
    test_dir = tmp_path_factory.mktemp("test_data")
    
    # Genoma de prueba - Asegurar formato FASTA válido
    genome = test_dir / "test_genome.fa"
    genome.write_text("""
>chr1
ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT
""".strip(), encoding="utf-8")  # .strip() para eliminar espacios en blanco

    # Archivo de picos
    peaks = test_dir / "test_peaks.tsv"
    peaks.write_text("""
TF_name\tPeak_start\tPeak_end
TF1\t0\t4
TF1\t10\t14
TF2\t20\t24
TF_BAD\t100\t200
""".strip(), encoding="utf-8")

    return test_dir