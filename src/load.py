

## Loas Tasa de Interes

import pandas as pd
from pathlib import Path
import sqlite3

## Ruta de archivo
path_processed = Path(r"C:\Users\PC\Desktop\Proyectos\Proyectos_Py\9.Tasas_Interes\data\processed")
path_bd = Path(r"C:\Users\PC\Desktop\Proyectos\Proyectos_Py\9.Tasas_Interes\data\base\tasa_interes.db")

data_tasas = pd.read_excel(path_processed / "tasa_interes_final.xlsx")

## Conectando a la base de datos
conn = sqlite3.connect(path_bd)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasa_dia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Periodo INTEGER,
    Fecha_Norm DATE,
    Bancos TEXT,
    Tipo_Tasa TEXT,
    tasa_interes FLOAT
)
""")

conn.commit()

## Guardando datos en la base de datos
data_tasas.to_sql(
        "tasa_dia",
        conn,
        if_exists="replace", ## append, replace, fail
        index=False
    )


query_fecha = """
SELECT MAX(Fecha_Norm) AS FechaHoy
FROM tasa_dia
"""

query = """
SELECT  *
FROM tasa_dia
WHERE Tipo_Tasa = 'Préstamos hipotecarios para vivienda'
AND Tasa_Interes IS NOT NULL
AND Fecha_Norm = (SELECT MAX(Fecha_Norm) FROM tasa_dia)
ORDER BY tasa_interes ASC
LIMIT 10
"""

fecha_max = pd.read_sql_query(query_fecha, conn)
tasa_hoy = pd.read_sql_query(query, conn)

print("Tasa de Interes para Prestamos Hipotecarios para Vivienda al día de hoy:")
print(fecha_max)
print("\n")
print(tasa_hoy)


tasa_result = {}
for i, row in tasa_hoy.iterrows():
    tasa_result[row['Bancos']] = row['tasa_interes']
    
print("\nTasa de Interes para Prestamos Hipotecarios para Vivienda al día de hoy:")
print(tasa_result)