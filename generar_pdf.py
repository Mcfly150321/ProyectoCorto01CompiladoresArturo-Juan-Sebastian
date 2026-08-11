import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Cargar variables de entorno
load_dotenv()

def obtener_ultimo_registro_db():
    try:
        mongo_uri = "mongodb+srv://sebaselcrackrodaspineda_db_user:HHC7k0lZguGZd9sN@cluster0.6lehjnv.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(mongo_uri)
        db = client["compiladores_db"]
        coleccion = db["analisis_lexico"]

        # Obtener el último documento insertado ordenando por _id descendente
        ultimo_registro = coleccion.find().sort("_id", -1).limit(1)
        registro = list(ultimo_registro)

        if registro:
            print("[Éxito] Último registro obtenido de MongoDB.")
            return registro[0]
        else:
            print("[Aviso] No se encontraron registros en la base de datos.")
            return None
    except Exception as e:
        print(f"[Error de Conexión a MongoDB]: {e}")
        return None

def generar_pdf_reporte1(data, nombre_archivo="Reporte_Estadistico.pdf"):
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elementos = []
    styles = getSampleStyleSheet()

    # Título Principal
    estilo_titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1A365D"), spaceAfter=15, alignment=1)
    elementos.append(Paragraph("REPORTE LÉXICO #1: ESTADÍSTICAS GENERALES Y TOTALES", estilo_titulo))
    elementos.append(Spacer(1, 10))

    # 1. Tabla basada en el diccionario "totales"
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

    # 2. Tabla basada en "resumen_palabras_reservadas"
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
        # Mensaje limpio si la lista está vacía
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

    # Extracción y estructuración específica de la sección de identificadores
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

if __name__ == "__main__":
    print("[*] Consultando el último registro en MongoDB...")
    registro_db = obtener_ultimo_registro_db()

    if registro_db:
        # Limpiar el ObjectId de mongo para que sea un diccionario de python estándar
        if "_id" in registro_db:
            del registro_db["_id"]

        print("[*] Generando Reporte 1 en PDF...")
        generar_pdf_reporte1(registro_db, "Reporte_Estadistico.pdf")

        print("[*] Generando Reporte 2 en PDF...")
        generar_pdf_reporte2(registro_db, "Reporte_Tabla_Simbolos.pdf")
    else:
        print("[Error] No se pudo generar ningún PDF porque no hay datos disponibles en la base de datos.")