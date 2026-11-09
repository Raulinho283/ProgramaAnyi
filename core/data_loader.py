import sqlite3
import os
from core import db_manager
from core import excel_parser

def guardar_evaluaciones_en_bd(ruta_archivo, nombre_periodo, nombre_carrera):
    """
    Procesa un archivo Excel y guarda sus datos en SQLite.
    Controla la creación automática de periodos y carreras, y evita duplicados.
    """
    # 1. Extraer los datos usando nuestro módulo
    resultado = excel_parser.procesar_archivo_excel(ruta_archivo)
    
    if not resultado["exito"]:
        return {"exito": False, "mensaje": f"Error al procesar archivo: {resultado['error']}"}
    
    evaluaciones = resultado["datos"]
    if not evaluaciones:
        return {"exito": False, "mensaje": "No se encontraron evaluaciones válidas en el archivo."}
        
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    try:
        # 2. Obtener o registrar el Periodo Académico
        cursor.execute("SELECT id FROM periodos_academicos WHERE nombre = ?", (nombre_periodo,))
        row = cursor.fetchone()
        if row:
            periodo_id = row[0]
        else:
            cursor.execute("INSERT INTO periodos_academicos (nombre) VALUES (?)", (nombre_periodo,))
            periodo_id = cursor.lastrowid
            
        # 3. Obtener o registrar la Carrera
        cursor.execute("SELECT id FROM carreras WHERE nombre = ?", (nombre_carrera,))
        row = cursor.fetchone()
        if row:
            carrera_id = row[0]
        else:
            cursor.execute("INSERT INTO carreras (nombre) VALUES (?)", (nombre_carrera,))
            carrera_id = cursor.lastrowid
            
        guardadas = 0
        duplicadas = 0
        
        # 4. Iterar e insertar cada evaluación encontrada
        for eval_data in evaluaciones:
            hash_hoja = eval_data["hash_hoja"]
            meta = eval_data["metadatos"]
            
            # Validar si esta hoja exacta ya fue subida previamente
            cursor.execute("SELECT id FROM evaluaciones_practica WHERE hash_hoja = ?", (hash_hoja,))
            if cursor.fetchone():
                duplicadas += 1
                continue # Saltamos esta hoja porque ya existe
                
            # Insertar Cabecera de la Evaluación
            cursor.execute("""
                INSERT INTO evaluaciones_practica 
                (periodo_id, carrera_id, modalidad, escenario, docente, numero_estudiantes, hash_hoja)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (periodo_id, carrera_id, meta["modalidad"], meta["escenario"], 
                  meta["docente"], meta["numero_estudiantes"], hash_hoja))
            
            evaluacion_id = cursor.lastrowid
            
            # Insertar Resultados Cuantitativos (los 5 indicadores + global)
            for indicador, puntaje in eval_data["cuantitativos"].items():
                cursor.execute("""
                    INSERT INTO resultados_cuantitativos (evaluacion_id, indicador, puntaje)
                    VALUES (?, ?, ?)
                """, (evaluacion_id, indicador, puntaje))
                
            # Insertar Resultados Cualitativos (Textos)
            for tipo, texto in eval_data["cualitativos"].items():
                cursor.execute("""
                    INSERT INTO resultados_cualitativos (evaluacion_id, tipo, texto)
                    VALUES (?, ?, ?)
                """, (evaluacion_id, tipo, texto))
                
            guardadas += 1
            
        # 5. Confirmar transacciones
        conn.commit()
        return {
            "exito": True, 
            "mensaje": f"Proceso completado con éxito. Evaluaciones guardadas: {guardadas} | Duplicadas omitidas: {duplicadas}."
        }
        
    except sqlite3.Error as e:
        conn.rollback() # Revertimos si hay un error crítico
        return {"exito": False, "mensaje": f"Error de base de datos: {e}"}
    finally:
        conn.close()

# --- BLOQUE DE PRUEBA LOCAL ---
if __name__ == "__main__":
    # Prueba la inserción apuntando al archivo borrador
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    archivo_prueba = os.path.join(base_dir, "BORRADOR IMPACTO DE PRACTICAS 2026 canva.xlsx")
    
    if os.path.exists(archivo_prueba):
        print("Iniciando carga de datos...")
        # Simulamos que un usuario subió el formato de Psicología para el periodo 2026-I
        respuesta = guardar_evaluaciones_en_bd(archivo_prueba, "2026-I", "Psicología")
        print(respuesta["mensaje"])
        
        # Si lo corres por segunda vez, debería decir "Duplicadas omitidas: 4"
        print("\nPrueba de re-subida (debería bloquear duplicados):")
        respuesta_dup = guardar_evaluaciones_en_bd(archivo_prueba, "2026-I", "Psicología")
        print(respuesta_dup["mensaje"])
    else:
        print("No se encontró el archivo de prueba.")