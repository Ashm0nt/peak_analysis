"""
Módulo de procesamiento de archivos de picos de ChIP-Seq para la extracción
y validación de regiones genómicas asociadas a factores de transcripción (TF).

Contiene dos funciones principales:

  1. lectura_peaks(peaks_path: str) -> Dict[str, List[Tuple[int, int]]]
     -----------------------------------------------------------------
     - Lee un TSV de picos asegurando que existan las columnas mínimas:
       "TF_name", "Peak_start", "Peak_end".
     - Filtra filas vacías, formateo incorrecto y coordenadas inválidas.
     - Agrupa los pares (start, end) por cada TF y devuelve un diccionario.
     - Registra estadísticas y advertencias/errores en el logger.

  2. extraer_secuencias(
       tf_coordenadas: Dict[str, List[Tuple[int, int]]],
       secuenciagenoma: str
     ) -> Dict[str, List[str]]
     --------------------------------------------------------------
     - Recorta fragmentos de ADN de la cadena completa del genoma usando
       las coordenadas (0-based) de cada TF.
     - Omite rangos fuera de los límites y registra advertencias.
     - Devuelve un diccionario TF → lista de secuencias extraídas.

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
from typing import Dict, List, Tuple

import pandas as pd

# =============================================================================
# FUNCIONES
# =============================================================================

#Configurar el logger para el módulo
logger = logging.getLogger(__name__)

def lectura_peaks(peaks_path: str) -> Dict[str, List[Tuple[int, int]]]:
    """
    Lee y valida un archivo TSV de picos, devolviendo coordenadas agrupadas
    por TF.

    El archivo debe contener, al menos, las columnas:
    - "TF_name"
    - "Peak_start"
    - "Peak_end"

    Args:
        peaks_path (str): Ruta al archivo TSV de picos.

    Returns:
        Dict[str, List[Tuple[int, int]]]: 
            Mapa de cada TF a su lista de tuplas (start, end).

    Raises:
        FileNotFoundError: Si `peaks_path` no existe.
        ValueError: Si faltan columnas requeridas o los datos no son válidos.
    """
     
    #Inicializar estructuras 
    tf_coordenadas: Dict[str, List[Tuple[int, int]]] = {}
    estadisticas = {
        'lineas_totales': 0,
        'picos_totales': 0,
        'picos_invalidos': 0,
        'picos_validos': 0,
        'errores': {'coordenadas': 0, 'estructura': 0, 'formato': 0},
        'advertencias': {'lineas_vacias': 0, 'campos_vacios': 0}
    }

    # Verificar que el archivo exista 
    if not os.path.isfile(peaks_path):
        msg = f"Archivo de picos no encontrado: {peaks_path}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    try:
        # Leer líneas crudas para contar vacías
        with open(peaks_path, mode="r", encoding="utf-8") as arch_picos:
        # Excluimos la cabecera
            for num_linea, linea in enumerate(arch_picos, 2):
                estadisticas['lineas_totales'] += 1

                if not linea.strip():
                    estadisticas['advertencias']['lineas_vacias'] += 1
                    logger.debug(f"Linea {num_linea}: Vacía - omitiendo")
                    continue


        # Leer con pandas
        try:
            df = pd.read_csv(peaks_path, sep="\t", 
                         dtype={"TF_name": str}, comment=None)
        except Exception as e:
            msg = f"No se pudo leer '{peaks_path}': {e}"
            logger.error(msg)
            raise ValueError(msg)

        # Validar columnas
        columnas_requeridas = ["TF_name", "Peak_start", "Peak_end"]
        columnas_faltantes = [c for c in columnas_requeridas 
                          if c not in df.columns]
        if columnas_faltantes:
            estadisticas['errores']['formato'] += 1
            msg = f"Columnas faltantes en {peaks_path}: {columnas_faltantes}"
            logger.error(msg)
            raise ValueError(msg)


        # Procesar filas
        for fila, valores in df.iterrows():
            estadisticas['picos_totales'] += 1
        
            tf = (valores["TF_name"] or "").strip()
            start = (valores["Peak_start"] or "")
            end = (valores["Peak_end"] or "")
            
            if not (tf and start and end):
                estadisticas['advertencias']['campos_vacios'] += 1
                estadisticas['picos_invalidos'] += 1
                logger.warning("Fila %d: campos vacíos, omitiendo", fila + 2)
                continue
    
            # Intentar parsear coordenadas
            try:
                start = int(float(start))
                end = int(float(end))
            except ValueError:
                estadisticas['errores']['formato'] += 1
                estadisticas['picos_invalidos'] += 1
                logger.warning(
                    "Fila %d: error de formato en coordenadas", fila + 2)
                continue

            # Validar orden y valor
            if start <= 0 or end <= 0:
                estadisticas['errores']['coordenadas'] += 1
                estadisticas['picos_invalidos'] += 1
                logger.warning(
                    "Fila %d: coordenada ≤ 0 (%d, %d)", fila + 2, start, end)
                continue
            if start >= end:
                estadisticas['errores']['coordenadas'] += 1
                estadisticas['picos_invalidos'] += 1
                logger.warning(
                    "Fila %d: start ≥ end (%d ≥ %d)", fila + 2, start, end)
                continue
        
            if tf not in tf_coordenadas:
                tf_coordenadas[tf] = []
                tf_coordenadas[tf].append((start, end))
                estadisticas['picos_validos'] += 1

    except Exception as e:
        logger.error(f"Error procesando picos: {str(e)}")
        raise 

    # Resumen de estadísticas
    logger.info(
        f"Resumen de procesamiento:\n"
        f"  Líneas totales: {estadisticas['lineas_totales']}\n"
        f"  Picos válidos: {estadisticas['picos_validos']}\n"
        f"  Picos inválidos: {estadisticas['picos_invalidos']}"
    )

    return tf_coordenadas

def extraer_secuencias(
    tf_coordenadas: Dict[str, List[Tuple[int, int]]],
    secuenciagenoma: str
) -> Dict[str, List[str]]:
    """
    Extrae fragmentos de ADN de la secuencia genómica según coordenadas 
    de picos.

    Para cada factor de transcripción (TF), recorta las subcadenas definidas
    por pares (start, end) en `tf_coordenadas`. Acumula estadísticas de 
    totales, válidos e inválidos, y registra advertencias cuando las 
    coordenadas estén fuera de rango.

    Args:
        tf_coordenadas (Dict[str, List[Tuple[int, int]]]):
            Mapa de cada TF a la lista de tuplas (start, end), 
            índices 0-based.
        secuenciagenoma (str): Cadena con la secuencia completa del genoma.

    Returns:
        Dict[str, List[str]]: Mapa de cada TF a la lista de secuencias 
            extraídas.
    """

    #Inicializar estructuras
    tf_secuencias: Dict[str, List[str]] = {}
    estadisticas = {
        'sec_totales': 0,
        'sec_validos': 0,
        'sec_invalidos': 0
    }

    #Longitud del genoma 
    longitud = len(secuenciagenoma)

    #Extracción de las coordenadas genómicas
    for tf, rangos in tf_coordenadas.items():
        secuencias_tf: List[str] = []
        for start, end in rangos:
            #Validación del rango
            estadisticas['sec_totales'] += 1
            if 0 <= start < end <= longitud:
                secuencias_tf.append(secuenciagenoma[start:end])
                estadisticas['sec_validos'] += 1
            else:
                estadisticas['sec_invalidos'] += 1
                logger.warning(
                    "%s: coordenadas inválidas (%d, %d)", tf, start, end
                )
        tf_secuencias[tf] = secuencias_tf
    
    #Resumen de estadpsiticas 
    logger.info(
        "Extracción completada: totales=%d, válidos=%d, inválidos=%d",
        estadisticas['sec_totales'],
        estadisticas['sec_validos'],
        estadisticas['sec_invalidos']
    )
    return tf_secuencias
