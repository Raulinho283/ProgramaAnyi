import pandas as pd
from core import db_manager

def obtener_filtros():
    """Obtiene las listas de periodos y carreras disponibles en la base de datos."""
    conn = db_manager.get_connection()
    periodos = pd.read_sql("SELECT nombre FROM periodos_academicos", conn)['nombre'].tolist()
    carreras = pd.read_sql("SELECT nombre FROM carreras", conn)['nombre'].tolist()
    conn.close()
    return periodos, carreras

def obtener_datos_dashboard(periodo, carrera):
    """
    Realiza una consulta cruzada (JOIN) para traer todos los datos cuantitativos
    asociados a un periodo y carrera específicos.
    """
    conn = db_manager.get_connection()
    query = """
    SELECT 
        ep.id as evaluacion_id,
        ep.modalidad, 
        ep.escenario, 
        ep.docente, 
        ep.numero_estudiantes,
        rc.indicador,
        rc.puntaje
    FROM evaluaciones_practica ep
    JOIN periodos_academicos pa ON ep.periodo_id = pa.id
    JOIN carreras c ON ep.carrera_id = c.id
    JOIN resultados_cuantitativos rc ON ep.id = rc.evaluacion_id
    WHERE pa.nombre = ? AND c.nombre = ?
    """
    df = pd.read_sql(query, conn, params=(periodo, carrera))
    conn.close()
    return df

def obtener_datos_cualitativos(periodo, carrera):
    """
    Realiza una consulta cruzada para traer todos los textos cualitativos (fortalezas, impactos).
    """
    conn = db_manager.get_connection()
    query = """
    SELECT 
        ep.modalidad, ep.docente, ep.escenario, ep.numero_estudiantes,
        rc.tipo, rc.texto
    FROM evaluaciones_practica ep
    JOIN periodos_academicos pa ON ep.periodo_id = pa.id
    JOIN carreras c ON ep.carrera_id = c.id
    JOIN resultados_cualitativos rc ON ep.id = rc.evaluacion_id
    WHERE pa.nombre = ? AND c.nombre = ?
    """
    df = pd.read_sql(query, conn, params=(periodo, carrera))
    conn.close()
    return df