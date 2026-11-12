import streamlit as st
import json
import os

def cargar_configuracion():
    ruta = os.path.join(os.getcwd(), 'config.json')
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"indicadores_cuantitativos": [], "indicadores_cualitativos": []}

def guardar_configuracion(config):
    ruta = os.path.join(os.getcwd(), 'config.json')
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def render():
    st.header("⚙️ Configuración del Extractor")
    st.markdown("Administra las palabras clave que el sistema busca en los archivos Excel. **Solo modifica esto si el formato institucional cambia.**")
    
    config = cargar_configuracion()
    
    st.subheader("Indicadores Cuantitativos (Calificación 1 a 5)")
    st.info("La 'Palabra Clave' es lo que el sistema busca en el Excel. El 'Nombre' es cómo se mostrará en los gráficos y reportes.")
    
    # Mostrar indicadores actuales
    for i, item in enumerate(config["indicadores_cuantitativos"]):
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            item["clave"] = st.text_input(f"Palabra Clave {i+1}", value=item["clave"], key=f"cuant_clave_{i}")
        with col2:
            item["nombre"] = st.text_input(f"Nombre del Indicador {i+1}", value=item["nombre"], key=f"cuant_nom_{i}")
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Eliminar", key=f"cuant_del_{i}"):
                config["indicadores_cuantitativos"].pop(i)
                guardar_configuracion(config)
                st.rerun()

    if st.button("➕ Agregar Nuevo Indicador Cuantitativo"):
        config["indicadores_cuantitativos"].append({"clave": "NUEVA CLAVE", "nombre": "Nuevo Indicador"})
        guardar_configuracion(config)
        st.rerun()
        
    st.markdown("---")
    
    if st.button("💾 Guardar Cambios", type="primary"):
        guardar_configuracion(config)
        st.success("Configuración actualizada correctamente. Los próximos Excel se leerán con estas reglas.")