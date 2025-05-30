"""
Proporciona la configuración de los argumentos de línea de comandos
necesarios para ejecutar la extracción de secuencias FASTA desde sitios de
unión de factores de transcripción (TF).

Funciones:
    configurar_argumentos() -> argparse.ArgumentParser
        Crea y devuelve un parser con:

        Argumentos obligatorios:
            -g, --genome      Ruta al archivo FASTA del genoma.
            -p, --peaks       Ruta al archivo TSV con columnas
                               TF_name, Peak_start, Peak_end.

        Argumentos opcionales:
            -o, --outdir      Directorio de salida para los FASTA
                              (default: "TF_picos_fasta").
            --logs            Directorio de logs (default: "logs").
            -v, --verbose     Activa el modo DEBUG en consola.
            -l, --line_length Longitud máxima de línea en los FASTA
                              (default: 80).

        Argumentos restantes:
            args_restantes    Cualquier otro parámetro posicional no
                              reconocido, almacenado como lista.
Autor:
    Ashley Yael Montiel Vargas <yaelmont@lcg.unam.mx>

Fecha:
    29 de mayo de 2025

Versión:
    4.1
"""
# =============================================================================
# IMPORTS
# =============================================================================
import argparse

def configurar_argumentos():
    """Configura y retorna el parser de argumentos
    
    Returns:
        argparse.ArgumentParser: Parser configurado
    """
    parser = argparse.ArgumentParser(
        description="Extrae secuencias FASTA de sitios de unión de factores " \
        "de transcripción"
    )
    
    # Argumentos requeridos
    parser.add_argument("-g", "--genome", required=True, 
                      help="Archivo FASTA del genoma")
    parser.add_argument("-p", "--peaks", required=True,
                      help="Archivo TSV con columnas: TF_name, Peak_start, " \
                      "Peak_end")
    
    # Argumentos opcionales
    parser.add_argument("-o", "--outdir", default="TF_picos_fasta",
                      help="Directorio de salida para archivos FASTA")
    parser.add_argument("--logs", default="logs",
                      help="Directorio para archivos de log")
    parser.add_argument("-v", "--verbose", action="store_true",
                      help="Mostrar mensajes DEBUG")
    parser.add_argument("-l", "--line_length", type=int, default=80,
                      help="Número de caracteres por línea en el archivo" \
                      " FASTA")
    
    # Manejar argumentos desconocidos
    parser.add_argument('args_restantes', nargs=argparse.REMAINDER)
    
    return parser

