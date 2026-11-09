import streamlit as st
import plotly.express as px
from core import stats_engine

def render():
    st.header("Dashboard Institucional de Prácticas")
    st.markdown("Análisis estadístico del impacto de las prácticas profesionales.")
    
    # 1. Obtener filtros disponibles
    periodos, carreras = stats_engine.obtener_filtros()
    
    if not periodos or not carreras:
        st.info("No hay datos en la base de datos. Por favor, ve a la sección de 'Cargar Evaluaciones' y sube un archivo.")
        return
        
    # 2. Renderizar selectores en la interfaz
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        periodo_sel = st.selectbox("Seleccione el Periodo Académico", periodos)
    with col_filtro2:
        carrera_sel = st.selectbox("Seleccione la Carrera", carreras)
        
    st.markdown("---")
    
    # 3. Traer los datos según el filtro
    df = stats_engine.obtener_datos_dashboard(periodo_sel, carrera_sel)
    
    if df.empty:
        st.warning(f"No se encontraron evaluaciones para la carrera de {carrera_sel} en el periodo {periodo_sel}.")
        return
        
    # 4. Cálculo de KPIs (Tarjetas principales)
    # Extraemos los datos únicos por evaluación para no sumar doble a los estudiantes
    df_unicos = df[['evaluacion_id', 'numero_estudiantes']].drop_duplicates()
    total_estudiantes = int(df_unicos['numero_estudiantes'].sum())
    total_evaluaciones = len(df_unicos)
    
    # Promedio global general de la carrera
    df_global = df[df['indicador'] == 'Evaluación Global']
    promedio_global = df_global['puntaje'].mean() if not df_global.empty else 0.0
    
    # Mostrar tarjetas
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Evaluaciones Procesadas", total_evaluaciones)
    col_kpi2.metric("Estudiantes Impactados", total_estudiantes)
    col_kpi3.metric("Promedio Global", f"{promedio_global:.2f} / 5.0")
    
    # 5. Gráfico de Barras Comparativo (Similar al del HTML original)
    st.subheader("Comparativo por Indicadores Institucionales")
    
    # Excluimos la evaluación global del gráfico para no distorsionar los 5 pilares
    df_grafico = df[df['indicador'] != 'Evaluación Global']
    
    # Promediamos los puntajes por indicador agrupando por docente/modalidad
    # Usaremos el nombre del docente como diferenciador (Karina, Claudia, etc.)
    df_agrupado = df_grafico.groupby(['indicador', 'docente'])['puntaje'].mean().reset_index()
    
    fig = px.bar(
        df_agrupado, 
        x='indicador', 
        y='puntaje', 
        color='docente', 
        barmode='group',
        labels={'puntaje': 'Calificación Promedio', 'indicador': 'Indicador Institucional', 'docente': 'Evaluador'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Forzar el eje Y para que siempre se vea de 0 a 5 (escala de calificación)
    fig.update_yaxes(range=[0, 5])
    st.plotly_chart(fig, use_container_width=True)
    
    # 6. Tabla de Detalles (Pivot Table)
    st.subheader("Desglose Cuantitativo por Escenario")
    # Convertimos los indicadores en columnas, y dejamos los escenarios/docentes en las filas
    df_tabla = df.pivot_table(
        index=['modalidad', 'escenario', 'docente'], 
        columns='indicador', 
        values='puntaje'
    ).reset_index()
    
    st.dataframe(df_tabla, use_container_width=True, hide_index=True)