import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Importas tu módulo de PDF
from generador_pdfs import exportar_salida_a_pdfs


class AppInterfaz:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Archivos y Terminal Consola (Fish)")
        self.root.geometry("700x550")
        self.root.minsize(600, 400)
        self.root.configure(bg="#f0f2f5")
        self._crear_widgets()

    def _crear_widgets(self):
        frame_archivo = ttk.LabelFrame(
            self.root, text=" 📁 Archivo ", padding=10
        )
        frame_archivo.pack(side="top", fill="x", padx=15, pady=5)

        self.lbl_archivo = ttk.Label(
            frame_archivo,
            text="Ningún archivo seleccionado",
            font=("Segoe UI", 9, "italic"),
        )
        self.lbl_archivo.pack(side="left", fill="x", expand=True, padx=5)

        btn_seleccionar = ttk.Button(
            frame_archivo, text="Seleccionar Archivo", command=self.procesar_archivo
        )
        btn_seleccionar.pack(side="right", padx=5)

        frame_input = ttk.Frame(self.root, padding=10)
        frame_input.pack(side="bottom", fill="x", padx=15, pady=5)

        lbl_prompt = ttk.Label(
            frame_input, text="> Comando:", font=("Consolas", 10, "bold")
        )
        lbl_prompt.pack(side="left", padx=(0, 5))

        self.ent_comando = ttk.Entry(frame_input, font=("Consolas", 10))
        self.ent_comando.pack(side="left", fill="x", expand=True, padx=5)
        self.ent_comando.bind(
            "<Return>", lambda event: self.ejecutar_comando_manual()
        )

        btn_ejecutar = ttk.Button(
            frame_input, text="Ejecutar", command=self.ejecutar_comando_manual
        )
        btn_ejecutar.pack(side="right", padx=5)

        frame_consola = ttk.LabelFrame(
            self.root, text=" 🖥️ Consola / Resultados ", padding=10
        )
        frame_consola.pack(side="top", fill="both", expand=True, padx=15, pady=5)

        self.txt_salida = tk.Text(
            frame_consola,
            bg="#1e1e1e",
            fg="#00ff66",
            insertbackground="white",
            font=("Consolas", 10),
            wrap="word",
            height=12,
        )
        self.txt_salida.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            frame_consola, orient="vertical", command=self.txt_salida.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.txt_salida.config(yscrollcommand=scrollbar.set)

    def imprimir_en_consola(self, texto):
        self.txt_salida.insert(tk.END, texto + "\n")
        self.txt_salida.see(tk.END)

    def ejecutar_comando_sistema(self, comando):
        try:
            ruta_fish = "/usr/bin/fish" if os.path.exists("/usr/bin/fish") else "fish"

            resultado = subprocess.run(
                comando,
                shell=True,
                executable=ruta_fish,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
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
            filetypes=[
                ("Todos los archivos", "*.*"),
                ("Groovy", "*.groovy"),
                ("Texto plano", "*.txt"),
            ],
        )

        if not ruta_archivo:
            return

        nombre_archivo_con_ext = os.path.basename(ruta_archivo)
        nombre_sin_ext, _ = os.path.splitext(nombre_archivo_con_ext)
        
        self.lbl_archivo.config(text=f"Seleccionado: {nombre_archivo_con_ext}")

        self.imprimir_en_consola(f"\n--- Procesando archivo: {nombre_archivo_con_ext} ---")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Creamos la carpeta output si no existe
        dir_output = os.path.join(base_dir, "output")
        os.makedirs(dir_output, exist_ok=True)

        # Nombres personalizados solicitados
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

        self.imprimir_en_consola("Generando reportes PDF...")
        
        # Llamada adaptada pasando también el nombre base para que los PDFs salgan bien nombrados
        exportar_salida_a_pdfs(ruta_salida_absoluta, nombre_sin_ext)
        self.imprimir_en_consola("¡PDFs creados con éxito!")

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