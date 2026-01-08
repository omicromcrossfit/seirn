import subprocess
import os
import sys

def run_streamlit():
    # Encuentra la ruta del ejecutable principal (que es el intérprete Python)
    python_exe_path = sys.executable

    # Define la ruta relativa del módulo __main__.py de streamlit
    # El ejecutable (sys.executable) actúa como la carpeta base del 'venv'
    
    # 1. Rutas relativas del ejecutable. PyInstaller lo pone en un nivel superior.
    # Esta es una ruta más robusta para Windows:
    streamlit_path_parts = ['Lib', 'site-packages', 'streamlit', '__main__.py']
    
    # Intenta construir la ruta al módulo de Streamlit
    base_dir = os.path.dirname(python_exe_path)
    
    # Busca el archivo __main__.py de Streamlit dentro del bundle
    # Nota: Usamos os.path.join para crear la ruta relativa dentro del bundle
    streamlit_module_path = os.path.join(
        base_dir, 'Lib', 'site-packages', 'streamlit', '__main__.py'
    )
    
    # Ruta del archivo principal de tu app
    script_path = os.path.join(os.path.dirname(__file__), 'app.py')

    # Ejecuta el intérprete de Python (el ejecutable) para correr el módulo de Streamlit
    # Comando final: [python.exe, C:\ruta\a\streamlit\__main__.py, run, C:\ruta\a\app.py]
    # Usamos base_dir para asegurar que subprocess puede encontrar los archivos dentro del bundle
    subprocess.run([python_exe_path, streamlit_module_path, 'run', script_path], cwd=base_dir)


if __name__ == '__main__':
    # Usamos un try/except general para que el error aparezca en consola
    try:
        run_streamlit()
    except Exception as e:
        # Esto imprimirá el error al final, muy útil para el debugging.
        # En ejecutable: Win+R, escribe cmd, arrastra el .exe a la ventana y dale Enter.
        print(f"Error al iniciar Streamlit: {e}")
        # Mantiene la ventana abierta para ver el mensaje de error
        input("Presiona Enter para salir...")