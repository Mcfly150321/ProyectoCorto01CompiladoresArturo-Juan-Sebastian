import re
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Carga las variables de entorno desde un archivo .env si existe
load_dotenv()

# --- 1. LÓGICA DE PARSEO ---
def leer_y_parsear_reporte(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        texto = f.read()

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

    # 1. Parsear Totales
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

# --- 2. LÓGICA DE GENERACIÓN DE PDF ---
def generar_pdf_reporte1(data, nombre_archivo="Reporte_Estadistico.pdf"):
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elementos = []
    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1A365D"), spaceAfter=15, alignment=1)
    elementos.append(Paragraph("REPORTE LÉXICO #1: ESTADÍSTICAS GENERALES Y TOTALES", estilo_titulo))
    elementos.append(Spacer(1, 10))

    totales = data.get("totales", {})
    datos_tabla = [["Métrica / Elemento del Análisis", "Cantidad Total"]]
    for k, v in totales.items():
        datos_tabla.append([k.replace("_", " ").capitalize(), str(v)])

    tabla_totales = Table(datos_tabla, colWidths=[320, 150])
    tabla_totales.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#EDF2F7")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
    ]))
    elementos.append(tabla_totales)
    elementos.append(Spacer(1, 20))

    elementos.append(Paragraph("Resumen de Palabras Reservadas Encontradas", styles['Heading2']))
    elementos.append(Spacer(1, 8))

    pr_desc = data.get("resumen_palabras_reservadas", [])
    if pr_desc:
        datos_pr = [["Palabra Reservada", "Apariciones"]]
        for item in pr_desc:
            datos_pr.append([str(item.get("palabra", "")), str(item.get("apariciones", ""))])
        
        tabla_pr = Table(datos_pr, colWidths=[320, 150])
        tabla_pr.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#2C5282")),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        elementos.append(tabla_pr)
    else:
        estilo_aviso = ParagraphStyle('Aviso', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor("#4A5568"))
        elementos.append(Paragraph("No se registraron palabras reservadas en este análisis.", estilo_aviso))

    doc.build(elementos)
    print(f"[PDF Generado] '{nombre_archivo}' creado exitosamente.")

def generar_pdf_reporte2(data, nombre_archivo="Reporte_Tabla_Simbolos.pdf"):
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elementos = []
    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1A365D"), spaceAfter=15, alignment=1)
    elementos.append(Paragraph("REPORTE LÉXICO #2: TABLA DE SÍMBOLOS (IDENTIFICADORES)", estilo_titulo))
    elementos.append(Spacer(1, 10))

    identificadores = data.get("identificadores", [])
    
    if identificadores:
        elementos.append(Paragraph("Detalle de Identificadores Encontrados", styles['Heading2']))
        elementos.append(Spacer(1, 5))

        datos = [["Lexema", "Línea", "Token", "Ámbito"]]
        for it in identificadores:
            datos.append([
                str(it.get("lexema", "")), 
                str(it.get("linea", "")), 
                str(it.get("token", "")), 
                str(it.get("ambito", "-"))
            ])

        tabla_ids = Table(datos, colWidths=[150, 70, 160, 90])
        tabla_ids.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4A5568")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")])
        ]))
        elementos.append(tabla_ids)
    else:
        estilo_aviso = ParagraphStyle('Aviso', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor("#4A5568"))
        elementos.append(Paragraph("No se registraron identificadores en la tabla de símbolos para este análisis.", estilo_aviso))

    doc.build(elementos)
    print(f"[PDF Generado] '{nombre_archivo}' creado exitosamente.")

# --- 3. FLUJO PRINCIPAL ---
if __name__ == "__main__":
    archivo_entrada = "resultado.txt"

    print(f"[*] Leyendo y parseando el archivo '{archivo_entrada}'...")
    json_resultado = leer_y_parsear_reporte(archivo_entrada)

    try:
        mongouri = "mongodb+srv://sebaselcrackrodaspineda_db_user:HHC7k0lZguGZd9sN@cluster0.6lehjnv.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(mongouri, tls=True, tlsAllowInvalidCertificates=True)
        db = client["compiladores_db"]
        coleccion = db["analisis_lexico"]

        # Insertar documento y capturar su ID exacto
        resultado_id = coleccion.insert_one(json_resultado).inserted_id
        print(f"[Éxito] Datos insertados con ID: {resultado_id}")

        print("[*] Generando reportes PDF...")
        # Generar usando directamente el objeto parseado (o si prefieres buscar por ID: coleccion.find_one({"_id": resultado_id}))
        generar_pdf_reporte1(json_resultado, "Reporte_Estadistico.pdf")
        generar_pdf_reporte2(json_resultado, "Reporte_Tabla_Simbolos.pdf")
        
        print("[Éxito] Proceso completado correctamente.")

    except Exception as e:
        print(f"[Error]: {e}")