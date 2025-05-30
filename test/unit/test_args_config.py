"""
Pruebas unitarias para el módulo args_config.py

Autor: Ashley Yael Montiel Vargas
Fecha: 2025-05-29

Este conjunto de pruebas valida que la configuración del parser de argumentos 
de línea de comandos cumpla con los requisitos de flags obligatorios y 
opcionales, valores por defecto, tipos de datos, y mensajes de ayuda 
informativos.
"""

# =============================================================================
# IMPORTS
# =============================================================================
import os
import sys
import argparse
import pytest
from unittest.mock import patch
from src.args_config import configurar_argumentos

# =============================================================================
# TEST
# =============================================================================

class TestConfigurarArgumentos:
    """Pruebas para la función configurar_argumentos()"""

    def test_parser_basico(self):
        """Se crea un ArgumentParser con descripción adecuada."""
        parser = configurar_argumentos()
        assert isinstance(parser, argparse.ArgumentParser)
        assert "Extrae secuencias FASTA" in parser.description

    def test_argumentos_obligatorios(self):
        """--genome y --peaks deben ser obligatorios y con help correcto."""
        parser = configurar_argumentos()

        act_genome = next(a for a in parser._actions if a.dest == "genome")
        assert act_genome.required is True
        assert "-g" in act_genome.option_strings and "--genome" in act_genome.option_strings
        assert "Archivo FASTA del genoma" in act_genome.help

        act_peaks = next(a for a in parser._actions if a.dest == "peaks")
        assert act_peaks.required is True
        assert "-p" in act_peaks.option_strings and "--peaks" in act_peaks.option_strings
        assert "Archivo TSV con columnas" in act_peaks.help

    def test_argumentos_opcionales_y_defectos(self):
        """Comprueba outdir, logs, verbose y line_length con sus defaults y flags."""
        parser = configurar_argumentos()

        act_out = next(a for a in parser._actions if a.dest == "outdir")
        assert act_out.required is False
        assert act_out.default == "TF_picos_fasta"
        assert "-o" in act_out.option_strings and "--outdir" in act_out.option_strings

        act_logs = next(a for a in parser._actions if a.dest == "logs")
        assert act_logs.default == "logs"
        assert "--logs" in act_logs.option_strings

        act_verbose = next(a for a in parser._actions if a.dest == "verbose")
        assert isinstance(act_verbose, argparse._StoreTrueAction)
        assert act_verbose.default is False
        assert "-v" in act_verbose.option_strings and "--verbose" in act_verbose.option_strings

        act_len = next(a for a in parser._actions if a.dest == "line_length")
        assert act_len.type is int
        assert act_len.default == 80
        assert "-l" in act_len.option_strings and "--line_length" in act_len.option_strings

    @patch("argparse.ArgumentParser.parse_args")
    def test_parseo_completo(self, mock_parse):
        """Simula el parseo de todos los flags y comprueba el Namespace resultante."""
        mock_parse.return_value = argparse.Namespace(
            genome="gen.fa",
            peaks="p.tsv",
            outdir="salida",
            logs="registros",
            verbose=True,
            line_length=60
        )
        parser = configurar_argumentos()
        args = parser.parse_args()
        assert args.genome == "gen.fa"
        assert args.peaks == "p.tsv"
        assert args.outdir == "salida"
        assert args.logs == "registros"
        assert args.verbose is True
        assert args.line_length == 60

    def test_defaults_sin_flags(self, monkeypatch):
        """Si solo se pasan --genome y --peaks, los defaults permanecen."""
        parser = configurar_argumentos()
        monkeypatch.setattr(sys, "argv", ["prog", "--genome", "g.fa", "--peaks", "p.tsv"])
        args = parser.parse_args()
        assert args.outdir == "TF_picos_fasta"
        assert args.logs == "logs"
        assert args.verbose is False
        assert args.line_length == 80

    def test_error_tipo_line_length(self):
        """Debe fallar si --line_length no es entero."""
        parser = configurar_argumentos()
        with pytest.raises(SystemExit):
            parser.parse_args([
                "--genome", "g.fa",
                "--peaks", "p.tsv",
                "--line_length", "no_entero"
            ])

    def test_falla_sin_obligatorios(self):
        """SystemExit si falta --genome o --peaks."""
        parser = configurar_argumentos()
        with pytest.raises(SystemExit):
            parser.parse_args(["--peaks", "p.tsv"])
        with pytest.raises(SystemExit):
            parser.parse_args(["--genome", "g.fa"])

    def test_help_informa_todos(self):
        """El help contiene todos los flags documentados."""
        parser = configurar_argumentos()
        help_text = parser.format_help()
        for flag in ("--genome", "--peaks", "--outdir", "--logs", "--verbose", "--line_length"):
            assert flag in help_text
        assert "Extrae secuencias FASTA" in help_text


