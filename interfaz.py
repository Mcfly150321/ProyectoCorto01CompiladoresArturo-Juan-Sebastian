import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class AppInterfaz:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Archivos y Terminal Consola")
        self.root.geometry("700x550")
        self.root.minsize(600, 400)

        # Configuración de estilo básico
        self.root.configure(bg="#f0f2f5")

        # UI Components
        self._crear_widgets()

    def _crear_widgets(self):
        # --- SECCIÓN 1: Seleccionador de Archivo ---
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

        # --- SECCIÓN 2: Entrada de Comandos Manuales (Empaquetado abajo primero) ---
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

        # --- SECCIÓN 3: Salida de Resultados / Terminal (Toma el espacio restante) ---
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
            height=12,  # Define una altura inicial para evitar que ocupe todo
        )
        self.txt_salida.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            frame_consola, orient="vertical", command=self.txt_salida.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.txt_salida.config(yscrollcommand=scrollbar.set)

    def imprimir_en_consola(self, texto):
        """Agrega texto al área de la consola integrada y desplaza hacia abajo."""
        self.txt_salida.insert(tk.END, texto + "\n")
        self.txt_salida.see(tk.END)

    def ejecutar_comando_sistema(self, comando):
        """Ejecuta un comando en la consola del sistema operativo y captura la salida."""
        try:
            # shell=True permite interpretar comandos built-in de la terminal (echo, dir, etc.)
            resultado = subprocess.run(
                comando,
                shell=True,
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
        """Abre el diálogo de archivos y ejecuta el comando solicitado con la información."""
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo",
            filetypes=[("Todos los archivos", "*.*"), ("Texto plano", "*.txt")],
        )

        if not ruta_archivo:
            return

        nombre_archivo = os.path.basename(ruta_archivo)
        self.lbl_archivo.config(text=f"Seleccionado: {nombre_archivo}")

        # Intentar leer el contenido del archivo
        try:
            with open(ruta_archivo, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.read().strip()
        except Exception as e:
            contenido = f"<No se pudo leer el contenido: {e}>"

        self.imprimir_en_consola(f"\n--- Procesando: {nombre_archivo} ---")

        # Construcción del comando echo (compatible con Windows cmd y Bash)
        # Nota: En Windows, pasar comillas dentro de un comando puede ser delicado,
        # así que formateamos las cadenas de forma limpia.
        comando_echo = f'echo Hola Mundo | Nombre del archivo: {nombre_archivo} | Contenido: {contenido}'

        self.imprimir_en_consola(f"$ {comando_echo}")
        self.ejecutar_comando_sistema(comando_echo)

    def ejecutar_comando_manual(self):
        """Toma el comando ingresado por el usuario en el Entry y lo ejecuta."""
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