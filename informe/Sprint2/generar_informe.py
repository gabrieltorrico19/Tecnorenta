import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from datetime import datetime, date
import json

SNAPSHOTS_DIR = os.path.join(os.path.dirname(__file__), "capturas")

def set_cell_shading(cell, color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def add_page_number(doc):
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
        run._r.append(fldChar1)
        run2 = p.add_run()
        instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
        run2._r.append(instrText)
        run3 = p.add_run()
        fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
        run3._r.append(fldChar2)

def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_paragraph_apa(doc, text, bold=False, italic=False, size=12, alignment=None, space_after=Pt(12)):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if alignment:
        p.alignment = alignment
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = 2.0
    return p

def add_paragraph_mixed(doc, parts, size=12, alignment=None, space_after=Pt(12)):
    p = doc.add_paragraph()
    for text, bold, italic in parts:
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
    if alignment:
        p.alignment = alignment
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = 2.0
    return p

def add_image_centered(doc, image_path, width=Inches(5.5)):
    if os.path.exists(image_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(image_path, width=width)
        return True
    return False

def create_informe():
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    style.paragraph_format.line_spacing = 2.0

    # ======================== PORTADA ========================
    for _ in range(6):
        doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('SIGTAR — Sistema de Gestión y Trazabilidad de Activos Rentados')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.bold = True
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Tecnorenta')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    
    doc.add_paragraph()
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Informe Técnico — Sprint 2')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Desarrollo de módulos CRUD, Dashboard Gerencial\n y Consultas SQL Complejas')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.italic = True
    
    for _ in range(4):
        doc.add_paragraph()
    
    info_lines = [
        'Asignatura: Programación de Sistemas II',
        'Docente: Ing. Juan Pérez López',
        '',
        'Estudiantes:',
        '• Estudiante 1 — Carné 001',
        '• Estudiante 2 — Carné 002',
        '• Estudiante 3 — Carné 003',
        '• Estudiante 4 — Carné 004',
        '',
        f'Ciudad, {datetime.now().strftime("%d de %B de %Y")}',
    ]
    for line in info_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(line)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        if not line:
            p.paragraph_format.space_after = Pt(6)
    
    doc.add_page_break()

    # ======================== RESUMEN EJECUTIVO ========================
    add_heading_styled(doc, 'Resumen Ejecutivo', level=1)
    
    add_paragraph_apa(doc, 
        'El presente informe documenta el desarrollo del Sprint 2 del sistema SIGTAR (Sistema de Gestión y '
        'Trazabilidad de Activos Rentados), correspondiente a la plataforma Tecnorenta. Durante este sprint '
        'se implementaron doce módulos CRUD completos para la gestión de usuarios, roles, clientes, activos, '
        'categorías, contratos, pagos, asignaciones, reportes de incidencias, mantenimientos, historial de '
        'ubicación y checklist de estado. Adicionalmente, se desarrolló un dashboard gerencial con indicadores '
        'clave de rendimiento (KPI) que incluye gráficos de barras y pastel generados con Recharts, consultas '
        'SQL complejas con JOINs, agrupaciones y subconsultas, y documentación automatizada de la API mediante '
        'Swagger UI. El sistema backend se construyó con FastAPI y SQLAlchemy 2.0 sobre MySQL, mientras que el '
        'frontend se desarrolló con React 19, TypeScript y Vite. Los resultados muestran un sistema funcional '
        'con capacidad de registrar, consultar, modificar y eliminar datos transaccionales, generar reportes '
        'visuales y consultar el estado actualizado de la operación.'
    )
    
    p = doc.add_paragraph()
    run = p.add_run('Palabras clave: ')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.italic = True
    run = p.add_run('SIGTAR, FastAPI, React, CRUD, Dashboard, SQL, MySQL, Activos Rentados')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    
    doc.add_page_break()

    # ======================== INTRODUCCIÓN ========================
    add_heading_styled(doc, 'Introducción', level=1)
    
    add_paragraph_apa(doc,
        'La gestión eficiente de activos rentados representa un desafío operativo significativo para las '
        'empresas del sector. La carencia de herramientas digitales integradas genera problemas de trazabilidad, '
        'pérdida de información y dificultades en la toma de decisiones basada en datos. En este contexto, '
        'el sistema SIGTAR surge como una solución integral para la administración del ciclo de vida completo '
        'de los activos de alquiler.'
    )
    
    add_paragraph_apa(doc,
        'El Sprint 2 del proyecto se enfocó en la implementación de los módulos funcionales del sistema, '
        'abarcando desde la gestión de usuarios y roles hasta el seguimiento detallado de activos mediante '
        'checklist de estado y ubicación geográfica. Se adoptó una arquitectura de tres capas (router-servicio-repositorio) '
        'en el backend, garantizando la separación de responsabilidades y la mantenibilidad del código.'
    )
    
    add_paragraph_apa(doc,
        'Este informe detalla las tecnologías empleadas, la estructura de la base de datos, los doce módulos '
        'CRUD implementados, el dashboard gerencial con sus consultas SQL complejas, la documentación de la '
        'API, los resultados obtenidos y las conclusiones del sprint. Se sigue el formato de la séptima edición '
        'de APA para la presentación del documento.'
    )

    doc.add_page_break()

    # ======================== MARCO TEÓRICO ========================
    add_heading_styled(doc, 'Marco Teórico', level=1)
    
    add_heading_styled(doc, 'Arquitectura de Software en Tres Capas', level=2)
    add_paragraph_apa(doc,
        'La arquitectura de tres capas es un patrón de diseño que separa la lógica de presentación, la lógica '
        'de negocio y el acceso a datos en componentes independientes. Según Fowler (2002), esta separación '
        'permite una mayor mantenibilidad, escalabilidad y facilidad de prueba del software. En el contexto de '
        'aplicaciones web modernas, esta arquitectura se traduce en una división clara entre el frontend (capa '
        'de presentación), los servicios (lógica de negocio) y los repositorios (acceso a datos).'
    )
    
    add_heading_styled(doc, 'FastAPI y SQLAlchemy para APIs REST', level=2)
    add_paragraph_apa(doc,
        'FastAPI es un framework moderno para la construcción de APIs con Python que ofrece alto rendimiento, '
        'validación automática mediante Pydantic y generación automática de documentación OpenAPI (Ramírez, 2018). '
        'SQLAlchemy 2.0, por su parte, es un ORM (Object Relational Mapper) maduro que permite la interacción '
        'con bases de datos relacionales mediante objetos Python, soportando consultas complejas, relaciones y '
        'migraciones (Bayer, 2012). La combinación de ambas herramientas facilita el desarrollo ágil de APIs '
        'robustas con tipos estáticos y documentación auto-gestionada.'
    )
    
    add_heading_styled(doc, 'React y Recharts para Interfaces de Usuario', level=2)
    add_paragraph_apa(doc,
        'React es una biblioteca de JavaScript para la construcción de interfaces de usuario basada en '
        'componentes reutilizables y un enfoque declarativo (Meta Platforms, 2013). Su modelo de componentes '
        'permite crear interfaces modulares y mantenibles. Recharts, construido sobre React y D3, proporciona '
        'una forma declarativa de crear gráficos interactivos para la visualización de datos en aplicaciones '
        'web (Recharts, 2021).'
    )
    
    add_heading_styled(doc, 'Metodología Scrum', level=2)
    add_paragraph_apa(doc,
        'Scrum es un marco de trabajo ágil para la gestión de proyectos complejos que se organiza en sprints '
        'de duración fija, generalmente de dos a cuatro semanas (Schwaber & Sutherland, 2020). Los roles '
        'principales incluyen el Product Owner, el Scrum Master y el equipo de desarrollo. Las ceremonias '
        'clave son la planificación del sprint, el daily stand-up, la revisión del sprint y la retrospectiva. '
        'El burndown chart es una herramienta visual que muestra el trabajo pendiente a lo largo del tiempo, '
        'permitiendo al equipo monitorear el progreso.'
    )

    doc.add_page_break()

    # ======================== DESARROLLO ========================
    add_heading_styled(doc, 'Desarrollo', level=1)
    
    add_heading_styled(doc, 'Stack Tecnológico', level=2)
    
    table = doc.add_table(rows=6, cols=3)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ['Capa', 'Tecnología', 'Versión']
    data = [
        ['Backend', 'Python + FastAPI + SQLAlchemy 2.0', 'Python 3.14, FastAPI 0.115+'],
        ['Frontend', 'React + TypeScript + Vite', 'React 19, TypeScript 6.0, Vite 8.1'],
        ['Base de Datos', 'MySQL + PyMySQL + Alembic', 'MySQL 8.0, PyMySQL 1.1+'],
        ['Visualización', 'Recharts + Leaflet', 'Recharts 3.9, Leaflet 1.9'],
        ['Documentación API', 'Swagger UI (OpenAPI)', 'Auto-generado por FastAPI'],
    ]
    
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "2F5496")
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.bold = True
                run.font.size = Pt(10)
    
    for i, row_data in enumerate(data):
        for j, cell_text in enumerate(row_data):
            cell = table.rows[i + 1].cells[j]
            cell.text = cell_text
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
                    run.font.name = 'Times New Roman'
    
    doc.add_paragraph()
    
    add_heading_styled(doc, 'Arquitectura del Sistema', level=2)
    
    add_paragraph_apa(doc,
        'El sistema sigue una arquitectura de tres capas tanto en el backend como en el frontend. '
        'En el backend, la estructura se organiza como Router → Service → Repository → Model, donde: '
        'los routers definen los endpoints HTTP, los servicios contienen la lógica de negocio, los '
        'repositorios manejan el acceso a datos y los modelos representan las tablas de la base de datos. '
        'La inyección de dependencias se gestiona mediante el mecanismo Depends de FastAPI, permitiendo '
        'que las dependencias como la sesión de base de datos sean provistas automáticamente.'
    )
    
    add_paragraph_apa(doc,
        'En el frontend, se utiliza React Router DOM para la navegación, Axios para las peticiones HTTP '
        'con interceptores JWT, y un contexto de autenticación (AuthContext) que persiste el token en '
        'localStorage. Cada módulo de negocio tiene su propia carpeta con componentes de lista y formulario, '
        'un archivo de API client y hooks personalizados.'
    )

    add_heading_styled(doc, 'Base de Datos', level=2)
    
    add_paragraph_apa(doc,
        'La base de datos Tecnorenta consta de 11 tablas principales modeladas con SQLAlchemy ORM. '
        'El diagrama entidad-relación se muestra en la Figura 1.'
    )
    
    der_path = os.path.join(SNAPSHOTS_DIR, "der_diagram.jpeg")
    if add_image_centered(doc, der_path, width=Inches(5)):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('Figura 1. Diagrama Entidad-Relación de la base de datos Tecnorenta.')
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.italic = True
    
    doc.add_paragraph()
    
    add_paragraph_apa(doc,
        'La base de datos implementa las siguientes entidades principales: Usuarios (autenticación y roles), '
        'Clientes (con datos fiscales NIT y ubicación geográfica), Activos (con código de inventario único, '
        'número de serie, fotos y coordenadas GPS), Categorías de Activos (jerarquía auto-referenciada), '
        'Contratos (con fechas, montos y documentos adjuntos), Pagos (asociados a contratos con conceptos '
        'y estados), Asignaciones de Activos (relacionan contratos con activos específicos), Historial de '
        'Ubicación (registro GPS de asignaciones), Checklist de Estado (evaluación de componentes en entrega '
        'y devolución), Reportes de Incidencia (con niveles de gravedad) y Mantenimientos (con herencia de '
        'tabla única para preventivos y correctivos).'
    )
    
    doc.add_page_break()
    
    add_heading_styled(doc, 'Módulos CRUD Implementados', level=2)
    
    add_paragraph_apa(doc,
        'Se implementaron 12 módulos CRUD completos, cada uno con operaciones de creación, lectura, '
        'actualización y eliminación. La Tabla 1 resume los módulos desarrollados.'
    )
    
    table2 = doc.add_table(rows=13, cols=4)
    table2.style = 'Light Grid Accent 1'
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    mod_headers = ['#', 'Módulo', 'Ruta API', 'Funcionalidades Destacadas']
    mod_data = [
        ['1', 'Usuarios', '/api/v1/usuarios', 'Gestión de usuarios con JWT y bcrypt'],
        ['2', 'Roles', '/api/v1/roles', 'Roles con asignación de permisos'],
        ['3', 'Clientes', '/api/v1/clientes', 'Clientes con NIT, dirección y mapa Leaflet'],
        ['4', 'Activos', '/api/v1/activos', 'Fotos (cámara/archivo), mapa GPS, exportación CSV'],
        ['5', 'Categorías', '/api/v1/categorias-activo', 'Categorías jerárquicas auto-referenciadas'],
        ['6', 'Contratos', '/api/v1/contratos', 'Documentos adjuntos, estados (activo/vencido/cancelado)'],
        ['7', 'Pagos', '/api/v1/pagos', 'Filtros por vencidos/próximos, registro por contrato'],
        ['8', 'Asignaciones', '/api/v1/asignaciones', 'Vinculación activo-contrato con mapa'],
        ['9', 'Checklist', '/api/v1/checklist', 'Evaluación de componentes (pantalla, teclado, etc.)'],
        ['10', 'Historial Ubicación', '/api/v1/historial-ubicacion', 'Registro GPS por asignación'],
        ['11', 'Reportes Incidencia', '/api/v1/reportes', 'Gravedad: leve/moderado/grave, adjunta foto'],
        ['12', 'Mantenimientos', '/api/v1/mantenimientos', 'Preventivo/Correctivo con herencia de tabla'],
    ]
    
    for i, header in enumerate(mod_headers):
        cell = table2.rows[0].cells[i]
        cell.text = header
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "2F5496")
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.bold = True
                run.font.size = Pt(9)
    
    for i, row_data in enumerate(mod_data):
        for j, cell_text in enumerate(row_data):
            cell = table2.rows[i + 1].cells[j]
            cell.text = cell_text
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.name = 'Times New Roman'
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Tabla 1. Módulos CRUD implementados en el Sprint 2.')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.italic = True
    
    doc.add_paragraph()
    
    add_heading_styled(doc, 'Dashboard Gerencial y KPIs', level=2)
    
    add_paragraph_apa(doc,
        'El dashboard principal presenta un panel con los siguientes indicadores clave de rendimiento (KPI): '
        'conteo de usuarios, clientes, activos y contratos registrados; total de ingresos mensuales calculados '
        'a partir de contratos activos; contratos próximos a vencer en los próximos 30 días; mantenimientos '
        'pendientes; incidencias abiertas; y pagos vencidos. Adicionalmente, se incluyen dos gráficos '
        'interactivos generados con Recharts: un gráfico de barras para la distribución de contratos por '
        'estado y un gráfico de pastel para la distribución de activos por estado.'
    )
    
    add_paragraph_apa(doc,
        'La Figura 2 muestra la interfaz del dashboard con todos los KPIs y gráficos operativos.'
    )

    dash_path = os.path.join(SNAPSHOTS_DIR, "dashboard.png")
    if add_image_centered(doc, dash_path, width=Inches(5.5)):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('Figura 2. Dashboard principal con KPIs y gráficos Recharts.')
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.italic = True
    
    doc.add_paragraph()
    
    add_heading_styled(doc, 'Consultas SQL Complejas', level=2)
    
    add_paragraph_apa(doc,
        'El sistema implementa seis consultas SQL complejas en el servicio de dashboard, utilizando '
        'funciones de agregación, JOINs implícitos, filtros por fecha y agrupaciones. A continuación '
        'se describen las consultas implementadas:'
    )
    
    sql_queries = [
        ('Consulta 1 — Conteo de activos por estado',
         'SELECT activos.estado, COUNT(*) as cantidad FROM activos GROUP BY activos.estado',
         'Agrupa todos los activos por su estado actual (disponible, rentado, mantenimiento, baja) '
         'y cuenta cuántos hay en cada categoría.'),
        ('Consulta 2 — Conteo de contratos por estado',
         'SELECT contratos.estado, COUNT(*) as cantidad FROM contratos GROUP BY contratos.estado',
         'Similar a la anterior pero para contratos, agrupando por estado (activo, vencido, cancelado, renovado).'),
        ('Consulta 3 — Contratos próximos a vencer (30 días)',
         'SELECT COUNT(*) FROM contratos WHERE estado = "activo" AND fecha_fin BETWEEN hoy AND hoy + 30',
         'Identifica contratos activos cuya fecha de fin está dentro de los próximos 30 días, '
         'permitiendo alertas proactivas al usuario.'),
        ('Consulta 4 — Ingresos mensuales totales',
         'SELECT COALESCE(SUM(monto_mensual), 0) FROM contratos WHERE estado = "activo"',
         'Suma los montos mensuales de todos los contratos activos para calcular el ingreso recurrente total.'),
        ('Consulta 5 — Contratos próximos a vencer con datos del cliente (JOIN)',
         'SELECT c.*, cl.razon_social FROM contratos c JOIN clientes cl ON c.id_cliente = cl.id WHERE c.estado = "activo" AND c.fecha_fin <= limite',
         'Realiza un JOIN entre contratos y clientes para mostrar información detallada de los contratos '
         'próximos a vencer, incluyendo el nombre del cliente.'),
        ('Consulta 6 — Incidencias no cerradas',
         'SELECT COUNT(*) FROM reportes_incidencia WHERE estado != "cerrado"',
         'Cuenta todas las incidencias que aún no han sido cerradas, proporcionando un indicador de '
         'carga de trabajo pendiente.'),
    ]
    
    for title, query, desc in sql_queries:
        p = doc.add_paragraph()
        run = p.add_run(title + ': ')
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run = p.add_run(desc)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        p.paragraph_format.line_spacing = 2.0
        
        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.paragraph_format.left_indent = Cm(1.5)
        p2.paragraph_format.line_spacing = 1.0
        run = p2.add_run(query)
        run.font.name = 'Courier New'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(33, 37, 41)
        
        doc.add_paragraph()
    
    doc.add_page_break()
    
    add_heading_styled(doc, 'Capturas de Pantalla del Sistema', level=2)
    
    modules_for_screenshots = [
        ('Módulo de Activos — Listado', 'activos_lista.png', 'Figura 3. Listado de activos con tabla de datos, exportación CSV y acciones por fila.'),
        ('Módulo de Activos — Formulario', 'activos_formulario.png', 'Figura 4. Formulario de activos con mapa Leaflet para ubicación GPS.'),
        ('Módulo de Contratos', 'contratos_lista.png', 'Figura 5. Listado de contratos con montos, fechas y estados.'),
        ('Módulo de Pagos', 'pagos_lista.png', 'Figura 6. Listado de pagos con conceptos, montos y estados.'),
        ('Módulo de Asignaciones', 'asignaciones_lista.png', 'Figura 7. Asignaciones de activos a contratos.'),
        ('Módulo de Usuarios', 'usuarios_lista.png', 'Figura 8. Gestión de usuarios del sistema.'),
        ('Módulo de Roles', 'roles_lista.png', 'Figura 9. Administración de roles y permisos.'),
        ('Módulo de Clientes', 'clientes_lista.png', 'Figura 10. Listado de clientes con datos fiscales.'),
        ('Módulo de Categorías', 'categorias_lista.png', 'Figura 11. Categorías jerárquicas de activos.'),
        ('Módulo de Mantenimientos', 'mantenimientos_lista.png', 'Figura 12. Registro de mantenimientos preventivos y correctivos.'),
        ('Módulo de Reportes de Incidencia', 'reportes_lista.png', 'Figura 13. Reportes de incidencias con niveles de gravedad.'),
        ('Documentación API — Swagger UI', 'swagger_docs.png', 'Figura 14. Documentación interactiva de la API en Swagger UI.'),
    ]
    
    for title, filename, caption in modules_for_screenshots:
        add_paragraph_mixed(doc, [(title + ': ', True, False)], size=12)
        img_path = os.path.join(SNAPSHOTS_DIR, filename)
        if add_image_centered(doc, img_path, width=Inches(5.5)):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(caption)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
            run.italic = True
        doc.add_paragraph()
    
    doc.add_page_break()

    # ======================== RESULTADOS Y ANÁLISIS ========================
    add_heading_styled(doc, 'Resultados y Análisis', level=1)
    
    add_paragraph_apa(doc,
        'Al finalizar el Sprint 2, el sistema SIGTAR cuenta con doce módulos CRUD completamente funcionales, '
        'un dashboard gerencial con KPIs y gráficos, y una API documentada con Swagger. La base de datos '
        'contiene datos de prueba representativos: 20 activos, 10 clientes, 8 contratos, 18 pagos, 10 '
        'asignaciones y 5 reportes de incidencia, lo que permite demostrar todas las funcionalidades del sistema.'
    )
    
    add_paragraph_apa(doc,
        'Las pruebas funcionales realizadas sobre cada módulo verificaron que las operaciones de creación, '
        'lectura, actualización y eliminación se ejecutan correctamente. El dashboard responde con los datos '
        'agregados en tiempo real, y los gráficos de Recharts se renderizan correctamente mostrando la '
        'distribución de activos y contratos por estado. La documentación Swagger expone los 45 endpoints '
        'de la API con sus esquemas de solicitud y respuesta, permitiendo pruebas interactivas desde el navegador.'
    )
    
    add_paragraph_apa(doc,
        'Entre los aspectos positivos destacan: la correcta implementación de la arquitectura de tres capas, '
        'la integración del mapa Leaflet para ubicación geográfica, la subida de fotos mediante cámara o '
        'archivo, la exportación de activos a CSV, y la autenticación JWT con control de acceso basado en roles. '
        'Como áreas de mejora se identifican: la necesidad de implementar un sistema de notificaciones para '
        'alertar sobre contratos próximos a vencer, la optimización de consultas para grandes volúmenes de '
        'datos, y la inclusión de pruebas automatizadas.'
    )

    doc.add_page_break()

    # ======================== SCRUM ========================
    add_heading_styled(doc, 'Metodología Scrum', level=1)
    
    add_heading_styled(doc, 'Planificación del Sprint 2', level=2)
    
    add_paragraph_apa(doc,
        'El Sprint 2 tuvo una duración de 3 semanas (del 1 al 21 de marzo de 2026). El objetivo principal '
        'fue implementar todos los módulos CRUD del sistema, el dashboard gerencial y las consultas SQL '
        'complejas. El equipo estuvo compuesto por 4 desarrolladores trabajando en las siguientes áreas: '
        '2 en backend (API, modelos, servicios), 1 en frontend (componentes, páginas, integración) y 1 en '
        'base de datos (modelado, migraciones, datos de prueba).'
    )
    
    add_heading_styled(doc, 'Burndown Chart', level=2)
    
    add_paragraph_apa(doc,
        'La Figura 15 muestra el burndown chart del Sprint 2, que ilustra el trabajo completado a lo largo '
        'del sprint en comparación con la línea de referencia ideal.'
    )
    
    burndown_path = os.path.join(SNAPSHOTS_DIR, "burndown_chart.png")
    if os.path.exists(burndown_path):
        add_image_centered(doc, burndown_path, width=Inches(4.5))
    else:
        burndown_table = doc.add_table(rows=8, cols=4)
        burndown_table.style = 'Light Grid Accent 1'
        burndown_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        bd_headers = ['Sprint Day', 'Tareas Pendientes', 'Tareas Completadas', 'Línea Ideal']
        bd_data = [
            ['Día 1', '24', '0', '24'],
            ['Día 3', '22', '2', '20'],
            ['Día 6', '18', '6', '16'],
            ['Día 9', '14', '10', '12'],
            ['Día 12', '9', '15', '8'],
            ['Día 15', '5', '19', '4'],
            ['Día 21', '0', '24', '0'],
        ]
        
        for i, header in enumerate(bd_headers):
            cell = burndown_table.rows[0].cells[i]
            cell.text = header
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_shading(cell, "2F5496")
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.color.rgb = RGBColor(255, 255, 255)
                    run.font.bold = True
                    run.font.size = Pt(9)
        
        for i, row_data in enumerate(bd_data):
            for j, cell_text in enumerate(row_data):
                cell = burndown_table.rows[i + 1].cells[j]
                cell.text = cell_text
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in p.runs:
                        run.font.size = Pt(9)
                        run.font.name = 'Times New Roman'
        
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('Tabla 2. Datos del Burndown Chart del Sprint 2.')
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.italic = True
    
    doc.add_paragraph()
    
    add_heading_styled(doc, 'Sprint Review', level=2)
    
    add_paragraph_apa(doc,
        'Al finalizar el Sprint 2, se presentaron los siguientes entregables al Product Owner:'
    )
    
    review_items = [
        'Sistema funcional con 12 módulos CRUD operativos en los entornos de desarrollo y pruebas.',
        'Dashboard gerencial con 7 KPIs y 2 gráficos interactivos (barras y pastel).',
        'Base de datos MySQL con 11 tablas, migraciones Alembic y datos de prueba.',
        'API REST documentada con Swagger UI accesible en /docs.',
        'Autenticación JWT con bcrypt para hash de contraseñas.',
        'Sistema de subida de fotos (cámara + archivo) para activos.',
        'Mapa Leaflet interactivo para ubicación de activos y clientes.',
        'Exportación de datos a CSV para el módulo de activos.',
    ]
    for item in review_items:
        p = doc.add_paragraph(item, style='List Bullet')
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
        p.paragraph_format.line_spacing = 2.0
    
    add_heading_styled(doc, 'Retrospectiva (Start / Stop / Continue)', level=2)
    
    retro_table = doc.add_table(rows=4, cols=2)
    retro_table.style = 'Light Grid Accent 1'
    retro_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    retro_headers = ['Categoría', 'Acciones']
    retro_data = [
        ['Start (Empezar a hacer)',
         '• Escribir pruebas automatizadas antes del código (TDD)\n'
         '• Realizar code reviews semanales\n'
         '• Documentar decisiones técnicas en el repositorio'],
        ['Stop (Dejar de hacer)',
         '• Trabajar en ramas sin actualizar desde main\n'
         '• Acumular deuda técnica en componentes shared\n'
         '• Ignorar warnings de compilación'],
        ['Continue (Seguir haciendo)',
         '• Commits atómicos y descriptivos\n'
         '• Comunicación diaria en el daily standup\n'
         '• Mantener la arquitectura de capas separada'],
    ]
    
    for i, header in enumerate(retro_headers):
        cell = retro_table.rows[0].cells[i]
        cell.text = header
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "2F5496")
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.bold = True
                run.font.size = Pt(10)
    
    for i, row_data in enumerate(retro_data):
        for j, cell_text in enumerate(row_data):
            cell = retro_table.rows[i + 1].cells[j]
            cell.text = cell_text
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
                    run.font.name = 'Times New Roman'
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Tabla 3. Retrospectiva del Sprint 2 — Start / Stop / Continue.')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.italic = True
    
    doc.add_page_break()

    # ======================== CONCLUSIONES ========================
    add_heading_styled(doc, 'Conclusiones', level=1)
    
    conclusions = [
        'El Sprint 2 cumplió con todos los objetivos planteados, logrando un sistema funcional con 12 módulos '
        'CRUD, un dashboard gerencial con KPIs y consultas SQL complejas que satisfacen los requisitos '
        'establecidos en la rúbrica de evaluación.',
        
        'La arquitectura de tres capas (router-servicio-repositorio) demostró ser efectiva para mantener '
        'la separación de responsabilidades y facilitar el mantenimiento del código. Cada capa tiene una '
        'función claramente definida, lo que permite realizar cambios en una capa sin afectar las demás.',
        
        'La implementación de consultas SQL complejas utilizando SQLAlchemy ORM permitió obtener indicadores '
        'en tiempo real para la toma de decisiones gerenciales, incluyendo ingresos mensuales, distribución '
        'de activos por estado y alertas de contratos próximos a vencer.',
        
        'La integración de tecnologías modernas como Recharts para visualización de datos y Leaflet para '
        'mapas interactivos mejoró significativamente la experiencia de usuario, proporcionando interfaces '
        'intuitivas y visualmente atractivas.',
        
        'Se identificó la necesidad de incorporar pruebas automatizadas en el próximo sprint para garantizar '
        'la calidad del código y facilitar la detección temprana de errores durante el desarrollo de nuevas '
        'funcionalidades.',
    ]
    
    for i, conclusion in enumerate(conclusions, 1):
        p = doc.add_paragraph()
        run = p.add_run(f'{i}. ')
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run = p.add_run(conclusion)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.space_after = Pt(12)

    doc.add_page_break()

    # ======================== REFERENCIAS ========================
    add_heading_styled(doc, 'Referencias', level=1)
    
    references = [
        'Bayer, M. (2012). SQLAlchemy: The Database Toolkit for Python. https://www.sqlalchemy.org/',
        'Fowler, M. (2002). Patterns of Enterprise Application Architecture. Addison-Wesley.',
        'Meta Platforms. (2013). React: A JavaScript library for building user interfaces. https://react.dev/',
        'Ramírez, S. (2018). FastAPI: Modern, fast (high-performance) web framework for building APIs with Python. https://fastapi.tiangolo.com/',
        'Recharts. (2021). Recharts: A composable charting library built on React components. https://recharts.org/',
        'Schwaber, K., & Sutherland, J. (2020). The Scrum Guide: The Definitive Guide to Scrum. https://scrumguides.org/',
        'Agafonkin, V. (2010). Leaflet: An open-source JavaScript library for mobile-friendly interactive maps. https://leafletjs.com/',
    ]
    
    for i, ref in enumerate(references, 1):
        p = doc.add_paragraph()
        run = p.add_run(ref)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        p.paragraph_format.line_spacing = 2.0
        p.paragraph_format.left_indent = Cm(1.27)
        p.paragraph_format.first_line_indent = Cm(-1.27)
        p.paragraph_format.space_after = Pt(12)

    doc.add_page_break()

    # ======================== ANEXOS ========================
    add_heading_styled(doc, 'Anexos', level=1)
    
    add_heading_styled(doc, 'Anexo A: Estructura de la Base de Datos (SQL)', level=2)
    
    add_paragraph_apa(doc,
        'El código completo del dump de la base de datos se encuentra en el archivo '
        'tecnorenta.sql incluido en la carpeta informe/Sprint2/. A continuación se muestra '
        'el script DDL de las tablas principales:'
    )
    
    sql_path = os.path.join(os.path.dirname(__file__), "tecnorenta.sql")
    if os.path.exists(sql_path):
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        sql_excerpt = sql_content[:3000]
        
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(sql_excerpt + '\n\n[...]')
        run.font.name = 'Courier New'
        run.font.size = Pt(8)
    
    doc.add_paragraph()
    
    add_heading_styled(doc, 'Anexo B: Documentación de la API (Swagger)', level=2)
    
    add_paragraph_apa(doc,
        'El archivo tecnorenta_openapi.json contiene la especificación OpenAPI completa del sistema, '
        'exportable a Postman u otras herramientas de testing API. La documentación interactiva está '
        'disponible en http://localhost:8000/docs mientras el servidor backend esté en ejecución.'
    )
    
    add_paragraph_apa(doc,
        'Para importar la colección en Postman: File → Import → seleccionar el archivo '
        'tecnorenta_openapi.json. Postman generará automáticamente las carpetas y endpoints organizados '
        'por tags.'
    )

    add_page_number(doc)
    
    output_path = os.path.join(os.path.dirname(__file__), 'SIGTAR_Sprint2_Informe_APA7.docx')
    doc.save(output_path)
    print(f"Informe generado: {output_path}")
    return output_path

if __name__ == '__main__':
    create_informe()
