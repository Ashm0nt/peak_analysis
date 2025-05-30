
# =============================================================================
# IMPORTS
# =============================================================================
import subprocess
import sys
from pathlib import Path
import pytest

# =============================================================================
# TEST
# =============================================================================

CLI_SCRIPT = Path(__file__).parent.parent.parent / "src" / "main.py"

def test_full_integration(test_data_dir, tmp_path):
    """
    Prueba completa del pipeline con:
    - Entradas válidas e inválidas
    - Verificación de outputs y logs
    """
    # Configurar paths
    genome = test_data_dir / "test_genome.fa"
    peaks = test_data_dir / "test_peaks.tsv"
    outdir = tmp_path / "results"
    logdir = tmp_path / "logs"

    # Ejecutar pipeline
    result = subprocess.run(
        [sys.executable, str(CLI_SCRIPT),
         "--genome", str(genome),
         "--peaks", str(peaks),
         "--outdir", str(outdir),
         "--logs", str(logdir),
         "--verbose"],
        capture_output=True,
        text=True
    )

    # Verificaciones
    if result.returncode != 0:
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
    assert result.returncode == 0, f"Pipeline falló con código {result.returncode}"
    
    # Verificar que los archivos se crearon
    assert (outdir / "TF1.fa").exists(), "Archivo TF1.fa no fue creado"
    assert (outdir / "TF2.fa").exists(), "Archivo TF2.fa no fue creado"

@pytest.mark.parametrize("line_len,expected", [
    (10, 10), (60, 60), (5, 5)
])
def test_line_length_config(test_data_dir, tmp_path, line_len, expected):
    """Prueba diferentes configuraciones de line_length"""
    genome = test_data_dir / "test_genome.fa"
    peaks = test_data_dir / "test_peaks.tsv"
    
    result = subprocess.run(
        [sys.executable, str(CLI_SCRIPT),
         "--genome", str(genome),
         "--peaks", str(peaks),
         "--outdir", str(tmp_path / "output"),
         "--line_length", str(line_len)],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    content = (tmp_path / "output" / "TF1.fa").read_text()
    lines = [ln.strip() 
             for ln in content.split("\n") 
             if ln and not ln.startswith(">")]
    assert all(len(ln) <= expected for ln in lines)

