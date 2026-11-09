import streamlit as st
from core import db_manager  # <- Importación necesaria
from views import upload_view
from views import dashboard_view
from views import reports_view

st.set_page_config(page_title="Impacto Prácticas", page_icon="🗣️", layout="wide")

def main():
    db_manager.init_db()  # <- Obliga a crear las tablas si el archivo está vacío
    
    st.sidebar.title("Menú Institucional")
    st.sidebar.markdown("---")
    
    menu = ["Dashboard Institucional", "Cargar Evaluaciones", "Generar Reportes PDF"]
    eleccion = st.sidebar.radio("Navegación:", menu)

    if eleccion == "Cargar Evaluaciones":
        upload_view.render()
    elif eleccion == "Dashboard Institucional":
        dashboard_view.render()
    elif eleccion == "Generar Reportes PDF":
        reports_view.render()

if __name__ == "__main__":
    main()