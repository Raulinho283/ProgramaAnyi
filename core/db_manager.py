import sqlite3
import os

# Definimos la ruta de la base de datos en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database.sqlite')

def get_connection():
    """Establece y retorna la conexión a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    # Habilitamos el soporte para llaves foráneas en SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Inicializa la base de datos creando las tablas necesarias si no existen."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Tabla de Periodos Académicos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS periodos_academicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)
    
    # 2. Tabla de Carreras
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carreras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)
    
    # 3. Tabla Principal: Evaluaciones de Práctica (Cabecera)
    # Incluye un identificador único (hash_hoja) para evitar procesar la misma pestaña dos veces.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluaciones_practica (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        periodo_id INTEGER NOT NULL,
        carrera_id INTEGER NOT NULL,
        modalidad TEXT NOT NULL,
        escenario TEXT NOT NULL,
        docente TEXT NOT NULL,
        numero_estudiantes INTEGER,
        hash_hoja TEXT UNIQUE NOT NULL, 
        fecha_procesamiento DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (periodo_id) REFERENCES periodos_academicos(id),
        FOREIGN KEY (carrera_id) REFERENCES carreras(id)
    )
    """)
    
    # 4. Tabla: Resultados Cuantitativos (Los 5 indicadores + Evaluación Global)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados_cuantitativos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evaluacion_id INTEGER NOT NULL,
        indicador TEXT NOT NULL,
        puntaje REAL NOT NULL,
        FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones_practica(id) ON DELETE CASCADE
    )
    """)
    
    # 5. Tabla: Resultados Cualitativos (Fortalezas, Aspectos a mejorar, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados_cualitativos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evaluacion_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        texto TEXT NOT NULL,
        FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones_practica(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"Base de datos inicializada correctamente en: {DB_PATH}")

if __name__ == "__main__":
    # Al ejecutar este script directamente, se crean las tablas.
    init_db()