#  Sistema de Análisis de Impacto de Prácticas Profesionales

Aplicación web desarrollada en Python para automatizar la evaluación, consolidación y análisis del impacto de las prácticas profesionales de los estudiantes en diferentes programas académicos e instituciones.

##  Características Principales

1. **Extracción Inteligente:** Lector dinámico de Excel que escanea formularios institucionales, evadiendo celdas vacías y formatos irregulares sin depender de filas fijas.
2. **Protección de Datos:** Base de datos SQLite integrada que previene la duplicación de evaluaciones mediante un sistema de validación por hashes (MD5).
3. **Dashboard Interactivo:** Panel analítico con indicadores clave (KPIs), tablas dinámicas y gráficos comparativos desarrollados con Plotly.
4. **Generación de Reportes:** Exportación automatizada a PDF con un diseño profesional institucional utilizando ReportLab, consolidando resultados cuantitativos y apreciaciones cualitativas.

##  Estructura del Proyecto

```text
impacto_practicas_app/
├── app.py                  # Archivo principal de ejecución (Streamlit App)
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Documentación del proyecto
├── database.sqlite         # Base de datos local (Se genera automáticamente)
├── /core                   # Lógica de negocio y procesamiento
│   ├── db_manager.py       # Conexión y creación de tablas SQLite
│   ├── excel_parser.py     # Algoritmo de lectura y limpieza de Excel
│   ├── stats_engine.py     # Consultas SQL cruzadas y preparación de DataFrames
│   └── pdf_export.py       # Maquetación y generación del informe en PDF
└── /views                  # Vistas de la interfaz de usuario (Frontend)
    ├── upload_view.py      # Interfaz de carga de archivos
    ├── dashboard_view.py   # Renderizado de métricas y gráficos
    └── reports_view.py     # Interfaz de generación y descarga de PDFs
```

##  Requisitos e Instalación

Asegúrate de tener instalado **Python 3.8** o superior en tu sistema.

**1. Clonar o descargar el proyecto:**
Ubícate en la carpeta raíz del proyecto (`impacto_practicas_app/`).

**2. Instalar las dependencias:**
Abre tu terminal y ejecuta el siguiente comando para instalar todas las librerías necesarias:
```bash
python -m pip install -r requirements.txt
```

*(Las librerías principales utilizadas son: Streamlit, Pandas, OpenPyXL, Plotly y ReportLab).*

##  Instrucciones de Uso

Para encender el servidor de la aplicación web, ejecuta el siguiente comando en la raíz del proyecto:
```bash
python -m streamlit run app.py
```
Esto abrirá automáticamente la aplicación en tu navegador web predeterminado.

### Flujo de Trabajo
1. **Cargar Evaluaciones:** Dirígete a la pestaña "Cargar Evaluaciones" en el menú lateral. Ingresa el Periodo Académico (ej. 2026-I), la Carrera (ej. Psicología) y sube el archivo Excel con los formatos llenos. El sistema procesará los datos e informará si hubo omisiones por duplicidad.
2. **Consultar Dashboard:** Ve a la sección "Dashboard Institucional". Utiliza los filtros superiores para seleccionar el periodo y carrera deseados. Explora el gráfico interactivo y la tabla de desglose.
3. **Generar PDF:** En la sección "Generar Reportes PDF", selecciona el periodo y la carrera, y haz clic en "Construir Documento PDF". Descarga el archivo final listo para impresión o envío institucional.

## 🏗️ Decisiones Técnicas y Arquitectura

* **Arquitectura Modular:** Se separó la vista (Streamlit) de la lógica de extracción y la capa de datos. Esto permite que el sistema escale o se adapte fácilmente si la institución cambia de formatos visuales en el futuro.
* **Procesamiento de Excel con Pandas:** En lugar de buscar celdas exactas (`B8`, `C12`), se desarrolló un algoritmo de búsqueda por palabras clave institucionales ("Nombre Docente", "I. Cumplimiento"), lo que garantiza flexibilidad frente a modificaciones en las plantillas de Excel por parte de distintas carreras.
* **Motor SQLite embebido:** Permite conservar la trazabilidad y la historia de múltiples semestres sin requerir infraestructura externa de servidores, ideal para un control interno seguro.