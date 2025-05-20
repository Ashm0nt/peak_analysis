#!/usr/bin/env python3
"""
Script principal para extracción de secuencias FASTA
"""

import sys
from modules.args_config import configurar_argumentos
from modules.logging_config import configurar_logging
from modules.genome import cargar_genoma
from modules.peaks import lectura_peaks, extraer_secuencias
from modules.io_utils import fasta_archivos

def main():
    # Configurar y parsear argumentos
    parser = configurar_argumentos()
    args = parser.parse_args()

    # Configurar logging
    logger = configurar_logging(args.logs, args.verbose)

    try:
        logger.info("Iniciando procesamiento")
        
        # 1. Cargar genoma
        genoma = cargar_genoma(args.genome)
        
        # 2. Procesar picos
        coordenadas = lectura_peaks(args.peaks)
        
        # 3. Extraer secuencias
        secuencias = extraer_secuencias(coordenadas, genoma)
        
        # 4. Escribir archivos FASTA
        archivos = fasta_archivos(secuencias, args.output, args.line_length)
        
        logger.info(f"Proceso completado. Archivos generados: {len(archivos)}")

    except Exception as e:
        logger.exception("Error durante la ejecución")
        exit(1)

if __name__ == "__main__":
    main()