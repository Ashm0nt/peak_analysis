"""
Pruebas unitarias para el módulo logging_config.py

Autor: Ashley Yael Montiel Vargas
Fecha: 2025-05-29
"""

import os
import sys
import logging
import pytest
from unittest.mock import patch
from datetime import datetime
from src.logging_config import configurar_logging


class TestConfigurarLogging:
    """Pruebas para la función configurar_logging()"""

    @pytest.fixture(autouse=True)
    def mock_datetime(self):
        """Mockea datetime.now().strftime() para un timestamp fijo."""
        with patch('src.logging_config.datetime') as mock_dt:
            mock_dt.now.return_value.strftime.return_value = "20250530_123456"
            yield

    def test_creacion_directorio_y_archivo(self, tmp_path):
        """Crea el directorio de logs y el archivo con nombre correcto."""
        log_dir = tmp_path / "new_logs"
        assert not log_dir.exists()

        logger = configurar_logging(output_dir=str(log_dir), verbose=False)
        # Directorio debe existir
        assert log_dir.exists() and log_dir.is_dir()

        # Debe haber un archivo log_20250530_123456.log
        log_file = log_dir / "log_20250530_123456.log"
        assert log_file.exists()

    def test_error_al_crear_directorio(self, monkeypatch):
        """Lanza RuntimeError si os.makedirs falla."""
        monkeypatch.setattr('os.makedirs', lambda *args, **kw: (_ for _ in ()).throw(PermissionError("Acceso denegado")))
        with pytest.raises(RuntimeError) as exc:
            configurar_logging(output_dir="/ruta/invalida")
        assert "No se pudo crear" in str(exc.value)
        assert "Acceso denegado" in str(exc.value)

    def test_handlers_configurados(self, tmp_path):
        """Verifica que existan FileHandler y StreamHandler con niveles correctos."""
        logger = configurar_logging(output_dir=str(tmp_path), verbose=False)
        handlers = logger.handlers
        fh = next(h for h in handlers if isinstance(h, logging.FileHandler))
        ch = next(h for h in handlers if isinstance(h, logging.StreamHandler))

        assert fh.level == logging.DEBUG
        assert ch.level == logging.INFO

    def test_verbose_mode(self, tmp_path):
        """En verbose=True, el StreamHandler baja a DEBUG."""
        logger = configurar_logging(output_dir=str(tmp_path), verbose=True)
        ch = next(h for h in logger.handlers if isinstance(h, logging.StreamHandler))
        assert ch.level == logging.DEBUG

    def test_formato_formatter(self, tmp_path):
        """Comprueba que el formatter incluya asctime, name, levelname y message."""
        logger = configurar_logging(output_dir=str(tmp_path), verbose=False)
        fh = next(h for h in logger.handlers if isinstance(h, logging.FileHandler))
        fmt = fh.formatter._fmt
        for token in ("%(asctime)s", "%(name)s", "%(levelname)s", "%(message)s"):
            assert token in fmt

    def test_elimina_handlers_previos(self, tmp_path):
        """Se eliminan handlers ya existentes antes de configurar de nuevo."""
        root = logging.getLogger()
        dummy = logging.NullHandler()
        root.addHandler(dummy)
        assert dummy in root.handlers

        configurar_logging(output_dir=str(tmp_path), verbose=False)
        assert dummy not in root.handlers

    def test_filehandler_utf8(self, tmp_path):
        """El FileHandler debe configurarse con encoding='utf-8'."""
        with patch('logging.FileHandler') as mock_fh:
            configurar_logging(output_dir=str(tmp_path), verbose=False)
            args, kwargs = mock_fh.call_args
            assert kwargs.get('encoding') == 'utf-8'

    def test_logging_en_archivo_y_consola(self, tmp_path, caplog):
        """Prueba emisión real de logs a consola (INFO+) y archivo (DEBUG+)."""
        logger = configurar_logging(output_dir=str(tmp_path), verbose=False)

        caplog.set_level(logging.INFO)
        logger.debug("Debug oculto")
        logger.info("Info visible")
        logger.warning("Warning visible")

        # Consola solo INFO+
        assert "Debug oculto" not in caplog.text
        assert "Info visible" in caplog.text
        assert "Warning visible" in caplog.text

        # Archivo contiene DEBUG+
        log_file = tmp_path / "log_20250530_123456.log"
        content = log_file.read_text(encoding="utf-8")
        for msg in ("Debug oculto", "Info visible", "Warning visible"):
            assert msg in content
