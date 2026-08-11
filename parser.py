import re
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env si existe
load_dotenv()

def leer_y_parsear_reporte(ruta_archivo):
    # Lee el archivo de texto generado por tu analizador léxico de Flex
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        texto = f.read()

    # Diccionario base para estructurar el JSON dinámicamente
    documento = {
        "totales": {},
        "resumen_palabras_reservadas": [],
        "enteros": [],
        "flotantes": [],
        "identificadores": [],
        "booleanos": [],
        "operadores": [],
        "palabras_reservadas": [],
        "errores_lexicos": []
    }

    # 1. Parsear Totales (Reporte 1 - Cantidades Totales)
    totales_regex = re.findall(r"(.+?):\s*(\d+)", texto)
    for clave, valor in totales_regex[:9]:
        key_limpia = clave.strip().lower().replace("cantidad de ", "").replace(" ", "_")
        documento["totales"][key_limpia] = int(valor)

    # 2. Parsear Conteo Descendente de Palabras Reservadas
    pr_desc = re.findall(r"Palabra:\s+(\w+)\s+\|\s+Apariciones:\s+(\d+)", texto)
    for palabra, apariciones in pr_desc:
        documento["resumen_palabras_reservadas"].append({
            "palabra": palabra,
            "apariciones": int(apariciones)
        })

    # 3. Extracción Dinámica de Enteros
    ent_raw = re.search(r"--- Conteo de Enteros ---(.*?)(--- Conteo de Flotantes ---|$)", texto, re.DOTALL)
    if ent_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", ent_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["enteros"].append(item)

    # 4. Extracción Dinámica de Flotantes
    float_raw = re.search(r"--- Conteo de Flotantes ---(.*?)(--- Conteo de Identificadores|$)", texto, re.DOTALL)
    if float_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", float_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["flotantes"].append(item)

    # 5. Extracción Dinámica de Identificadores (Tabla de Símbolos)
    id_raw = re.search(r"--- Conteo de Identificadores \(Tabla de Simbolos\) ---(.*?)(--- Conteo de Booleanos|$)", texto, re.DOTALL)
    if id_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)\s+\|\s+Ambito:\s+(?P<ambito>\S+)", id_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["identificadores"].append(item)

    # 6. Extracción Dinámica de Booleanos
    bool_raw = re.search(r"--- Conteo de Booleanos ---(.*?)(--- Conteo de Operadores|$)", texto, re.DOTALL)
    if bool_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", bool_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["booleanos"].append(item)

    # 7. Extracción Dinámica de Operadores
    op_raw = re.search(r"--- Conteo de Operadores ---(.*?)(--- Conteo de Palabras Reservadas|$)", texto, re.DOTALL)
    if op_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>.+?)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", op_raw.group(1)):
            item = m.groupdict()
            item["lexema"] = item["lexema"].strip()
            item["linea"] = int(item["linea"])
            documento["operadores"].append(item)

    # 8. Extracción Dinámica de Palabras Reservadas (Detalle)
    pr_raw = re.search(r"--- Conteo de Palabras Reservadas ---(.*?)(--- Conteo de Errores Lexicos|$)", texto, re.DOTALL)
    if pr_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", pr_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["palabras_reservadas"].append(item)

    return documento

if __name__ == "__main__":
    # Nombre del archivo de salida generado por tu analizador (ej: ./proyecto_corto < prueba.groovy > resultado.txt)
    archivo_entrada = "resultado.txt"

    print(f"[*] Leyendo y parseando el archivo '{archivo_entrada}'...")
    json_resultado = leer_y_parsear_reporte(archivo_entrada)

    # Mostrar JSON generado en consola
    print("\n--- JSON Estructurado Resultante ---")
    print(json.dumps(json_resultado, indent=4, ensure_ascii=False))

    # Conectar y subir a MongoDB (usando variable de entorno o fallback local)
    try:
        mongouri = "mongodb+srv://sebaselcrackrodaspineda_db_user:HHC7k0lZguGZd9sN@cluster0.6lehjnv.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(mongouri,tls=True, tlsAllowInvalidCertificates=True)
        db = client["compiladores_db"]
        coleccion = db["analisis_lexico"]

        resultado_id = coleccion.insert_one(json_resultado).inserted_id
        print(f"\n[Éxito] Reporte parseado e insertado en MongoDB con el ID: {resultado_id}")

    except Exception as e:
        print(f"\n[Error de Conexión a MongoDB]: {e}")