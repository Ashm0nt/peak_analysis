"""
Funciones auxiliares para la escritura de archivos FASTA a partir de
secuencias agrupadas por factor de transcripción (TF).

Este módulo ofrece:

  - escribir_fasta(tf_secuencias, output_dir, chars_por_linea)
    --------------------------------------------------------
    Dado un diccionario TF → lista de secuencias de ADN, crea un
    archivo FASTA por cada TF, con headers informativos
    (`>TF_pico_<n>_len=<longitud>`) y líneas de longitud fija.

Autor:
    Ashley Yael Montiel Vargas <yaelmont@lcg.unam.mx>

Fecha:
    29 de mayo de 2025

Versión:
    5.1
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

logger = logging.getLogger(__name__)

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

     # Si no hay nada que procesar
    if not tf_secuencias:
        logger.debug("No hay secuencias.")
        return []


    #Comprobar la ruta de salida de los archivos
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        msg = f"No se pudo crear el directorio '{output_dir}': {e}"
        logger.error(msg)
        raise RuntimeError(msg)
    
    
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
                for i, secuencia in enumerate(secuencias, start=1):
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
        except IOError as e:
            logger.error(f"Error generando archivo para {tf}: {str(e)}")
            raise

    return archivos_generados
