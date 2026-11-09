import streamlit as st
from core import stats_engine
from core import pdf_export

def render():
    st.header("Generación de Reportes Institucionales")
    st.markdown("Genera y descarga el informe en formato PDF")
    
    periodos, carreras = stats_engine.obtener_filtros()
    
    if not periodos or not carreras:
        st.info("No hay datos en la base de datos para generar reportes.")
        return
        
    col1, col2 = st.columns(2)
    with col1:
        periodo_sel = st.selectbox("Seleccione el Periodo a exportar", periodos)
    with col2:
        carrera_sel = st.selectbox("Seleccione la Carrera a exportar", carreras)
        
    st.markdown("---")
        
    if st.button("Construir Documento PDF", type="primary"):
        with st.spinner("Procesando datos y maquetando el documento..."):
            df_cuant = stats_engine.obtener_datos_dashboard(periodo_sel, carrera_sel)
            df_cual = stats_engine.obtener_datos_cualitativos(periodo_sel, carrera_sel)
            
            if df_cuant.empty:
                st.warning("No hay evaluaciones registradas para esta selección.")
                return
                
            # Generamos el PDF físicamente en una carpeta temporal
            ruta_pdf = pdf_export.generar_reporte_pdf(periodo_sel, carrera_sel, df_cuant, df_cual)
            
            # Leemos el PDF generado y creamos el botón de descarga
            with open(ruta_pdf, "rb") as archivo_pdf:
                st.success("Documento generado correctamente.")
                st.download_button(
                    label="⬇️ Descargar Reporte PDF",
                    data=archivo_pdf,
                    file_name=f"Reporte_Practicas_{carrera_sel}_{periodo_sel}.pdf",
                    mime="application/pdf"
                )