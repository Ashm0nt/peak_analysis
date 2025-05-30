"""
Autor: 
    Ashley Yael Montiel Vargas

Fecha:
     01-Mayo-2025

Version:
    4.0

Descripcion:
    Script para extraer secuencias FASTA de sitios de union de factores de 
    transcripcion en base a coordenadas obtenidas a partir de experimentos
    ChIP-seq 

Funcionalidad:
    1. Lee el archivo FASTA de entrada.
    2. Extrae las secuencias y las guarda en archivos separados.
    3. Los archivos generados se guardan en un directorio especificado por 
        el usuario.
    4. Los nombres de los archivos se asignan de manera secuencial como 
        'fragmento_001.fasta', 'fragmento_002.fasta', etc.

Argumentos:
    -g, --genome: Ruta al archivo FASTA de entrada
    -p, --peaks: Ruta al archivo que contiene los picos de TFs
    -o, --outdir: Directorio de salida de los archivos generados
    --logs: Directorio de salida del log
    -l, --line_lenght: Formato para las secuencias de fasta (opcional)
    --verbose: Activar log DEBUG

Uso:
    python3 extract_fasta.py -g ../data/E_coli_K12_MG1655_U00096.3.txt 
        -p ../data/union_peaks_file.tsv -o ../results/ --logs ../doc -v 

"""

# =============================================================================
# IMPORTS
# =============================================================================
import sys
from args_config import configurar_argumentos
from logging_config import configurar_logging
from genome import cargar_genoma
from peaks import lectura_peaks, extraer_secuencias
from io_utils import escribir_fasta

# =============================================================================
# MAIN
# =============================================================================
def main():
    # Configurar y parsear argumentos
    parser = configurar_argumentos()

    # Detectar opciones no reconocidas antes de parsear
    valid_opts = set(parser._option_string_actions.keys())
    for raw in sys.argv[1:]:
        # separar "--foo=bar" → "--foo"
        opt = raw.split("=", 1)[0]
        if opt.startswith("-") and opt not in valid_opts:
            parser.error(f"unrecognized argument: {opt}")
    args = parser.parse_args()

    #Manejo de argumentos no reconocidos
    if args.args_restantes:
        print(f"Error: Argumentos no reconocidos: {args.args_restantes}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

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
        archivos = escribir_fasta(secuencias, args.outdir, args.line_length)
        
        logger.info(f"Proceso completado. Archivos generados: {len(archivos)}")

    except Exception as e:
        logger.exception("Error durante la ejecución")
        exit(1)

if __name__ == "__main__":
    main()