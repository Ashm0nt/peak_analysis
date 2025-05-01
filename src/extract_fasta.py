'''
Script para extraer secuencias FASTA de sitios de unión de factores de transcripción
en E. coli sin usar módulos externos.

Autor: Ashley Yael Montiel Vargas
Fecha: 01-Mayo-2025
'''

import os
from datetime import datetime
import logging
import argparse

def configurar_logging(output_dir="logs"):
    """Configura el sistema de logging centralizado"""
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def cargar_genoma(genoma_path):
    '''
    Funcion que cargar el genoma a partir de un archivo fasta a una sola variable

    Args:
        genome_path (str): Ruta del archivo del genoma
    
    Returns: 
        secuencia (str): Secuencia del genoma como cadena de texto
    
    Raises: 
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo FASTA está vacío o tiene formato incorrecto.
    '''
    #Verificacion de la ruta 
    if not os.path.isfile(genoma_path):
        logging.error (f"Archivo de genoma no encontrados: {genoma_path}")
        raise FileNotFoundError(f"Archivo de genoma no encontrado: {genoma_path}")
    
    try:
        with open(genoma_path) as archivo:
            encabezado = archivo.readline()

            #Verifica que el archivo sea formato FASTA
            if not encabezado.startswith('>'):
                logging.error ("Formato FASTA invalido: falta encabezado: '>")
                raise ValueError("Formato FASTA invalido: falta encabezado '>'")
                
            secuencia = ''.join(
                linea.strip().upper()
                for linea in archivo
                if not linea.startswith('>')
            )
        
            #Verifica que el archivo no este vacio
        if not secuencia:
            logging.error("Archivo FASTA vacio")
            raise ValueError("Archivo FASTA vacio")
    
        logging.info(f"Genoma cargado correctamente. Longitud: {len(secuencia)}")
        
        return secuencia
    
    except UnicodeDecodeError:
        logging.error("El archivo no parece ser un FASTA valido (problema de codificacion)")
        raise ValueError("Error de codificacion: archivo no es texto plano")
    

def lectura_peaks (peaks_path):
    '''
    Funcion que lee el archivo de picos y devuleve un diccionario con TF_name, start y end
    
    Args:
        peaks_path (str): Ruta del archivo de picos

    Returns:
        Lista de diccionarios con los datos para cada TF (start, end)

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato del archivo es incorrecto
    '''
    tf_coordenadas= {}

    estadisticas = {
        'lineas_totales': 0,
        'picos_totales': 0,
        'picos_invalidos': 0,
        'picos_validos': 0,
        'errores': {
            'coordenadas' : 0,
            'estructura' : 0,
            'formato' : 0     
        },

        'advertencias': {
            'lineas_vacias': 0,
            'campos_vacios': 0,
        }
    }

    columnas_requeridas = ["TF_name", "Peak_start", "Peak_end"]

    #Validar la ruta del archivo
    if not os.path.isfile(peaks_path):
        logging.error(f"Archivo de picos no encontrado: {peaks_path}")
        raise FileNotFoundError(f"Archivo no encontrado: {peaks_path}")

    try:
        with open (peaks_path) as arch_picos:
            campos = arch_picos.readline().rstrip('\n').split('\t')
            columnas_faltantes = [col for col in columnas_requeridas if col not in campos]

            #Valida que el archivo tenga las columnas necesarias
            if columnas_faltantes:
                estadisticas['errores']['formato'] += 1
                logging.error(f"El archivo no cuenta con las columnas requeridas para el analisis. Columnas faltantes: {columnas_faltantes}")
                raise ValueError(f"El archivo no cuenta con las columnas requeridas para el analisis. Columnas faltantes: {columnas_faltantes}")
            
            
            idx_tf = campos.index('TF_name')
            idx_start = campos.index('Peak_start')
            idx_end = campos.index('Peak_end')
            
            for num_linea, linea in enumerate(arch_picos, 2):
                estadisticas['lineas_totales'] += 1

                #No se toman en cuenta lineas vacias
                if not linea.strip():
                    estadisticas['advertencias']['lineas_vacias'] += 1
                    logging.debug(f"Linea {num_linea}: Vacia - omitiendo")
                    continue

                campos_linea = linea.rstrip('\n').split('\t')

                try: 
                    tf = campos_linea[idx_tf]
                    start = int(campos_linea[idx_start])
                    end = int(campos_linea[idx_end])
                    estadisticas['picos_totales'] += 1
                    
                    #Validar que las regiones no sean incongruentes
                    if not tf or not start or not end:
                        estadisticas['advertencias']['campos_vacios'] += 1
                        estadisticas['picos_invalidos'] += 1
                        logging.warning(f"Línea {num_linea}: campos vacíos - omitida")
                        continue

                    if start >= end:
                        estadisticas['errores']['coordenadas'] += 1
                        estadisticas['picos_invalidos'] += 1
                        logging.warning(f"Línea {num_linea}: Start >= End ({start} >= {end})")
                        continue

                    
                    if tf not in tf_coordenadas:
                        tf_coordenadas[tf] = []
                    tf_coordenadas[tf].append((start, end))
                    estadisticas['picos_validos'] += 1

                except ValueError as e:
                    logging.warning(f"Linea {num_linea}: Error de formato -{str(e)}")
                    estadisticas['errores']['formato'] += 1
                    estadisticas['picos_invalidos'] += 1

                except IndexError:
                    logging.warning(f"Linea {num_linea}: Campos insuficientes")
                    estadisticas['errores']['estructura'] += 1
                
    except Exception as e:
        logging.error(f"Error inesperado procesando pico: {str(e)}")
        raise        

    logging.info(
        f"Resumen de procesamiento:\n"
        f"  Lineas totales: {estadisticas['lineas_totales']}\n"
        f"  Picos validos: {estadisticas['picos_validos']}\n"
        f"  Picos inválidos: {estadisticas['picos_invalidos']}\n"
        f"  Advertencias:\n"
        f"    Líneas vacias: {estadisticas['advertencias']['lineas_vacias']}\n"
        f"    Campos vacios: {estadisticas['advertencias']['campos_vacios']}\n"
        f"  Errores:\n"
        f"    Coordenadas invalidas: {estadisticas['errores']['coordenadas']}\n"
        f"    Estructura incompleta: {estadisticas['errores']['estructura']}"
    )
    
    return tf_coordenadas

def extraer_secuencias (tf_coordenadas, secuencia):
    '''
    Funcion que extrae secuencias genomicas basadas en coordenadas

    Args:
        tf_coordenadas (dic): Diccionario con las coordenadas por TF
        secuencia (str): Genoma

    Return:
        tf_secuencias (dic): Diccionario con las secuencias de cada TF
    '''

    longitud_genoma = len(secuencia)

    tf_secuencias = {}
    estadisticas_secuencias = {
        'sec_totales': 0,
        'sec_validos' : 0,
        'sec_invalidos': 0
    }

    for tf, coordenadas in tf_coordenadas.items():
        tf_secuencias[tf] = []
        for start, end in coordenadas:
            estadisticas_secuencias['sec_totales'] += 1
            #Validar coordenadas y guardar secuencia
            if 0 <= start < longitud_genoma and start < end <= longitud_genoma:
                pico_secuencia = secuencia [start:end]
                tf_secuencias[tf].append(pico_secuencia)
                estadisticas_secuencias['sec_validos'] += 1

            else:
                logging.warning(f"Coordenadas inválidas para {tf} (start: {start}, end: {end}). Omitiendo.")
                estadisticas_secuencias['sec_invalidos'] += 1

    logging.info(
        f"Extracción de secuencias completada:\n"
        f"  Picos totales: {estadisticas_secuencias['sec_totales']}\n"
        f"  Picos válidos: {estadisticas_secuencias['sec_validos']}\n"
        f"  Picos inválidos: {estadisticas_secuencias['sec_invalidos']}"
    )

    return tf_secuencias

def fasta_archivos(tf_secuencias, output_dir="TF_picos_fasta", chars_linea=80):
    '''
    Funcion que crea los archivos fasta para cada TF con todas las secuencias identificadas

    Args:
        tf_secuencias(dic): Diccionario con las secuencias por cada TF
        output_dir (str): Directorio de salida
    Return: 
        Directorio con los archivos fasta generados
    '''
    #Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    archivos_generados = []

    for tf, secuencias in tf_secuencias.items():
        #Si la secuencia esta vacia
        if not secuencias:
            continue

        nombre_archivo = os.path.join(output_dir, f"{tf}.fa")
        try:
            #Generar un archivo oara escribir las secuencias
            with open(nombre_archivo, 'w') as arch_salida:
                for i, secuencia in enumerate(secuencias, 1):
                    arch_salida.write(f">{tf}_pico_{i}_len={len(secuencia)}\n")
                    
                    # Escribir secuencia en líneas de 80 caracteres (estándar FASTA)
                    for j in range(0, len(secuencia), chars_linea):
                        arch_salida.write(f"{secuencia[j:j+chars_linea]}\n")

                    archivos_generados.append(nombre_archivo)
            logging.info(f"Archivo generado: {nombre_archivo} ({len(secuencias)} secuencias)")
            
        except Exception as e:
            logging.error(f"Error generando archivo para {tf}: {str(e)}")
    
    return archivos_generados


if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        description="Extrae secuencias FASTA de sitios de unión de factores de transcripción en E. coli."
    )
    parser.add_argument("-g", "--genome", required=True, help="Archivo FASTA del genoma de E. coli")
    parser.add_argument("-p", "--peaks", required=True, help="Archivo con coordenadas de picos (TSV con columnas: TF_name, Peak_start, Peak_end)")
    parser.add_argument("-o", "--output", default="TF_picos_fasta", help="Directorio de salida para los archivos FASTA")
    parser.add_argument("-l", "--line_length", type=int, default=80, help="Número de caracteres por línea en el archivo FASTA")
    parser.add_argument("--logs", default="logs", help="Directorio para archivos de log")

    args = parser.parse_args()

    # Configurar logging
    configurar_logging(args.logs)

    try:
        logging.info("Iniciando el procesamiento de datos")

        # Cargar genoma
        genoma = cargar_genoma(args.genome)

        # Leer picos
        coordenadas = lectura_peaks(args.peaks)

        # Extraer secuencias
        secuencias = extraer_secuencias(coordenadas, genoma)

        # Escribir archivos FASTA
        archivos = fasta_archivos(secuencias, args.output, args.line_length)

        logging.info(f"Proceso completado. Archivos generados: {len(archivos)}")

    except Exception as e:
        logging.error(f"Error durante la ejecución: {str(e)}")
        exit(1)