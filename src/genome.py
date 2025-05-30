"""
Módulo para la carga y validación de archivos FASTA de genoma.

Contiene:

  - cargar_genoma(genoma_path: str) -> str
    ------------------------------------------------------------
    Lee un archivo FASTA completo y devuelve la secuencia concatenada
    en mayúsculas. Realiza las siguientes comprobaciones:

      * Verifica que el fichero exista y sea accesible.
      * Valida que la primera línea comience con '>'.
      * Ignora cabezales secundarios y concatena solo las líneas de
        secuencia.
      * Comprueba que la secuencia no esté vacía.
      * Maneja errores de formato, archivo inexistente y problemas
        de codificación.

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

    # Intentamos abrir primero para capturar PermissionError
    try:
        #Abrir el archivo
        with open(genoma_path, mode="r", encoding="utf-8") as archivo:
            #Leer y validar encabezado FASTA
            encabezado = archivo.readline().strip()
            if not encabezado.startswith('>'):
                msg = "Formato FASTA inválido: falta línea de encabezado '>'"
                logger.error(msg)
                raise ValueError(msg)

            #Concatenar las lineas
            secuencia = "".join(
                linea.strip().upper()
                for linea in archivo
                if not linea.startswith(">")
            )

    except PermissionError as e:
        msg = "Permiso denegado"
        logger.error(f"{msg}: {e}")
        raise ValueError(msg)
    except FileNotFoundError:
        msg = f"Archivo de genoma no encontrado: {genoma_path}"
        logger.error(msg)
        raise FileNotFoundError(msg)  
    except UnicodeDecodeError as e:
        msg = f"Error de codificación al leer '{genoma_path}': {e}"
        logger.error(msg)
        raise ValueError(msg)
        
    # Si el archivo está vacio
    if not secuencia:
        msg = "Archivo FASTA vacío"
        logger.error(msg)
        raise ValueError(msg)
    
    logger.info("Genoma cargado; longitud: %d bp", len(secuencia))
    return secuencia
    