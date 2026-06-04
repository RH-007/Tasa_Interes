
## Transformacion de datos

## librerias
import pandas as pd
import datetime as dt
from pathlib import Path

## Ruta de archivos

path_raw = Path(r"C:\Users\PC\Desktop\Proyectos\Proyectos_Py\9.Tasas_Interes\data\raw")
path_processed = Path(r"C:\Users\PC\Desktop\Proyectos\Proyectos_Py\9.Tasas_Interes\data\processed")


## Rango de fechas
fecha_inicio = "2026-01-05"
fecha_fin = dt.date.today()

fechas = pd.date_range(
    start=fecha_inicio,
    end=fecha_fin,
    freq="B"
)

fecha_consulta = []

for fecha in fechas:

    periodo = fecha.strftime("%Y%m")   # YYYYMM
    fecha_str = fecha.strftime("%d_%m_%Y")

    nombre_archivo = f"tasa_interes_{fecha_str}_{periodo}.xlsx"

    fecha_consulta.append({
        "periodo": periodo,
        "fecha": fecha_str,
        "nombre_archivo": nombre_archivo
    })


data_tasas = []

for archivo in fecha_consulta:

    nombre_archivo = archivo["nombre_archivo"]

    path_file = path_raw / nombre_archivo

    try:

        data = pd.read_excel(
            path_file
            , skiprows = 6
            , skipfooter= 3
        )

        data.dropna(axis=1, how="all", inplace=True)
        data["Periodo"] = archivo["periodo"]
        data["Fecha"] = archivo["fecha"]


        data_tasas.append(data)
    
    except FileNotFoundError:
        print("Archivo No Encontrado", nombre_archivo)
        


data_tasas_final = []

for data_i in data_tasas:
    
    data_final_pv = pd.melt(data_i
                    , id_vars= ['Periodo', 'Fecha' , 'Tasa Anual (%)']
                    , var_name= "Bancos" 
                    , value_name="tasa_interes")
    
    data_tasas_final.append(data_final_pv)
    
    
## uninedo informacion    
data_tasas_final_df = pd.concat(data_tasas_final, ignore_index=True, axis = 0)


## conversion de tipos de datos
data_tasas_final_df["Tipo_Tasa"] = (data_tasas_final_df["Tasa Anual (%)"].str.strip())
data_tasas_final_df["Fecha_Norm"] = pd.to_datetime(data_tasas_final_df["Fecha"], format="%d_%m_%Y")
data_tasas_final_df["tasa_interes"] = pd.to_numeric(data_tasas_final_df["tasa_interes"], errors="coerce")

## filtrado de tipo de datp
tasas_interes = [
    "Consumo",
    "Tarjetas de Crédito",
    "Préstamos Revolventes",
    "Préstamos no  Revolventes para automóviles",
    "Préstamos no  Revolventes para libre disponibilidad hasta 360 días",
    "Préstamos no  Revolventes para libre disponibilidad a más de 360 días", 
    "Préstamos hipotecarios para vivienda"
]
data_tasa_final_df_f = data_tasas_final_df[data_tasas_final_df["Tipo_Tasa"].isin(tasas_interes)]



df_tasas_final = data_tasa_final_df_f[["Periodo","Fecha_Norm", "Bancos", "Tipo_Tasa", "tasa_interes"]].copy()

## guardando resultado final
df_tasas_final.to_excel(path_processed / "tasa_interes_final.xlsx", index=False)

print("Archivo final guardado en carpeta processed!")