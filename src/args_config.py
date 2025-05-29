"""
Módulo para configuración de argumentos de línea de comandos

Autor: Ashley Yael Montiel Vargas
Fecha: 29-Mayo-2025
Versión: 4.0
"""

import argparse

def configurar_argumentos():
    """Configura y retorna el parser de argumentos
    
    Returns:
        argparse.ArgumentParser: Parser configurado
    """
    parser = argparse.ArgumentParser(
        description="Extrae secuencias FASTA de sitios de unión de factores de transcripción"
    )
    
    # Argumentos requeridos
    parser.add_argument("-g", "--genome", required=True, 
                      help="Archivo FASTA del genoma")
    parser.add_argument("-p", "--peaks", required=True,
                      help="Archivo TSV con columnas: TF_name, Peak_start, Peak_end")
    
    # Argumentos opcionales
    parser.add_argument("-o", "--outdir", default="TF_picos_fasta",
                      help="Directorio de salida para archivos FASTA")
    parser.add_argument("--logs", default="logs",
                      help="Directorio para archivos de log")
    parser.add_argument("-v", "--verbose", action="store_true",
                      help="Mostrar mensajes DEBUG")
    parser.add_argument("-l", "--line_length", type=int, default=80,
                      help="Número de caracteres por línea en el archivo FASTA")
    
    return parser

