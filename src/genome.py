"""
Módulo para la validación y lectura del archivos FASTA 

Autor: Ashley Yael Montiel Vargas
Fecha: 29-Mayo-2025
Versión: 5.0
"""
# =============================================================================
# IMPORTS
# =============================================================================
import os
import logging
from typing import TextIO

# =============================================================================
# FUNCIONES
# =============================================================================

# COnfigurar el logger para el módulo
logger = logging.getLogger(__name__)

def cargar_genoma(genoma_path : str) -> str:
    """
    Carga la secuencia de un genoma desde un archivo FASTA.

    Esta función lee un archivo FASTA que debe comenzar con una línea de 
    encabezado (">...") seguida de una o más líneas de secuencia. Se concatena 
    y devuelve como una sola cadena de bases en mayúsculas.

    Args:
        genoma_path (str): Ruta al archivo FASTA del genoma.

    Returns:
        str: Secuencia completa del genoma en mayúsculas.

    Raises:
        FileNotFoundError: Si `genoma_path` no existe o no es un archivo.
        ValueError: Si el archivo no comienza con '>' o la secuencia está 
        vacía.
    """

    #Verificar que exista el archivo 
    if not os.path.isfile(genoma_path):
        msg = f"Archivo de genoma no encontrado: {genoma_path}"
        logger.error(msg)
        raise FileNotFoundError(msg)
    
    try:
        with open(genoma_path, mode="r", encoding="utf-8") as archivo:
            #Leer y validar encabezado FASTA
            encabezado = archivo.readline().strip()
            if not encabezado.startswith('>'):
                msg = "Formato FASTA inválido: falta línea de encabezado '>'"
                logger.error(msg)
                raise ValueError(msg)

            #Concantenar las líneas 
            secuencia = "".join(
                linea.strip().upper()
                for linea in archivo
                if not linea.startswith(">")
            )
        
        # Si el archivo está vacio
        if not secuencia:
            msg = "El archivo FASTA está vacío o no contiene secuencia válida"
            logger.error(msg)
            raise ValueError(msg)
    
        logger.info("Genoma cargado; longitud: %d bp", len(secuencia))
        return secuencia
    
    except UnicodeDecodeError as e:
        msg = f"Error de codificación al leer '{genoma_path}': {e}"
        logger.error(msg)
        raise ValueError(msg)