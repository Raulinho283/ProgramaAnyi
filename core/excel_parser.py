import pandas as pd
import hashlib
import warnings

# Ignoramos advertencias de estilos de openpyxl
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def generar_hash_hoja(df):
    """Genera un identificador único (MD5) basado en el contenido para evitar duplicados."""
    contenido = df.to_json()
    return hashlib.md5(contenido.encode('utf-8')).hexdigest()

def limpiar_texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()

def obtener_siguiente_valor(row, j_actual, limite_busqueda=10):
    """
    Busca el siguiente valor no nulo en la misma fila.
    Esto resuelve el problema de las celdas combinadas o vacías en Excel.
    """
    for offset in range(1, limite_busqueda):
        if j_actual + offset < len(row):
            val = row.iloc[j_actual + offset]
            # Si el valor no es nulo y no está vacío, lo retornamos
            if pd.notna(val) and str(val).strip() != "":
                return val
    return ""

def extraer_datos_hoja(df):
    datos = {
        "valida": False,
        "metadatos": {"docente": "", "modalidad": "", "escenario": "", "numero_estudiantes": 0},
        "cuantitativos": {},
        "cualitativos": {}
    }
    
    for i, row in df.iterrows():
        for j, col_val in enumerate(row):
            texto_celda = limpiar_texto(col_val).upper()
            
            if not texto_celda:
                continue
                
            # --- METADATOS (Aseguramos que solo capture la primera coincidencia) ---
            if "NOMBRE DOCENTE" in texto_celda and not datos["metadatos"]["docente"]:
                datos["metadatos"]["docente"] = limpiar_texto(obtener_siguiente_valor(row, j))
                
            elif ("PRÁCTICA" in texto_celda or "PRACTICA" in texto_celda) and not datos["metadatos"]["modalidad"]:
                # Evitamos falsos positivos con otros títulos de la hoja
                if "ESCENARIO" not in texto_celda and "EVALUACIÓN" not in texto_celda and "DESARROLLO" not in texto_celda and "ITEM" not in texto_celda:
                    datos["metadatos"]["modalidad"] = limpiar_texto(obtener_siguiente_valor(row, j))
                    
            elif "ESCENARIO" in texto_celda and not datos["metadatos"]["escenario"]:
                datos["metadatos"]["escenario"] = limpiar_texto(obtener_siguiente_valor(row, j))
                
            elif "ESTUDIANTES" in texto_celda and datos["metadatos"]["numero_estudiantes"] == 0:
                val = obtener_siguiente_valor(row, j)
                try:
                    datos["metadatos"]["numero_estudiantes"] = int(val)
                except (ValueError, TypeError):
                    pass
            
            # --- INDICADORES CUANTITATIVOS ---
            indicadores_claves = [
                ("I. CUMPLIMIENTO", "I. Cumplimiento del Desarrollo"),
                ("II. DESARROLLO", "II. Desarrollo de Competencias"),
                ("III. IMPACTO", "III. Impacto en el Entorno"),
                ("IV. ARTICULACIÓN", "IV. Articulación Institucional"),
                ("V. ALCANCE", "V. Alcance de las Prácticas"),
                ("GLOBAL DEL PROCESO", "Evaluación Global")
            ]
            
            for clave_busqueda, nombre_estandar in indicadores_claves:
                if clave_busqueda in texto_celda:
                    val = obtener_siguiente_valor(row, j)
                    try:
                        # Aseguramos que se guarde como número decimal
                        datos["cuantitativos"][nombre_estandar] = float(val)
                    except (ValueError, TypeError):
                        pass

            # --- RESPUESTAS CUALITATIVAS ---
            cualitativas_claves = [
                ("PRINCIPAL FORTALEZA", "Fortaleza"),
                ("PRINCIPAL ASPECTO", "Aspecto a Mejorar"),
                ("PRINCIPAL IMPACTO", "Impacto Observado"),
                ("RECOMENDACIÓN GENERAL", "Recomendación")
            ]
            
            for clave_busqueda, nombre_estandar in cualitativas_claves:
                if clave_busqueda in texto_celda:
                    val = obtener_siguiente_valor(row, j)
                    if isinstance(val, str) and len(val) > 5:
                        datos["cualitativos"][nombre_estandar] = limpiar_texto(val)

    # Validación final
    if datos["metadatos"]["docente"] and datos["metadatos"]["escenario"]:
        datos["valida"] = True
        
    return datos

def procesar_archivo_excel(ruta_archivo):
    resultados = []
    try:
        # El bloque 'with' garantiza que Pandas cierre el archivo al terminar de leer
        with pd.ExcelFile(ruta_archivo) as xls:
            for nombre_hoja in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)
                
                if df.empty:
                    continue
                    
                datos = extraer_datos_hoja(df)
                
                if datos["valida"]:
                    datos["nombre_hoja"] = nombre_hoja
                    datos["hash_hoja"] = generar_hash_hoja(df)
                    resultados.append(datos)
                    
        return {"exito": True, "datos": resultados, "error": None}
        
    except Exception as e:
        return {"exito": False, "datos": [], "error": str(e)}

# --- BLOQUE DE PRUEBA LOCAL ---
if __name__ == "__main__":
    import os
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    archivo_prueba = os.path.join(base_dir, "BORRADOR IMPACTO DE PRACTICAS 2026 canva.xlsx")
    
    if os.path.exists(archivo_prueba):
        print(f"Procesando archivo: {archivo_prueba}...\n")
        resultado = procesar_archivo_excel(archivo_prueba)
        
        if resultado["exito"]:
            evaluaciones = resultado["datos"]
            print(f"Se encontraron {len(evaluaciones)} evaluaciones válidas (se descartaron hojas vacías).\n")
            
            for eval_data in evaluaciones:
                print(f"--- Hoja: {eval_data['nombre_hoja']} ---")
                print(f"Docente: {eval_data['metadatos']['docente']}")
                print(f"Escenario: {eval_data['metadatos']['escenario']}")
                print(f"Indicadores leídos: {len(eval_data['cuantitativos'])}/6")
                print(f"Textos cualitativos leídos: {len(eval_data['cualitativos'])}/4")
                print("-" * 40)
        else:
            print(f"Error procesando el archivo: {resultado['error']}")