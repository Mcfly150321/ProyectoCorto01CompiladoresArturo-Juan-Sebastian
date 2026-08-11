import os
import subprocess
import re
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pymongo import MongoClient
from dotenv import load_dotenv

# ReportLab para los PDFs
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

load_dotenv()


# --- 1. LÓGICA DE PARSEO DEL TXT ---
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

    totales_regex = re.findall(r"(.+?):\s*(\d+)", texto)
    for clave, valor in totales_regex[:9]:
        key_limpia = clave.strip().lower().replace("cantidad de ", "").replace(" ", "_")
        documento["totales"][key_limpia] = int(valor)

    pr_desc = re.findall(r"Palabra:\s+(\w+)\s+\|\s+Apariciones:\s+(\d+)", texto)
    for palabra, apariciones in pr_desc:
        documento["resumen_palabras_reservadas"].append({
            "palabra": palabra,
            "apariciones": int(apariciones)
        })

    ent_raw = re.search(r"--- Conteo de Enteros ---(.*?)(--- Conteo de Flotantes ---|$)", texto, re.DOTALL)
    if ent_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", ent_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["enteros"].append(item)

    float_raw = re.search(r"--- Conteo de Flotantes ---(.*?)(--- Conteo de Identificadores|$)", texto, re.DOTALL)
    if float_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", float_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["flotantes"].append(item)

    id_raw = re.search(r"--- Conteo de Identificadores \(Tabla de Simbolos\) ---(.*?)(--- Conteo de Booleanos|$)", texto, re.DOTALL)
    if id_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)\s+\|\s+Ambito:\s+(?P<ambito>\S+)", id_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["identificadores"].append(item)

    bool_raw = re.search(r"--- Conteo de Booleanos ---(.*?)(--- Conteo de Operadores|$)", texto, re.DOTALL)
    if bool_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", bool_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["booleanos"].append(item)

    op_raw = re.search(r"--- Conteo de Operadores ---(.*?)(--- Conteo de Palabras Reservadas|$)", texto, re.DOTALL)
    if op_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>.+?)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", op_raw.group(1)):
            item = m.groupdict()
            item["lexema"] = item["lexema"].strip()
            item["linea"] = int(item["linea"])
            documento["operadores"].append(item)

    pr_raw = re.search(r"--- Conteo de Palabras Reservadas ---(.*?)(--- Conteo de Errores Lexicos|$)", texto, re.DOTALL)
    if pr_raw:
        for m in re.finditer(r"Lexema:\s+(?P<lexema>\S+)\s+\|\s+Linea:\s+(?P<linea>\d+)\s+\|\s+Token:\s+(?P<token>\S+)", pr_raw.group(1)):
            item = m.groupdict()
            item["linea"] = int(item["linea"])
            documento["palabras_reservadas"].append(item)

    return documento


# --- 2. LÓGICA DE GENERACIÓN DE PDF DESDE LA DATA OBTENIDA DE DB ---
def generar_pdf_reporte1(data, nombre_archivo):
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

def generar_pdf_reporte2(data, nombre_archivo):
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

def exportar_salida_a_pdfs_desde_db(ruta_txt, nombre_base):
    # 1. Parsear el archivo .txt generado en output
    json_data = leer_y_parsear_reporte(ruta_txt)

    # 2. Conectar a MongoDB e insertar
    mongouri = "mongodb+srv://sebaselcrackrodaspineda_db_user:HHC7k0lZguGZd9sN@cluster0.6lehjnv.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongouri, tls=True, tlsAllowInvalidCertificates=True)
    db = client["compiladores_db"]
    coleccion = db["analisis_lexico"]

    resultado_id = coleccion.insert_one(json_data).inserted_id
    print(f"[Éxito] Documento insertado en MongoDB con ID: {resultado_id}")

    # 3. Obtener la data DIRECTAMENTE de la Base de Datos usando el ID retornado
    registro_desde_db = coleccion.find_one({"_id": resultado_id})

    if not registro_desde_db:
        raise Exception("No se pudo recuperar el registro desde MongoDB usando el ID.")

    # 4. Generar PDFs usando la data recuperada de la DB
    base_dir = os.path.dirname(os.path.abspath(ruta_txt))
    pdf1_path = os.path.join(base_dir, f"Reporte_Estadistico_{nombre_base}.pdf")
    pdf2_path = os.path.join(base_dir, f"Reporte_Tabla_Simbolos_{nombre_base}.pdf")

    generar_pdf_reporte1(registro_desde_db, pdf1_path)
    generar_pdf_reporte2(registro_desde_db, pdf2_path)


