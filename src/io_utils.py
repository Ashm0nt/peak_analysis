"""
Módulo para utilidades de entrada/salida

Autor: Ashley Yael Montiel Vargas
Fecha: 29-Mayo-2025
Versión: 5.0
"""

# =============================================================================
# IMPORTS
# =============================================================================

import os
import logging
from typing import Dict, List

# =============================================================================
# FUNCIONES
# =============================================================================

logger = logging.getLogger('extract_fasta.io_utils')

def escribir_fasta(
        tf_secuencias: Dict[str, List[str]],
        output_dir: str = "TF_picos_fasta",
        chars_por_linea: int = 80
    ) -> List[str]:

    """
    Escribe un archivo FASTA por cada factor de transcripción (TF)
    con sus secuencias de picos, formateadas en líneas de longitud fija.

    Args:
        tf_secuencias (Dict[str, List[str]]):
            Mapa de nombre de TF a lista de secuencias de ADN.
        output_dir (str):
            Ruta al directorio donde se guardarán los FASTA.
            Se crea si no existe.
        chars_por_linea (int):
            Número máximo de caracteres por línea en el FASTA.

    Returns:
        List[str]: Lista de rutas (como cadenas) de los archivos FASTA 
        creados.
    """

    #Comprobar la ruta de salida de los archivos
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        msg = f"No se pudo crear el directorio '{output_dir}': {e}"
        logger.error(msg)
        raise

    archivos_generados: List[str] = []

    #Comprobar que almenos haya secuencias 
    for tf, secuencias in tf_secuencias.items():
        if not secuencias:
            logger.debug("No hay secuencias para '%s'; se omite.", tf)
            continue

        nombre_archivo = os.path.join(output_dir, f"{tf}.fa")
        try:
            with open(
                nombre_archivo, mode="w", encoding="utf-8") as arch_salida:
                for i, secuencia in enumerate(secuencias, star= 1):
                    #Escribir la cabecera de cada secuencia
                    arch_salida.write(
                        f">{tf}_pico_{i}_len={len(secuencia)}\n")
                    for j in range(0, len(secuencia), chars_por_linea):
                        #Dividir la secuencia en líneas de longitud fija
                        arch_salida.write(
                            f"{secuencia[j:j+chars_por_linea]}\n")

            archivos_generados.append(nombre_archivo)
            logger.info(
                "Archivo generado: '%s' ('%d secuencias)",
                nombre_archivo,
                len(secuencias)
            )
        except Exception as e:
            logger.error(f"Error generando archivo para {tf}: {str(e)}")
    
    return archivos_generados
