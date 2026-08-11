# ==========================================
# MÓDULO: generador_pdfs.py
# (Guarda este código en un archivo llamado generador_pdfs.py)
# ==========================================

import os
from fpdf import FPDF

# Directorio base para guardar los PDFs generados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_PDFS = os.path.join(BASE_DIR, "pdfs")
os.makedirs(TMP_PDFS, exist_ok=True)


class PDFReporte(FPDF):
    def __init__(self, titulo_reporte):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.titulo_reporte = titulo_reporte
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, self.titulo_reporte, border=0, ln=1, align="C")
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")


def _generar_pdf_individual(titulo, contenido_lineas, nombre_archivo_salida):
    pdf = PDFReporte(titulo_reporte=titulo)
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font("Courier", size=9)
    pdf.set_text_color(20, 20, 20)

    for linea in contenido_lineas:
        linea_limpia = linea.replace("\xa0", " ")
        if linea_limpia.startswith("---"):
            pdf.ln(2)
            pdf.set_font("Courier", "B", 10)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(0, 5, linea_limpia)
            pdf.set_font("Courier", "", 9)
            pdf.set_text_color(20, 20, 20)
        else:
            pdf.multi_cell(0, 4.5, linea_limpia)

    ruta_pdf = os.path.join(TMP_PDFS, nombre_archivo_salida)
    pdf.output(ruta_pdf)
    return ruta_pdf


def exportar_salida_a_pdfs(ruta_salida_txt="salida.txt", nombre_sin_ext="archivo"):
    """
    Función modular que lee 'salida.txt', extrae los reportes y genera los PDFs con nombres personalizados.
    """
    if not os.path.exists(ruta_salida_txt):
        print(f"[ERROR]: No se encontró el archivo {ruta_salida_txt}")
        return []

    with open(ruta_salida_txt, "r", encoding="utf-8", errors="ignore") as f:
        texto_completo = f.read()

    lineas = texto_completo.splitlines()
    lineas_rep1 = []
    lineas_rep2 = []
    reporte_actual = None

    for linea in lineas:
        if "Reporte #1" in linea:
            reporte_actual = 1
            continue
        elif "Reporte #2" in linea:
            reporte_actual = 2
            continue

        if reporte_actual == 1:
            lineas_rep1.append(linea)
        elif reporte_actual == 2:
            lineas_rep2.append(linea)

    archivos_generados = []

    if lineas_rep1:
        pdf_1 = _generar_pdf_individual(
            titulo="REPORTE #1 - CANTIDADES Y RESUMEN",
            contenido_lineas=lineas_rep1,
            nombre_archivo_salida=f"pdf1_{nombre_sin_ext}.pdf",
        )
        archivos_generados.append(pdf_1)

    if lineas_rep2:
        pdf_2 = _generar_pdf_individual(
            titulo="REPORTE #2 - DESGLOSE DE TOKENS",
            contenido_lineas=lineas_rep2,
            nombre_archivo_salida=f"pdf2_{nombre_sin_ext}.pdf",
        )
        archivos_generados.append(pdf_2)

    print(f"✅ PDFs generados correctamente en: {TMP_PDFS}")
    return archivos_generados