
"""

Este módulo proporciona la función `configurar_logging`, que:

  1. Crea (si no existe) el directorio de logs.
  2. Genera un archivo de log con nombre `log_YYYYMMDD_HHMMSS.log`.
  3. Configura un `FileHandler` para capturar TODOS los niveles (DEBUG+).
  4. Configura un `StreamHandler` para consola (INFO+ por defecto, DEBUG si verbose).
  5. Elimina handlers previos para evitar entradas duplicadas.

Autor:
    Ashley Yael Montiel Vargas <yaelmont@lcg.unam.mx>

Fecha:
    29 de mayo de 2025

Versión:
    4.3
"""

# =============================================================================
# IMPORTS
# =============================================================================

import os
from datetime import datetime
import logging

# =============================================================================
# FUNCIONES
# =============================================================================

def configurar_logging(
        output_dir: str = "logs", verbose: bool = False
) -> logging.Logger:
    
    """Configura el sistema de logging avanzado
    
    Args:
        output_dir (str): Directorio para los archivos de log
        verbose (bool): Si es True, muestra mensajes DEBUG
    
    Returns:
        logging.Logger: Logger configurado
    """

    #Crear directorio de logs si no hay uno
    try: 
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"No se pudo crear '{output_dir}': {e}")     
    
    # 2) Nombre de archivo con timestamp
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(output_dir, f"log_{ts}.log")

    # 3) Logger raíz
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = True

    # 4) Eliminar handlers previos
    for h in list(logger.handlers):
        logger.removeHandler(h)

    # 5) Formateador común
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)

    # 6) FileHandler (DEBUG+)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 7) StreamHandler para consola (INFO+ o DEBUG+ si verbose)
    stream_level = logging.DEBUG if verbose else logging.INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(stream_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger