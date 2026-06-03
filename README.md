# Tasas de Interes del Sistema Financiero

Proyecto en Python para descargar, transformar y guardar informacion de tasas de interes del sistema financiero peruano desde la pagina de la SBS.

## Objetivo

Automatizar el proceso de consulta de tasas de interes, procesar los archivos Excel descargados y guardar la informacion final en una base de datos SQLite.

## Estructura del proyecto

```text
9.Tasas_Interes/
├── data/
│   ├── raw/          # Archivos descargados desde la SBS
│   ├── processed/    # Archivo final procesado
│   └── tasa_interes.db
├── src/
│   ├── extract.py    # Descarga los archivos de tasas
│   ├── transform.py  # Limpia y transforma la informacion
│   ├── load.py       # Guarda la data en SQLite
│   ├── main.py       # Ejecuta todo el pipeline
│   └── report.py     # Reportes futuros
└── README.md
```

## Flujo del pipeline

```text
Extract  ->  Transform  ->  Load

Descargar datos  ->  Procesar datos  ->  Guardar en base de datos
```

## Como ejecutar el proyecto

Desde la carpeta principal del proyecto:

```powershell
cd "C:\Users\PC\Desktop\Proyectos\Proyectos_Py\9.Tasas_Interes"
python src\main.py
```

## Etapas del proceso

### 1. Extract

El archivo `extract.py` descarga los archivos Excel desde la pagina de la SBS y los guarda en:

```text
data/raw/
```

### 2. Transform

El archivo `transform.py` lee los archivos descargados, limpia la informacion, transforma la data a formato largo y genera el archivo final:

```text
data/processed/tasa_interes_final.xlsx
```

### 3. Load

El archivo `load.py` carga la informacion procesada en una base SQLite:

```text
data/tasa_interes.db
```

Tambien muestra un ranking de tasas hipotecarias para vivienda.

## Estado del proyecto

Proyecto en desarrollo.

Proximas mejoras:

- Convertir los scripts en funciones.
- Agregar reportes automaticos.
- Mejorar el manejo de errores.
- Automatizar el envio del resumen.
