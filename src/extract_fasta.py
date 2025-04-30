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
    if not os.path.exits(genoma_path):
        raise FileNotFoundError(f"Archivo de genoma no encontrado: {genoma_path}")
    try:
        with open(genoma_path) as archivo:
            linea = archivo.readline()

            if not linea.startswith('>'):
                raise ValueError("Formato FASTA invalido: falta encabezado '>'")
                
            for linea in archivo:
                if linea.startswith ('>'):
                    break
                secuencia +=linea
            
            if not secuencia:
                raise ValueError("Archivo FASTA vacio")
        
        return secuencia
    
    except Exception as e:
        raise ValueError(f"Error al leer archivo FASTA: {str(e)}")


                

