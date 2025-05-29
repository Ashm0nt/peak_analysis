"""
Configuración centralizada del sistema de logging

Autor: Ashley Yael Montiel Vargas
Fecha: 01-Mayo-2025
Versión: 
"""
"""
Configuración centralizada del sistema de logging

Autor: Ashley Yael Montiel Vargas
Fecha: 01-Mayo-2025
Versión: 4.0
"""

import os
from datetime import datetime
import logging

def configurar_logging(output_dir="logs", verbose=False):
    """Configura el sistema de logging avanzado
    
    Args:
        output_dir (str): Directorio para los archivos de log
        verbose (bool): Si es True, muestra mensajes DEBUG
    
    Returns:
        logging.Logger: Logger configurado
    """
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logger = logging.getLogger('extract_fasta')
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Eliminar handlers existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Handler para archivo (todos los niveles)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para consola (solo INFO y superior)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger