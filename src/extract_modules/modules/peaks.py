"""
Módulo para procesamiento de archivos de picos ChIP-seq

Autor: Ashley Yael Montiel Vargas
Fecha: 01-Mayo-2025
Versión: 4.0
"""

import os
import logging

logger = logging.getLogger('extract_fasta.peaks')

def lectura_peaks(peaks_path):
    """Lee y valida archivo con coordenadas de picos
    
    Args:
        peaks_path (str): Ruta al archivo TSV de picos
    
    Returns:
        dict: Diccionario con coordenadas por TF
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato es incorrecto
    """
    tf_coordenadas = {}
    estadisticas = {
        'lineas_totales': 0,
        'picos_totales': 0,
        'picos_invalidos': 0,
        'picos_validos': 0,
        'errores': {'coordenadas': 0, 'estructura': 0, 'formato': 0},
        'advertencias': {'lineas_vacias': 0, 'campos_vacios': 0}
    }

    columnas_requeridas = ["TF_name", "Peak_start", "Peak_end"]

    if not os.path.isfile(peaks_path):
        logger.error(f"Archivo de picos no encontrado: {peaks_path}")
        raise FileNotFoundError(f"Archivo no encontrado: {peaks_path}")

    try:
        with open(peaks_path) as arch_picos:
            campos = arch_picos.readline().rstrip('\n').split('\t')
            columnas_faltantes = [col for col in columnas_requeridas if col not in campos]

            if columnas_faltantes:
                estadisticas['errores']['formato'] += 1
                logger.error(f"Columnas faltantes: {columnas_faltantes}")
                raise ValueError(f"Columnas faltantes: {columnas_faltantes}")
            
            idx_tf = campos.index('TF_name')
            idx_start = campos.index('Peak_start')
            idx_end = campos.index('Peak_end')
            
            for num_linea, linea in enumerate(arch_picos, 2):
                estadisticas['lineas_totales'] += 1

                if not linea.strip():
                    estadisticas['advertencias']['lineas_vacias'] += 1
                    logger.debug(f"Linea {num_linea}: Vacía - omitiendo")
                    continue

                campos_linea = linea.rstrip('\n').split('\t')

                try: 
                    tf = campos_linea[idx_tf]
                    start = int(float(campos_linea[idx_start]))
                    end = int(float(campos_linea[idx_end]))
                    estadisticas['picos_totales'] += 1
                    
                    if not tf or not start or not end:
                        estadisticas['advertencias']['campos_vacios'] += 1
                        estadisticas['picos_invalidos'] += 1
                        logger.warning(f"Línea {num_linea}: campos vacíos")
                        continue

                    if start >= end:
                        estadisticas['errores']['coordenadas'] += 1
                        estadisticas['picos_invalidos'] += 1
                        logger.warning(f"Línea {num_linea}: Start >= End ({start} >= {end})")
                        continue

                    if tf not in tf_coordenadas:
                        tf_coordenadas[tf] = []
                    tf_coordenadas[tf].append((start, end))
                    estadisticas['picos_validos'] += 1

                except ValueError as e:
                    logger.warning(f"Linea {num_linea}: Error de formato - {str(e)}")
                    estadisticas['errores']['formato'] += 1
                    estadisticas['picos_invalidos'] += 1

                except IndexError:
                    logger.warning(f"Linea {num_linea}: Campos insuficientes")
                    estadisticas['errores']['estructura'] += 1
                
    except Exception as e:
        logger.error(f"Error procesando picos: {str(e)}")
        raise        

    logger.info(
        f"Resumen de procesamiento:\n"
        f"  Líneas totales: {estadisticas['lineas_totales']}\n"
        f"  Picos válidos: {estadisticas['picos_validos']}\n"
        f"  Picos inválidos: {estadisticas['picos_invalidos']}"
    )
    
    return tf_coordenadas

def extraer_secuencias(tf_coordenadas, secuencia):
    """Extrae secuencias genómicas basadas en coordenadas
    
    Args:
        tf_coordenadas (dict): Coordenadas por TF
        secuencia (str): Secuencia del genoma
    
    Returns:
        dict: Secuencias por TF
    """
    longitud_genoma = len(secuencia)
    tf_secuencias = {}
    estadisticas = {'sec_totales': 0, 'sec_validos': 0, 'sec_invalidos': 0}

    for tf, coordenadas in tf_coordenadas.items():
        tf_secuencias[tf] = []
        for start, end in coordenadas:
            estadisticas['sec_totales'] += 1
            if 0 <= start < longitud_genoma and start < end <= longitud_genoma:
                tf_secuencias[tf].append(secuencia[start:end])
                estadisticas['sec_validos'] += 1
            else:
                logger.warning(f"Coordenadas inválidas para {tf} ({start}, {end})")
                estadisticas['sec_invalidos'] += 1

    logger.info(
        f"Extracción completada:\n"
        f"  Picos totales: {estadisticas['sec_totales']}\n"
        f"  Válidos: {estadisticas['sec_validos']}\n"
        f"  Inválidos: {estadisticas['sec_invalidos']}"
    )

    return tf_secuencias
