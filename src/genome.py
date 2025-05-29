"""
Módulo para manejo de archivos FASTA de genoma

Autor: Ashley Yael Montiel Vargas
Fecha: 01-Mayo-2025
Versión: 4.0
"""

import os
import logging

logger = logging.getLogger('extract_fasta.genome')

def cargar_genoma(genoma_path):
    """Carga el genoma desde un archivo FASTA
    
    Args:
        genoma_path (str): Ruta al archivo FASTA
    
    Returns:
        str: Secuencia del genoma
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato es incorrecto o está vacío
    """
    if not os.path.isfile(genoma_path):
        logger.error(f"Archivo de genoma no encontrado: {genoma_path}")
        raise FileNotFoundError(f"Archivo de genoma no encontrado: {genoma_path}")
    
    try:
        with open(genoma_path) as archivo:
            encabezado = archivo.readline()

            if not encabezado.startswith('>'):
                logger.error("Formato FASTA inválido: falta encabezado '>'")
                raise ValueError("Formato FASTA inválido: falta encabezado '>'")
                
            secuencia = ''.join(
                linea.strip().upper()
                for linea in archivo
                if not linea.startswith('>')
            )
        
        if not secuencia:
            logger.error("Archivo FASTA vacío")
            raise ValueError("Archivo FASTA vacío")
    
        logger.info(f"Genoma cargado. Longitud: {len(secuencia)}")
        return secuencia
    
    except UnicodeDecodeError:
        logger.error("El archivo no parece ser un FASTA válido")
        raise ValueError("Error de codificación: archivo no es texto plano")