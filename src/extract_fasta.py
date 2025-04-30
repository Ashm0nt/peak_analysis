'''
Script para extraer secuencias FASTA de sitios de unión de factores de transcripción
en E. coli sin usar módulos externos.

Autor: Ashley Yael Montiel Vargas
Fecha: 01-Mayo-2025
'''

import os
import argparse

def cargar_genoma(genoma_path):
    '''
    Funcion que cargar el genoma a partir de un archivo fasta a una sola variable

    Args:
        genome_path (str): Ruta del archivo del genoma
    
    Return: 
        secuencia (str): Secuencia del genoma como cadena de texto
    
    Raises: 
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo FASTA está vacío o tiene formato incorrecto.
    '''
    #Verificacion de la ruta
    if not os.path.exits(genoma_path):
        raise FileNotFoundError(f"Archivo de genoma no encontrado: {genoma_path}")
    try:
        with open(genoma_path) as archivo:
            linea = archivo.readline()

            #Verifica que el archivo sea formato FASTA
            if not linea.startswith('>'):
                raise ValueError("Formato FASTA invalido: falta encabezado '>'")
                
            for linea in archivo:
                #Control de anotaciones posteriores
                if linea.startswith ('>'):
                    continue
                secuencia +=linea
            #Verifica que el archivo no este vacio
            if not secuencia:
                raise ValueError("Archivo FASTA vacio")
        
        return secuencia
    
    #Control de Error
    except Exception as e:
        raise ValueError(f"Error al leer archivo FASTA: {str(e)}")

def lectura_peaks (peaks_path):
    '''
    Funcion que lee el archivo de picos y deculeve un diccionario con TF_name, start y end
    
    Args:
        peaks_path (str): Ruta del archivo de picos

    Return:
        Lista de diccionarios con los datos para cada TF (star, end)

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato del archivo es incorrecto
    '''
    tf_coordenadas= {}
    columnas_requeridas = ["TF_name", "Peak_start", "Peak_end"]

    #Validar la ruta del archivo
    if not os.path.exists(peaks_path):
        raise FileNotFoundError(f"Archivo no encontrado: {peaks_path}")
    try: 
        with open (peaks_path) as arch_picos:
            campos = arch_picos.readline().rstrip().split('\t')

            columnas_faltantes = [col for col in columnas_requeridas if col not in campos]
            #Valida que el archivo tenga las columnas necesarias
            if columnas_faltantes:
                raise ValueError(f"El archivo no cuenta con las columnas requeridas para el analisis. Columnas flatantes: {columnas_faltantes}")
            
            try:
                idx_tf = campos.index('TF_name')
                idx_start = campos.index('Peak_start')
                idx_end = campos.index('Peak_end')
            except ValueError as e:
                raise ValueError(f"Columna no encontrada: {str(e)}")
            
            for num_linea, linea in enumerate(arch_picos, 2):
                linea = linea.rstrip()
                #No se toman en cuenta lineas vacias
                if not linea:
                    continue
                linea = linea.split('\t')
                #Si la linea tiene vacio un campo necesario
                if not all(linea[idx] for idx in [idx_tf, idx_start, idx_end]):
                    print(f"Linea {num_linea}: Campos requeridos vacíos - omitiendo")
                    continue 

                try: 
                    tf = linea[idx_tf]
                    start = linea[idx_start]
                    end = linea[idx_end]
                    
                    #Validat que las regiones no sean incongruentes
                    if start >= end:
                        print(f"Linea {num_linea}: Start >= End ({start} >= {end}) - omitiendo")
                        continue
                    
                    if tf not in tf_coordenadas:
                        tf_coordenadas[tf] = []
                    tf_coordenadas[tf].append((start, end))
                
                except ValueError:
                    print(f"Línea {num_linea}: Valores numéricos inválidos - omitiendo")
                    continue
                
        return tf_coordenadas
    except Exception as e:
        raise Exception(f"Error al leer el archivo de picos: {str(e)}")




                


            
