

## Extract: Tasa de Interes - Sistema Bancario

## Librerias
import datetime as dt
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import os


print("Iniciando proceso de extracción de tasas de interés...")

## Website de consulta
web = "https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIActivaTipoCreditoEmpresa.aspx?tip=B"

path_raw = rf"C:\Users\PC\Desktop\Proyectos\Proyectos_Py\9.Tasas_Interes\data\raw"

## rango de fechas
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
    

print("Fecha a Extraer:", fecha_consulta[-1]['fecha'])
    

## Configuracion del driver
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": path_raw,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

url = "https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIActivaTipoCreditoEmpresa.aspx?tip=B"
driver.get(url)



def consulta_tasa_interes(input_fecha: str):

    wait = WebDriverWait(driver, 10)

    # INGRESAR FECHA
    fecha_input = wait.until(
        EC.presence_of_element_located((By.ID, "ctl00_cphContent_rdpDate_dateInput"))
    )

    fecha_input.clear()
    fecha_input.send_keys(input_fecha)

    time.sleep(3)

    # CLICK CONSULTAR
    consultar_btn = driver.find_element(By.ID, "ctl00_cphContent_btnConsultar")
    consultar_btn.click()

    time.sleep(3)

    # CLICK EXPORTAR (esperar que sea clickeable)}
    try:
        exportar_btn = wait.until(
            EC.presence_of_element_located((By.ID, "ctl00_cphContent_btnExportar"))
        )
        exportar_btn.click()
        print(f"Descarga iniciada para {input_fecha}")
        return True

    except TimeoutException:
        print(f"No existe botón exportar para {input_fecha}")
        return False
    
def renombrar_ultimo_archivo(path_raw, nuevo_nombre):

    time.sleep(3) 

    archivos = []

    for f in os.listdir(path_raw):
        if f.endswith(".xlsx"):
            archivos.append(f)

    if not archivos:
        raise FileNotFoundError("No se encontró archivo descargado.")

    # tomar el archivo más reciente
    rutas = []

    for f in archivos:
        ruta = os.path.join(path_raw, f)
        rutas.append(ruta)
    
    archivo_reciente = max(rutas, key=os.path.getctime)

    nueva_ruta = os.path.join(path_raw, nuevo_nombre)

    os.rename(archivo_reciente, nueva_ruta)

    print(f"Archivo guardado como: {nuevo_nombre}")



ultima_fecha = fecha_consulta[-1]

fecha = ultima_fecha['fecha']
periodo = ultima_fecha['periodo']
nombre_archivo = ultima_fecha['nombre_archivo']  # ejemplo: Tasa_201901.xls

print(f"Descargada  - Fecha consulta: {fecha}")

descarga_ok = consulta_tasa_interes(fecha)

if descarga_ok:
    renombrar_ultimo_archivo(path_raw, nombre_archivo)