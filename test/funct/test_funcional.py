import subprocess
import sys
from pathlib import Path
import pytest

CLI_SCRIPT = Path(__file__).parent.parent.parent / "src" / "main.py"

def test_missing_required_args():
    """Prueba que el CLI falla sin argumentos requeridos"""
    result = subprocess.run(
        [sys.executable, str(CLI_SCRIPT)],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
    assert "error" in result.stderr.lower()
    assert "--genome" in result.stderr
    assert "--peaks" in result.stderr

def test_invalid_args():
    """Prueba manejo de argumentos inválidos"""
    result = subprocess.run(
        [sys.executable, str(CLI_SCRIPT), "--invalid-arg"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
    assert "unrecognized argument" in result.stderr.lower()

def test_help_output():
    """Prueba que el mensaje de ayuda se genera correctamente"""
    result = subprocess.run(
        [sys.executable, str(CLI_SCRIPT), "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Extrae secuencias FASTA" in result.stdout
    assert "--genome" in result.stdout
    assert "--peaks" in result.stdout