# --- 3. INTERFAZ GRÁFICA ---
class AppInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Archivos y Terminal Consola (Fish)")
        self.root.geometry("700x550")
        self.root.minsize(600, 400)
        self.root.configure(bg="#f0f2f5")
        self._crear_widgets()

    def _crear_widgets(self):
        frame_archivo = ttk.LabelFrame(self.root, text=" 📁 Archivo ", padding=10)
        frame_archivo.pack(side="top", fill="x", padx=15, pady=5)

        self.lbl_archivo = ttk.Label(frame_archivo, text="Ningún archivo seleccionado", font=("Segoe UI", 9, "italic"))
        self.lbl_archivo.pack(side="left", fill="x", expand=True, padx=5)

        btn_seleccionar = ttk.Button(frame_archivo, text="Seleccionar Archivo", command=self.procesar_archivo)
        btn_seleccionar.pack(side="right", padx=5)

        frame_input = ttk.Frame(self.root, padding=10)
        frame_input.pack(side="bottom", fill="x", padx=15, pady=5)

        lbl_prompt = ttk.Label(frame_input, text="> Comando:", font=("Consolas", 10, "bold"))
        lbl_prompt.pack(side="left", padx=(0, 5))

        self.ent_comando = ttk.Entry(frame_input, font=("Consolas", 10))
        self.ent_comando.pack(side="left", fill="x", expand=True, padx=5)
        self.ent_comando.bind("<Return>", lambda event: self.ejecutar_comando_manual())

        btn_ejecutar = ttk.Button(frame_input, text="Ejecutar", command=self.ejecutar_comando_manual)
        btn_ejecutar.pack(side="right", padx=5)

        frame_consola = ttk.LabelFrame(self.root, text=" 🖥️ Consola / Resultados ", padding=10)
        frame_consola.pack(side="top", fill="both", expand=True, padx=15, pady=5)

        self.txt_salida = tk.Text(frame_consola, bg="#1e1e1e", fg="#00ff66", insertbackground="white", font=("Consolas", 10), wrap="word", height=12)
        self.txt_salida.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_consola, orient="vertical", command=self.txt_salida.yview)
        scrollbar.pack(side="right", fill="y")
        self.txt_salida.config(yscrollcommand=scrollbar.set)

    def imprimir_en_consola(self, texto):
        self.txt_salida.insert(tk.END, texto + "\n")
        self.txt_salida.see(tk.END)

    def ejecutar_comando_sistema(self, comando):
        try:
            ruta_fish = "/usr/bin/fish" if os.path.exists("/usr/bin/fish") else "fish"
            resultado = subprocess.run(
                comando, shell=True, executable=ruta_fish, capture_output=True, text=True, encoding="utf-8", errors="replace"
            )
            if resultado.stdout:
                self.imprimir_en_consola(resultado.stdout.strip())
            if resultado.stderr:
                self.imprimir_en_consola(f"[ERROR]: {resultado.stderr.strip()}")
        except Exception as e:
            self.imprimir_en_consola(f"[EXCEPCIÓN]: {str(e)}")

    def procesar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=[("Todos los archivos", "*.*"), ("Groovy", "*.groovy"), ("Texto plano", "*.txt")]
        )

        if not ruta_archivo:
            return

        nombre_archivo_con_ext = os.path.basename(ruta_archivo)
        nombre_sin_ext, _ = os.path.splitext(nombre_archivo_con_ext)
        
        self.lbl_archivo.config(text=f"Seleccionado: {nombre_archivo_con_ext}")
        self.imprimir_en_consola(f"\n--- Procesando archivo: {nombre_archivo_con_ext} ---")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        dir_output = os.path.join(base_dir, "output")
        os.makedirs(dir_output, exist_ok=True)

        nombre_txt = f"salida_{nombre_sin_ext}.txt"
        ruta_salida_absoluta = os.path.join(dir_output, nombre_txt)
        ruta_binario_absoluta = os.path.join(base_dir, "Edicion2", "edicion2")

        try:
            with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f_in:
                contenido_archivo = f_in.read()

            resultado_proceso = subprocess.run(
                [ruta_binario_absoluta],
                input=contenido_archivo,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            with open(ruta_salida_absoluta, "w", encoding="utf-8") as f_out:
                f_out.write(resultado_proceso.stdout)

            if resultado_proceso.stdout:
                self.imprimir_en_consola(resultado_proceso.stdout.strip())
            if resultado_proceso.stderr:
                self.imprimir_en_consola(f"[ERROR]: {resultado_proceso.stderr.strip()}")

        except Exception as e:
            self.imprimir_en_consola(f"[EXCEPCIÓN]: {str(e)}")

        self.imprimir_en_consola("Enviando a MongoDB y generando PDFs desde la DB...")
        
        try:
            exportar_salida_a_pdfs_desde_db(ruta_salida_absoluta, nombre_sin_ext)
            self.imprimir_en_consola("¡Datos subidos a MongoDB y PDFs creados con éxito desde la DB!")
        except Exception as e:
            self.imprimir_en_consola(f"[ERROR DB/PDF]: {str(e)}")

    def ejecutar_comando_manual(self):
        comando = self.ent_comando.get().strip()
        if not comando:
            return

        self.imprimir_en_consola(f"\n$ {comando}")
        self.ejecutar_comando_sistema(comando)
        self.ent_comando.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppInterfaz(root)
    root.mainloop()