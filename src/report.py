

## Envio de Mensaje

import sqlite3
import pandas as pd
from pathlib import Path
from twilio.rest import Client
import json
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv(rf"C:\Users\PC\Desktop\Proyectos\Proyectos_Py\9.Tasas_Interes\src\.env")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

path_bd = Path(r"C:\Users\PC\Desktop\Proyectos\Proyectos_Py\9.Tasas_Interes\data\base\tasa_interes.db")
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN


def crear_mensaje_reporte():
    conn = sqlite3.connect(path_bd)

    query = """
    SELECT Bancos, tasa_interes, Fecha_Norm
    FROM tasa_dia
    WHERE Tipo_Tasa = 'Préstamos hipotecarios para vivienda'
    AND tasa_interes IS NOT NULL
    AND Fecha_Norm = (SELECT MAX(Fecha_Norm) FROM tasa_dia)
    ORDER BY tasa_interes ASC
    LIMIT 10
    """

    data = pd.read_sql_query(query, conn)
    conn.close()

    if data.empty:
        return "No se encontraron tasas hipotecarias."

    fecha = data["Fecha_Norm"].iloc[0]

    mensaje = f"Tasas hipotecarias mas bajas - {fecha}\n\n"

    for i, row in data.iterrows():
        mensaje += f"{i + 1}. {row['Bancos']}: {row['tasa_interes']}%\n"

    return mensaje



def enviar_whatsapp_twilio(mensaje):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=TWILIO_FROM,
        body=mensaje,
        to=TWILIO_TO
    )

    print("Mensaje enviado por Twilio.")
    print("SID:", message.sid)


mensaje = crear_mensaje_reporte()
print(mensaje)
enviar_whatsapp_twilio(mensaje)

