### Casos de Prueba para el Módulo 1: Extractor y Creador de Secuencias FASTA


1.  **Caso: Archivo del genoma no se encuentra.**
    
    -   **Entradas:**
        -   Ruta incorrecta o inexistente para el archivo FASTA del genoma.
        -   Archivo de picos válido.
        -   Directorio de salida.
    -   **Esperado:** `"Error: Genome file not found"`
    
    ```python
    mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
    ```
    ```
    Error: "Ecoli.fna" genome file not found
    ```
2.  **Caso: Archivo de picos vacío.**
    
    -   **Entradas:**
        -   Archivo de picos vacío.
        -   Archivo FASTA del genoma.
        -   Directorio de salida.
    -   **Esperado:** `"Error: the peak file is empty."`

 ```python
    mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
```
  
```
Error: the peak file is empty
```

3.  **Caso: Posiciones `Peak_start` y `Peak_end` fuera del rango del genoma.**
    
    -   **Entradas:**
        -   Archivo de picos con algunas posiciones `Peak_start` y `Peak_end` fuera del tamaño del genoma.
        -   Archivo FASTA del genoma válido.
        -   Directorio de salida.
    -   **Esperado:**
        -   El sistema debe imprimir un mensaje de advertencia: `"Warning: Some peaks are bigger than the genome". Check the log.out file`
        
        -   Generar un archivo de log indicando los picos fuera de rango. El archivo debe contener las líneas del archivo de picos que tienen problemas.
        -   Los picos fuera de rango deben ser ignorados y no se deben incluir en los archivos FASTA generados.


    ```python
        mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
    ```
    ```
        Warning: Some peaks are bigger than the genome. Check the log.out file
    ```
    ```bash
        #Comando para Verificar la Salida:
        ls
    ```

    ```bash
        #Salida Esperada:
        log.out
        fasta_peaks/
    ```

4. **Caso: Coordenadas incompletas (falta Peak_start o Peak_end).**

    - **Entradas:**
        - Archivo de picos con una fila que tiene solo Peak_start o solo Peak_end.
        - Archivo FASTA del genoma válido.
        - Directorio de salida.

    - **Esperado:**
        - El sistema debe imprimir un mensaje de error: '"Error: Incomplete peak coordinates in the peak file."'
        - Registrar el error en el archivo de log (log.out)
        - No se deben generar archivos FASTA para las filas con coordenadas incompletas.

    ```pyhton
        mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/
    ```

    ```
        Error: Incomplete peak coordinates in the peak file. Check the log.out file
    ```

    ```bash
        #Comando para Verificar la Salida:
        ls
    ```

    ```bash
        #Salida Esperada:
        log.out
        fasta_peaks/
    ```

5. **Caso: Archivo de picos mal formateado (columnas faltantes)**

    - **Entradas:**
        - Archivo de picos con columnas faltantes (por ejemplo, falta 'Peak_start' o 'TF_name').
        - Archivo FASTA del genoma válido.
        - Directorio de salida.
     
    - **Esperado:**
        - El sistema debe imprimir un mensaje de error: "Error: Invalid peak file format. Missing required columns."
        - No se deben generar archivos FASTA

    ```python
        mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/
    ```

    ```
        Error: Invalid peak file format. Missing required columns.
    ```

6. **Caso: Archivo de secuencia mal formateado**

     - **Entradas:**
        - Archivo de picos válido
        - Archivo FASTA del genoma inválido.
        - Directorio de salida.
     
    - **Esperado:**
        - El sistema debe imprimir un mensaje de error: "Error: Invalid FASTA format. Missing information."
        - No se deben generar archivos FASTA

    ```python
        mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/
    ```

    ```
        Error: Invalid genome file format. Missing required columns.
    ```

7. **Caso: Archivo de picos con valores no numéricos en 'Peak_start' o 'Peak_end'.**

    - **Entradas:**
        - Archivo de picos con valores no numéricos en Peak_start o Peak_end.
        - Archivo FASTA del genoma válido.
        - Directorio de salida.

    - **Esperado:**
        - El sistema debe imprimir un mensaje de error: "Error: Non-numeric values in Peak_start or Peak_end."
        - No se deben generar archivos FASTA para las filas con valores no numéricos.
        - Registrar el error en el archivo de log (log.out)

     ```pyhton
        mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/
    ```

    ```
        Error: Non-numeric values in Peak_start or Peak_end.
    ```

    ```bash
        #Comando para Verificar la Salida:
        ls
    ```

    ```bash
        #Salida Esperada:
        log.out
        fasta_peaks/
    ```

8. **Caso : Directorio de salida no existe**

    - **Entradas**
        - Archivo de picos válido.
        - Archivo FASTA del genoma válido.
        - Directorio de salida inexistente.

    - **Esperado**
        - El sistema debe crear el directorio de salida automáticamente.
        - Se deben generar los archivos FASTA en el directorio creado.
        - Registrar un mensaje en el archivo de log (log.out) indicando que el directorio fue creado.
     

    ```python
        mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/
    ```

    ```
        Directory "fasta_peaks/" created successfully.
    ```

    ```
        #Contenido del archivo log.out
        Info: Directory "fasta_peaks/" created successfully.
    ```

    ```bash
        ls
    ```

    ```bash
        fasta_peaks/
    ```
