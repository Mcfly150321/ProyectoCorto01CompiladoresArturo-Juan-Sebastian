# 🚀 Proyecto Corto 1: Analizador Léxico y Generador de Reportes

Repositorio para el proyecto de Compiladores enfocado en el análisis léxico, integración con base de datos NoSQL (MongoDB) y generación automatizada de reportes en PDF mediante una interfaz gráfica.

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalado en tu sistema:
* **Python** (versión 3.8 o superior recomendada)
* **Git**
* Entorno de consola compatible (**Bash** o **Fish**)

---

## ⚙️ Instalación y Configuración

Sigue estos pasos en tu terminal para configurar el proyecto y ponerlo en marcha:

### 1. Clonar el repositorio y ubicarse en la carpeta
git clone https://github.com/Mcfly150321/ProyectoCorto01CompiladoresArturo-Juan-Sebastian.git
cd TuCarpetaDelProyecto

### 2. Crear y activar el entorno virtual
Dependiendo de la shell que utilices, ejecuta el comando correspondiente:

* **Si usas Bash:**
python -m venv entorno
source entorno/bin/activate

* **Si usas Fish:**
python -m venv entorno
source entorno/bin/activate.fish

### 3. Instalar las dependencias
Una vez activado el entorno virtual, instala las librerías necesarias:
pip install -r requirements.txt

---

## ▶️ Ejecución del Programa

Para iniciar la aplicación con la interfaz gráfica, ejecuta el script principal:

python completo.py

### 🖥️ Uso de la Interfaz:
1. Haz clic en **"Seleccionar Archivo"**.
2. Elige un archivo con extensión `.groovy` o texto plano (`.txt`).
3. El sistema procesará el analizador léxico, subirá el resultado a **MongoDB** y generará los **PDFs** en la carpeta `output/`.

---

## 👥 Integrantes
* **Arturo**
* **Juan**
* **Sebastián**