"""
Módulo para utilidades de entrada/salida

Autor: Ashley Yael Montiel Vargas
Fecha: 01-Mayo-2025
Versión: 4.0
"""

import os
import logging

logger = logging.getLogger('extract_fasta.io_utils')

def fasta_archivos(tf_secuencias, output_dir="TF_picos_fasta", chars_linea=80):
    """Escribe archivos FASTA para cada TF
    
    Args:
        tf_secuencias (dict): Secuencias por TF
        output_dir (str): Directorio de salida
        chars_linea (int): Caracteres por línea en FASTA
    
    Returns:
        list: Rutas de archivos generados
    """
    os.makedirs(output_dir, exist_ok=True)
    archivos_generados = []

    for tf, secuencias in tf_secuencias.items():
        if not secuencias:
            continue

        nombre_archivo = os.path.join(output_dir, f"{tf}.fa")
        try:
            with open(nombre_archivo, 'w') as arch_salida:
                for i, secuencia in enumerate(secuencias, 1):
                    arch_salida.write(f">{tf}_pico_{i}_len={len(secuencia)}\n")
                    for j in range(0, len(secuencia), chars_linea):
                        arch_salida.write(f"{secuencia[j:j+chars_linea]}\n")

            archivos_generados.append(nombre_archivo)
            logger.info(f"Archivo generado: {nombre_archivo} ({len(secuencias)} secuencias)")
            
        except Exception as e:
            logger.error(f"Error generando archivo para {tf}: {str(e)}")
    
    return archivos_generados
