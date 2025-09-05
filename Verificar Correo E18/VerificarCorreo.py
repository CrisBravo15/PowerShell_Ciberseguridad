import sys
import requests
import time
import getpass
import os
import logging
import csv

# Administrar loggin de actividad y errores
logging.basicConfig(
    filename="registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Especificar cual argumento es el correo a verificar
if len(sys.argv) != 2:
    print("Uso: python VerificarCorreo.py correo@example.com")
    sys.exit(1)
correo = sys.argv[1]

# Verificar que exista apikey.txt
if not os.path.exists("apikey.txt"):
    # Si no se encuentra el archivo el usuario ingresa la key
    print("No se encontró el archivo apikey.txt")
    clave = getpass.getpass("Ingresa tu API key: ")
    try:
        with open("apikey.txt", "w") as archivo:
            archivo.write(clave.strip())
    except Exception as e:
        logging.error(f"No se pudo guardar la API key: {e}")
        sys.exit(1)

# Abrir el archivo y obtener la API key
with open("apikey.txt", "r") as archivo:
    api_key = archivo.read().strip()

# Definir url y headers para realizar la llamada
url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}"
headers = {
    "hibp-api-key": api_key,
    "user-agent": "PythonScript"
}

# Probar la conexión con la API
try:
    response = requests.get(url, headers=headers)
except Exception as e:
    print("Error al conectar con la API.")
    logging.error(f"Error de conexión: {e}")
    sys.exit(1)

if response.status_code == 200:
    brechas = response.json()
    c_brechas = len(brechas)
    log = f"Consulta exitosa para {correo}. Brechas encontradas:{c_brechas}"
    logging.info(log)

    # Crear archivo de reporte CSV
    try:
        with open("reporte.csv", "w", newline='', encoding="utf-8") as ar_csv:
            writer = csv.writer(ar_csv)
            writer.writerow(["Título", "Dominio", "Fecha de Brecha",
                             "Datos comprometidos", "Verificada",
                             "Sensible"])
            # Se recorren 3 brechas de las que se localizaron
            for i, brecha in enumerate(brechas[:3]):
                nombre = brecha['Name']
                detalle_url = f"https://haveibeenpwned.com/api/v3/breach/{nombre}"
                try:
                    detalle_resp = requests.get(detalle_url, headers=headers)
                    if detalle_resp.status_code == 200:
                        detalle = detalle_resp.json()
                        writer.writerow([
                            detalle.get('Title'),
                            detalle.get('Domain'),
                            detalle.get('BreachDate'),
                            ','.join(detalle.get('DataClasses',[])),
                            "Si" if detalle.get("IsVerified") else "No",
                            "Si" if detalle.get("IsSensitive") else "No"
                        ])
                    else:
                        msj = f"No se pudo obtener detalles de la brecha: {nombre}"
                        msj += f"Código: {detalle_resp.status_code}"
                        logging.error(msj)
                except Exception as e:
                    log = f"Error al consultar detalles de la brecha {nombre}: {e}"
                    logging.error(log)
                if i < 2:
                    # Delay entre consultas
                    time.sleep(10)
    except Exception as e:
        print("Error al generar el archivo CSV.")
        logging.error(f"Error al escribir reporte.csv: {e}")
        sys.exit(1)
    print("Consulta completada.")
    print("Revisa el archivo reporte.csv para ver los resultados")

elif response.status_code == 404:
    print(f"La cuenta {correo} no aparece en ninguna brecha conocida")
    logging.info(f"Consulta exitosa para {correo}. No se encontraron brechas")
elif response.status_code == 401:
    print("Error de autenticación: revisa tu API key.")
    logging.error("Error 401: API key inválida")
else:
    print(f"Error inesperado. Código de estado: {response.status_code}")
    error = f"Error inesperado. Código de estado: {response.status_code}"
    logging.error(error)
