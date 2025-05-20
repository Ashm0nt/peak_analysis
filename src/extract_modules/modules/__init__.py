"""
Paquete modules - Contiene todos los módulos principales del proyecto

Módulos disponibles:
- genome: Manejo de archivos FASTA del genoma
- peaks: Procesamiento de picos ChIP-seq
- io_utils: Utilidades de entrada/salida
- logging_config: Configuración del sistema de logging
- args_config: Configuración de argumentos CLI
"""

from .genome import cargar_genoma
from .peaks import lectura_peaks, extraer_secuencias
from .io_utils import fasta_archivos
from .logging_config import configurar_logging
from .args_config import configurar_argumentos

__all__ = [
    'cargar_genoma',
    'lectura_peaks',
    'extraer_secuencias',
    'fasta_archivos',
    'configurar_logging',
    'configurar_argumentos'
]