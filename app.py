import streamlit as st
from core import db_manager
from views import upload_view
from views import dashboard_view
from views import reports_view
from views import settings_view # <- Importación nueva

st.set_page_config(page_title="Impacto Prácticas", page_icon="📊", layout="wide")

def main():
    db_manager.init_db()
    
    st.sidebar.title("Menú Institucional")
    st.sidebar.markdown("---")
    
    # Agregamos "Configuración" al menú
    menu = ["Dashboard Institucional", "Cargar Evaluaciones", "Generar Reportes PDF", "Configuración"]
    eleccion = st.sidebar.radio("Navegación:", menu)

    if eleccion == "Cargar Evaluaciones":
        upload_view.render()
    elif eleccion == "Dashboard Institucional":
        dashboard_view.render()
    elif eleccion == "Generar Reportes PDF":
        reports_view.render()
    elif eleccion == "Configuración":
        settings_view.render() # <- Llamamos a la vista

if __name__ == "__main__":
    main()