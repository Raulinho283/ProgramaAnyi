import streamlit as st
import tempfile
import os
from core import data_loader

def render():
    st.header("Carga de Evaluaciones de Prácticas")
    st.write("Sube el archivo Excel consolidado de las evaluaciones institucionales.")

    # Formularios de metadatos
    col1, col2 = st.columns(2)
    with col1:
        periodo = st.text_input("Periodo Académico", placeholder="Ej. 2026-I")
    with col2:
        carrera = st.text_input("Carrera", placeholder="Ej. Psicología")

    archivo_subido = st.file_uploader("Selecciona el archivo Excel", type=["xlsx", "xls"])

    if st.button("Procesar y Guardar", type="primary"):
        if not periodo or not carrera:
            st.warning("Por favor, ingresa el periodo académico y la carrera antes de continuar.")
            return
        
        if archivo_subido is None:
            st.warning("Por favor, sube un archivo Excel.")
            return
            
        with st.spinner("Procesando archivo, detectando indicadores y guardando en la base de datos..."):
            # Streamlit maneja los archivos en memoria; lo guardamos temporalmente para Pandas
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                tmp.write(archivo_subido.getvalue())
                tmp_path = tmp.name
            
            # Ejecutamos nuestro pipeline de extracción
            resultado = data_loader.guardar_evaluaciones_en_bd(tmp_path, periodo.strip(), carrera.strip())
            
            # Limpiamos el archivo temporal
            os.remove(tmp_path)

            if resultado["exito"]:
                st.success(resultado["mensaje"])
            else:
                st.error(resultado["mensaje"])