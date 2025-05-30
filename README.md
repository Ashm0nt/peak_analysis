
# Extracción de sitios de unión de unión de TF obtenidos a través de ChIP-seq en _Escherichia coli_ 

### Metadatos
- Fecha: 29-05-2025
- Nombre: Ashley Yael Montiel Vargas 
- Correo: yaelmont@lcg.unam.mx

## Resumen

Este proyecto automatiza la extracción reproducible de las secuencias genómicas correspondientes a los picos de unión de 139 factores de transcripción en el genoma de Escherichia coli, obtenidos mediante ChIP-Seq. A partir de un archivo de picos y la referencia FASTA del genoma, genera automáticamente archivos FASTA individuales para cada TF, listos para su análisis de motivos.

## Datos de entrada

### 1. Archivo de Picos
Contiene información sobre las regiones de unión de los 139 factores de transcripción. Se organiza en las siguientes columnas:

- **Dataset_Ids**: Identificadores de los datasets. Cada identificador representa un experimento o condición específica bajo la cual se identificaron los sitios de unión para el TF correspondiente.
- **TF_name**: Nombre del factor de transcripción que se une a la secuencia de ADN especificada.
- **Peak_start**: Posición inicial del pico de unión en el genoma.
- **Peak_end**: Posición final del pico de unión en el genoma.
- **Peak_center**: Posición central del pico de unión en el genoma.
- **Peak_number**: Número secuencial del pico, útil para referencias internas dentro del mismo conjunto de datos.
- **Max_Fold_Enrichment**: Enriquecimiento máximo observado en el pico.
- **Max_Norm_Fold_Enrichment**: Enriquecimiento máximo normalizado.
- **Proximal_genes**: Genes próximos al sitio de unión.
- **Center_position_type**: Tipo de posición central del pico (por ejemplo, intergénica, intrónica, etc.).

Es necesario que contenga tres columnas: `TF_name`, `Peak_start`, `Peak_end` para que se puedea llevar a cabo el análisis

### 2.Genoma Completo de E. coli
Archivo FASTA De referencia

## Objetivos del Proyecto

- **Extraer**: leer coordenadas de picos y extraer la secuencia genómica en el cromosoma forward.  
- **Agrupar**: para cada `TF_name`, reunir todas sus secuencias de picos.  
- **Generar FASTA**: crear `TF_name.fa` con un header descriptivo.  
- **Reportar**: registrar logs y generar un archivo con estadísticas (líneas procesadas, picos válidos/inválidos, errores y advertencias).

## Uso

```bash
python main.py  --peaks path/to/peaks.tsv \
  --genome path/to/ecoli.fa \
  --outdir output/fasta \
  --log-dir logs \
  --verbose \
  --line_length 80
```

--peaks <file>: TSV con columnas mínimas TF_name, Peak_start, Peak_end.

--genome <file>: FASTA del genoma de E. coli.

--outdir <dir>: Directorio donde se escribirán los FASTA. (Se crea si no existe.)

--log-dir <dir>: Carpeta destino para los logs de ejecución.

--verbose: Activa logging en nivel DEBUG.

--line_leght: Especifica el numero de caracteres por línea de la secuencia

## Salida

### 1.Archivos FASTA
Los archivos generados se alamcenan en un directorio que el usuario especifique, o en su defecto se crea un directorio para almacenarlos

- output/fasta/<TF_name>.fa
- Cada header contiene: >TF_name_pico_<n>_len=<longitud>

### 2.Logs
Archivo que contiene toda la información de la ejecución del programa, puede ser solo de información o modo DEBUG. 

#### Validación de archivos

- Confirmación de existencia y accesos del TSV de picos y del FASTA del genoma.

- Error crítico y aborta si faltan o no son legibles.

#### Estadísticas de lectura de picos

- Líneas procesadas (excluyendo cabecera).
- Líneas vacías detectadas en el TSV.
- Picos totales (filas con datos en TF_name, Peak_start, Peak_end).
- Picos válidos: coordenadas correctamente formateadas y start < end.
- Picos inválidos: detalles de cada fila descartada, con causa:
    - Formato no numérico (ValueError).
    - Coordenadas fuera de rango o start ≥ end.
    - Campos vacíos.
- Advertencias detalladas
    - “Línea X: campos vacíos, omitiendo”
    - “Línea X: start ≥ end (Y ≥ Z), omitiendo”
    - “Línea X: error de formato en coordenadas”

- Resumen tras lectura de picos

```yaml
Copiar código
Resumen de procesamiento:
  Líneas totales: 123
  Líneas vacías: 2
  Picos totales: 121
  Picos válidos: 118
  Picos inválidos: 3
  Errores – formato: 1, coordenadas: 2, estructura: 0
  Advertencias – campos vacíos: 0
```

### Extracción de secuencias FASTA

- Confirmación de carga del genoma (Genoma cargado; longitud: 4641652 bp).

- Para cada TF:
    - “Generado FASTA: TF_name.fa (N secuencias)”.

- Advertencias de coordenadas fuera de rango durante el corte.

### Resumen final de extracción

```yaml
Extracción completada: totales=118, válidos=118, inválidos=0
```
### Errores críticos

Cualquier excepción no controlada se registra con stack trace y causa el paro del programa.

## Pruebas
Se incluye un paquete de test, con pruebas unitarias  para cada modulo, así como pruebas ejecutables.

## Codigo fuente
El código fuente está disponible en este repositorio. Se acoge con satisfacción cualquier contribución o sugerencia a través de solicitudes pull request.

## Terminos de uso
Este script está disponible bajo la licencia MIT. Consulte el archivo LICENSE para obtener más detalles sobre la licencia.

- Si utiliza este script, por favor citelo

