'''
Script para extraer secuencias FASTA de sitios de unión de factores de transcripción
en E. coli sin usar módulos externos.

Autor: Ashley Yael Montiel Vargas
Fecha: 01-Mayo-2025
'''

import os
import logging
import argparse

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
        'picos_totales': 0,
        'picos_totales': 0,
        'picos_invalidos': 0,
        'picos_validos': 0,
        'errores': 0,
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
                estadisticas['errores'] += 1
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
                    
                    if tf not in tf_coordenadas:
                        tf_coordenadas[tf] = []
                    tf_coordenadas[tf].append((start, end))
                    estadisticas['picos_validos'] += 1

                except ValueError as e:
                    logging.warning(f"Linea {num_linea}: Error de formato -{str(e)}")
                    estadisticas['errores']['coordenadas'] += 1
                    estadisticas['picos_invalidos'] += 1

                except IndexError:
                    logging.warning(f"Linea {num_linea}: Campos insuficientes")
                    estadisticas['errores'] += 1
                
    except Exception as e:
        logging.error(f"Error inesperado procesando pico: {str(e)}")
        raise        

    logging.info(
        f"Procesamiento completado. "
        f"Lineas: {estadisticas['lineas_procesadas']}, "
        f"Picos válidos: {estadisticas['picos_validos']}, "
        f"Errores: {estadisticas['errores']}, "
        f"Advertencias: {estadisticas['advertencias']}"
    )

    return tf_coordenadas

def extraer_secuencias (tf_coordenadas, secuencia):
    '''
    Funcion que extrea secuencias genomicas basadas en coordenadas

    Args:
        tf_coordenadas (dic): Diccionario con las coordenadas por TF
        secuencia (str): Genoma

    Return:
        tf_secuencias (dic): Diccionario con las secuencias de cada TF
    '''

    longitud_genoma = len(secuencia)

    tf_secuencias = {}
    estadisticas_picos = {
        'picos_totales': 0,
        'picos validos' : 0,
        'picos invalidos': 0
    }

    for tf, coordenadas in tf_coordenadas.items():
        tf_secuencias[tf] = []
        for start, end in coordenadas:
            #Validar coordenadas y guardar secuencia
            if 0 <= start < longitud_genoma and start < end <= longitud_genoma:
                pico_secuencia = secuencia [start:end]
                tf_secuencias[tf].append(pico_secuencia)

            else:
                print(f"Advertencia: Coordenadas inválidas para {tf} (start: {start}, end: {end}). Omitiendo.")

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
            print(f"Archivo generado: {nombre_archivo} ({len(secuencias)} secuencias)")
            
        except Exception as e:
            print(f"Error generando archivo para {tf}: {str(e)}")
    
    return archivos_generados


if __name__ == "__main__":









                


            
