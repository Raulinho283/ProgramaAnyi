import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generar_reporte_pdf(periodo, carrera, df_cuant, df_cual):
    # Creamos un archivo temporal para el PDF
    temp_dir = tempfile.gettempdir()
    ruta_pdf = os.path.join(temp_dir, f"Impacto_Practicas_{carrera}_{periodo}.pdf")
    
    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    estilos = getSampleStyleSheet()
    historia = []
    
    # --- ESTILOS PERSONALIZADOS ---
    estilo_titulo = ParagraphStyle(
        'Titulo', parent=estilos['Heading1'], alignment=1, textColor=colors.HexColor("#1a2a6c"), fontSize=14
    )
    estilo_subtitulo = ParagraphStyle(
        'Subtitulo', parent=estilos['Normal'], alignment=1, textColor=colors.HexColor("#4a90e2")
    )
    estilo_seccion = ParagraphStyle(
        'Seccion', parent=estilos['Heading2'], textColor=colors.HexColor("#1a2a6c"), spaceBefore=20, spaceAfter=10
    )
    estilo_texto = ParagraphStyle('Texto', parent=estilos['Normal'], alignment=4, spaceAfter=8) # alignment 4 es justificado
    
    # --- CABECERA ---
    historia.append(Paragraph("EVALUACIÓN DEL IMPACTO DE LAS PRÁCTICAS PROFESIONALES", estilo_titulo))
    historia.append(Paragraph(f"PROGRAMA DE {carrera.upper()} | PERIODO {periodo}", estilo_subtitulo))
    historia.append(Spacer(1, 20))
    
    # --- TABLA CUANTITATIVA ---
    historia.append(Paragraph("I. Análisis Cuantitativo Comparativo", estilo_seccion))
    
    # Preparamos la tabla dinámica (pivot) para el PDF
    pivot_df = df_cuant.pivot_table(index='indicador', columns='docente', values='puntaje').reset_index()
    
    # Convertimos el DataFrame a lista de listas para ReportLab
    datos_tabla = [pivot_df.columns.tolist()] # Encabezados
    for row in pivot_df.values.tolist():
        # Formatear números a 2 decimales
        fila_formateada = [f"{val:.2f}" if isinstance(val, float) else val for val in row]
        datos_tabla.append(fila_formateada)
        
    tabla = Table(datos_tabla, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1a2a6c")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#f0f4f8")), # Columna de indicadores sombreada
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
    ]))
    historia.append(tabla)
    
    # --- ANÁLISIS CUALITATIVO ---
    historia.append(Paragraph("II. Análisis Cualitativo por Escenario", estilo_seccion))
    
    # Agrupamos por docente para iterar sus textos
    docentes = df_cual['docente'].unique()
    for docente in docentes:
        df_docente = df_cual[df_cual['docente'] == docente]
        escenario = df_docente['escenario'].iloc[0]
        modalidad = df_docente['modalidad'].iloc[0]
        estudiantes = df_docente['numero_estudiantes'].iloc[0]
        
        # Título del escenario
        historia.append(Paragraph(f"<b>{modalidad} - Docente: {docente}</b>", estilos['Heading3']))
        historia.append(Paragraph(f"<b>Escenario:</b> {escenario} | <b>N° Estudiantes:</b> {estudiantes}", estilos['Normal']))
        historia.append(Spacer(1, 10))
        
        # Textos de evaluación
        for _, fila in df_docente.iterrows():
            texto_html = f"<b>{fila['tipo']}:</b> {fila['texto']}"
            historia.append(Paragraph(texto_html, estilo_texto))
            
        historia.append(Spacer(1, 15))
        
    # Construcción final del PDF
    doc.build(historia)
    return ruta_pdf