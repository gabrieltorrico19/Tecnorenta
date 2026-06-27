"""Generate Sprint 1 APA 7 Word document for SIGTAR project."""

import base64
import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

CAPTURAS_DIR = os.path.join(os.path.dirname(__file__), "capturas")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "SIGTAR_Sprint1_Informe_APA7.docx")

# ─── helpers ─────────────────────────────────────────────────────────────────

def set_cell_shading(cell, color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def add_table_row(table, cells_data, bold=False, header=False):
    row = table.add_row()
    for i, text in enumerate(cells_data):
        cell = row.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(str(text))
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.bold = bold
        if header:
            set_cell_shading(cell, "2B579A")
            run.font.color.rgb = RGBColor(255, 255, 255)
    return row

def add_screenshot(doc, filename, width=Inches(5.5), caption=""):
    path = os.path.join(CAPTURAS_DIR, filename)
    if not os.path.exists(path):
        doc.add_paragraph(f"[Imagen no encontrada: {filename}]")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(path, width=width)
    if caption:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run(f"Figura. {caption}")
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.italic = True

def apa_paragraph(doc, text, bold=False, italic=False, space_after=Pt(0)):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.first_line_indent = Cm(1.27)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.bold = bold
    run.italic = italic
    return p

def apa_heading(doc, text, level):
    """Create APA 7 heading."""
    h = doc.add_heading(text, level=level)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in h.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        if level == 1:
            run.bold = True
            run.font.size = Pt(14)
        elif level == 2:
            run.bold = True
            run.font.size = Pt(12)
        elif level == 3:
            run.bold = True
            run.italic = True
            run.font.size = Pt(12)
        elif level == 4:
            run.bold = False
            run.italic = True
            run.font.size = Pt(12)
    return h

def set_apa_margins(doc):
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

# ─── main ─────────────────────────────────────────────────────────────────────

def create_document():
    doc = Document()

    # ── Global styles ──
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing = 2.0
    set_apa_margins(doc)

    # ════════════════════════════════════════════════════════════════════════════
    #  PORTADA APA 7
    # ════════════════════════════════════════════════════════════════════════════
    for _ in range(6):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run("Informe Técnico del Sprint 1\nDesarrollo del Núcleo Técnico del Sistema SIGTAR\nSistema de Información para la Gestión y Trazabilidad\ndel Leasing de Activos - TecnoRenta Oriente S.R.L.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True

    doc.add_paragraph()

    authors = [
        "Samuel Ignacio Parada Quiroga (Scrum Master - Líder de grupo)",
        "Gabriel Torrico Arce (Product Owner)",
        "Kevin Adalid Mirones Patiño (Desarrollador - Dev Lead)",
    ]
    for a in authors:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 2.0
        r = p.add_run(a)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    doc.add_paragraph()
    doc.add_paragraph()

    lines = [
        "Universidad Privada Domingo Savio (UPDS)",
        "Asignatura: Sistemas de Información II",
        "Docente: Ing. Jimmy Nataniel Requena Llorentty",
        "Santa Cruz de la Sierra, Bolivia",
        "Julio de 2026",
    ]
    for l in lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 2.0
        r = p.add_run(l)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════════════
    #  RESUMEN EJECUTIVO
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "Resumen Ejecutivo", level=1)

    apa_paragraph(doc, (
        "El presente informe documenta los resultados del Sprint 1 del proyecto SIGTAR, correspondiente al "
        "desarrollo del núcleo técnico del sistema de información para la gestión y trazabilidad del leasing de "
        "activos de TecnoRenta Oriente S.R.L. Durante este sprint, se implementó una base de datos relacional "
        "normalizada en tercera forma normal (3FN) con 15 tablas, 117 registros de prueba con datos latinoamericanos, "
        "un módulo de autenticación basado en JWT con bcrypt (saltRounds=10), un sistema de roles y permisos con "
        "seis roles y 33 permisos granulares, y un frontend React 19 con TypeScript que integra mapas Leaflet, "
        "captura fotográfica vía webcam y gráficos Recharts. El stack tecnológico seleccionado fue Python 3.14+ "
        "con FastAPI y SQLAlchemy 2.0 para el backend, MySQL (XAMPP) como gestor de base de datos, y React 19 "
        "con Vite para el frontend. El control de versiones se realizó en GitHub con ramas main/develop y 13 "
        "commits semánticos. La retrospectiva identifica como principales aciertos la arquitectura modular en "
        "capas y la experiencia de usuario del frontend, y como áreas de mejora la necesidad de pruebas "
        "automatizadas y la planificación de tareas técnicas."
    ))

    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.27)
    p.paragraph_format.line_spacing = 2.0
    r = p.add_run("Palabras clave: ")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r = p.add_run("Sprint 1, autenticación JWT, roles y permisos, base de datos 3NF, FastAPI, React, SIGTAR")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════════════
    #  1. INTRODUCCIÓN
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "1. Introducción", level=1)

    apa_paragraph(doc,
        "La transformación digital de las micro, pequeñas y medianas empresas (MIPYMES) en América Latina "
        "representa un desafío y una oportunidad para la modernización de los procesos operativos. TecnoRenta "
        "Oriente S.R.L., una PYME boliviana dedicada al alquiler de laptops a domicilio, enfrentaba problemas "
        "de información como inventario y contratos gestionados en Excel disperso, pérdida de 8 a 12 horas "
        "semanales en tareas manuales, renovaciones de contratos omitidas por falta de alertas, y decisiones "
        "gerenciales basadas en corazonadas en lugar de datos."
    )

    apa_paragraph(doc, (
        "El Sprint 0 del proyecto (configuración del entorno ágil Scrum) definió un equipo Scrum con roles "
        "claros, un Product Backlog de 23 historias de usuario priorizadas con MoSCoW y estimadas con Planning "
        "Poker, y un Sprint 1 Backlog centrado en las historias Must Have. El objetivo del Sprint 1 fue: "
        "'Disponer de un acceso seguro por roles y un inventario centralizado de activos operativo, que "
        "reemplace el Excel del almacén y garantice que solo usuarios autorizados accedan al sistema'."
    ))

    apa_paragraph(doc, (
        "El presente informe detalla los resultados alcanzados: la implementación de la base de datos "
        "relacional normalizada en 3FN con 15 tablas, el módulo de autenticación JWT con bcrypt, el sistema "
        "de roles y permisos con middleware de autorización, el frontend React con mapa interactivo y "
        "captura fotográfica, y el control de versiones con 13 commits en GitHub. Se incluyen capturas de "
        "pantalla del API documentada con Swagger, del frontend funcional, de la base de datos y del "
        "repositorio. Finalmente, se presentan la retrospectiva Start/Stop/Continue y las conclusiones "
        "del sprint."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  2. MARCO TEÓRICO
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "2. Marco Teórico", level=1)

    apa_heading(doc, "2.1 Scrum y Gestión Ágil de Proyectos", level=2)
    apa_paragraph(doc, (
        "Scrum es un marco de trabajo liviano que ayuda a las personas, equipos y organizaciones a generar "
        "valor mediante soluciones adaptativas para problemas complejos (Schwaber & Sutherland, 2020). Se "
        "sustenta en el empirismo y el pensamiento Lean, y organiza el trabajo en iteraciones de duración "
        "fija llamadas sprints. El Sprint 1 del proyecto SIGTAR tuvo una duración de dos semanas e incluyó "
        "las ceremonias de Sprint Planning, Daily Scrum, Sprint Review y Retrospectiva."
    ))

    apa_heading(doc, "2.2 Autenticación JWT y bcrypt", level=2)
    apa_paragraph(doc, (
        "JSON Web Token (JWT) es un estándar abierto (RFC 7519) que define una forma compacta y autónoma "
        "de transmitir información entre partes como un objeto JSON. En el contexto de APIs REST, se utiliza "
        "para autenticación stateless: el servidor genera un token firmado que el cliente envía en el "
        "encabezado Authorization de cada solicitud (Jones et al., 2015). El algoritmo de hash bcrypt "
        "incorpora un salt aleatorio y un factor de costo (saltRounds) que hace que el hash sea resistente "
        "a ataques de fuerza bruta (Provos & Mazières, 1999)."
    ))

    apa_heading(doc, "2.3 Normalización de Bases de Datos (3FN)", level=2)
    apa_paragraph(doc, (
        "La normalización es un proceso sistemático para organizar los datos en una base de datos relacional "
        "con el objetivo de reducir la redundancia y evitar anomalías de actualización. La primera forma "
        "normal (1FN) elimina grupos repetitivos; la segunda (2FN) elimina dependencias parciales; la "
        "tercera (3FN) elimina dependencias transitivas (Codd, 1970; Date, 2004). Todas las tablas del "
        "sistema SIGTAR cumplen con 3FN."
    ))

    apa_heading(doc, "2.4 Vinculación con los ODS", level=2)
    apa_paragraph(doc, (
        "El proyecto SIGTAR se alinea con tres Objetivos de Desarrollo Sostenible de la Agenda 2030: "
        "ODS 8 (Trabajo decente y crecimiento económico) al liberar horas productivas mediante la "
        "automatización de procesos manuales; ODS 9 (Industria, innovación e infraestructura) al "
        "implementar una solución tecnológica innovadora para una PYME; y ODS 12 (Producción y consumo "
        "responsables) al extender la vida útil de los activos mediante mantenimiento preventivo y "
        "trazabilidad."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  3. STACK TECNOLÓGICO
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "3. Stack Tecnológico", level=1)

    apa_paragraph(doc, (
        "El equipo seleccionó el stack Python/FastAPI/React/MySQL tras evaluar las opciones propuestas en "
        "la guía del sprint. Se descartó PHP/Laravel por la menor experiencia del equipo y Node.js/Express "
        "por la preferencia del equipo por el tipado estático de Python y TypeScript. El stack final quedó "
        "conformado por los siguientes componentes:"
    ))

    # Tabla de stack
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, text in enumerate(["Capa", "Tecnología", "Versión"]):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.bold = True
        set_cell_shading(cell, "2B579A")
        run.font.color.rgb = RGBColor(255, 255, 255)

    stack_data = [
        ("Backend", "Python 3.14+ / FastAPI / SQLAlchemy 2.0 / Alembic / PyMySQL / Pydantic v2", "3.14 / 0.115+ / 2.0 / 1.14+ / 1.1+ / 2.10+"),
        ("Autenticación", "python-jose + bcrypt + HTTPBearer", "3.3+ / 4.2+"),
        ("Base de datos", "MySQL (XAMPP / MariaDB)", "10.4 (MariaDB)"),
        ("Frontend", "React 19 / TypeScript 6 / Vite 8 / Axios", "19.2 / 6.0 / 8.1 / 1.18"),
        ("Mapas", "Leaflet 1.9 + react-leaflet 5", "1.9.4 / 5.0"),
        ("Gráficos", "Recharts", "3.9"),
        ("Iconos", "Lucide React", "1.21"),
        ("Control de versiones", "Git + GitHub", "—"),
        ("Entorno local", "XAMPP (Apache + MySQL) / VS Code", "8.x / 1.98"),
    ]
    for row_data in stack_data:
        add_table_row(table, row_data)

    # Captura
    add_screenshot(doc, "swagger_docs.png", width=Inches(5.2),
                   caption="Interfaz Swagger UI con todos los endpoints del API REST en /docs.")

    apa_paragraph(doc, (
        "La Figura 1 muestra la documentación interactiva del API generada automáticamente por FastAPI "
        "con Swagger UI, donde se pueden visualizar y probar los 13 routers registrados con sus endpoints "
        "CRUD completos."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  4. BASE DE DATOS RELACIONAL (3FN)
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "4. Base de Datos Relacional", level=1)

    apa_heading(doc, "4.1 Diseño y Normalización", level=2)
    apa_paragraph(doc, (
        "La base de datos fue diseñada a partir del diagrama de clases de la Actividad 2, aplicando "
        "las reglas de normalización hasta tercera forma normal (3FN). El modelo relacional resultante "
        "consta de 15 tablas que representan las entidades principales del negocio de alquiler de activos."
    ))

    apa_paragraph(doc, (
        "Análisis de normalización:"
    ))
    apa_paragraph(doc, (
        "• Primera forma normal (1FN): Cada tabla tiene una clave primaria (id), los atributos son "
        "atómicos (no hay grupos repetitivos), y cada columna contiene un solo valor por fila. Por ejemplo, "
        "la tabla activos tiene una columna modelo (varchar) en lugar de múltiples columnas de modelo."
    ))
    apa_paragraph(doc, (
        "• Segunda forma normal (2FN): Todas las tablas cumplen con 1FN y los atributos no clave "
        "dependen completamente de la clave primaria. Las tablas pivote como roles_permisos tienen "
        "clave primaria compuesta (id_rol, id_permiso) y ningún atributo no clave."
    ))
    apa_paragraph(doc, (
        "• Tercera forma normal (3FN): No existen dependencias transitivas. Por ejemplo, en la tabla "
        "activos, el atributo id_categoria depende directamente de la clave primaria id, no de otro "
        "atributo no clave. La información de la categoría se obtiene mediante JOIN con la tabla "
        "categorias_activo."
    ))

    apa_heading(doc, "4.2 Tablas del Sistema", level=2)

    tables_data = [
        ("roles", "id, nombre (unique)", "Almacena los 6 roles del sistema (Administrador a Cliente)"),
        ("permisos", "id, nombre (unique), descripcion", "Catálogo de 33 permisos granulares (modulo.accion)"),
        ("roles_permisos", "id_rol (FK), id_permiso (FK)", "Tabla pivote para asignación N:M de permisos a roles"),
        ("usuarios", "id, nombre, email (unique), password_hash, telefono, activo, id_rol (FK), created_at, updated_at", "Usuarios del sistema con hash bcrypt y rol asignado"),
        ("categorias_activo", "id, nombre, nivel, descripcion, id_categoria_padre (FK auto-ref)", "Categorías jerárquicas de activos (auto-referencia para subcategorías)"),
        ("clientes", "id, razon_social, nit (unique), direccion, latitud, longitud, sector", "Clientes con NIT único y coordenadas geográficas"),
        ("activos", "id, codigo_inventario (unique), modelo, numero_serie (unique), estado (ENUM), fecha_compra, valor_depreciado, id_categoria (FK), latitud, longitud, creado_por (FK), fecha_creacion, modificado_por (FK)", "Inventario de activos con estado ENUM y coordenadas GPS"),
        ("contratos", "id, fecha_inicio, fecha_fin, condiciones_uso, estado (ENUM), monto_mensual, id_cliente (FK), creado_por (FK)", "Contratos de alquiler con montos y estados"),
        ("pagos", "id, id_contrato (FK), concepto, monto, fecha, estado (ENUM)", "Registro de pagos vinculados a contratos"),
        ("asignaciones_activo", "id, fecha_asignacion, fecha_devolucion, latitud, longitud, id_contrato (FK), id_activo (FK), creado_por (FK)", "Asignación física de activos con ubicación GPS"),
        ("historial_ubicacion", "id, id_asignacion (FK), latitud, longitud, timestamp", "Historial de movimientos GPS de activos asignados"),
        ("checklist_estado", "id, id_asignacion (FK), momento (ENUM), pantalla (ENUM), teclado (ENUM), carcasa (ENUM), cargador, observaciones, url_fotos, id_usuario (FK)", "Checklist de entrega/devolución con estado de componentes"),
        ("reportes_incidencia", "id, fecha, descripcion, gravedad (ENUM), url_foto, estado (ENUM), id_activo (FK), creado_por (FK)", "Reportes de incidentes con clasificación de gravedad"),
        ("mantenimientos", "id, tipo (ENUM polimórfico), fecha, costo, descripcion, url_foto, id_activo (FK), frecuencia_dias, proxima_fecha, id_reporte_origen (FK), tiempo_reparacion", "Mantenimientos preventivos y correctivos (herencia de tabla única)"),
        ("activos_fotos", "id, id_activo (FK), url, orden, fecha_subida", "Fotografías de activos con orden y URL"),
    ]

    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, text in enumerate(["Tabla", "Columnas (PK, FK, UNIQUE)", "Descripción"]):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(8)
        run.bold = True
        set_cell_shading(cell, "2B579A")
        run.font.color.rgb = RGBColor(255, 255, 255)

    for tn, cols, desc in tables_data:
        add_table_row(table, [tn, cols, desc])

    apa_paragraph(doc, (
        "La base de datos incluye 6 tipos ENUM (EstadoActivo, EstadoContrato, EstadoPago, GravedadIncidencia, "
        "EstadoIncidencia, MomentoChecklist, EstadoComponente, TipoMantenimiento) que garantizan la integridad "
        "de los datos restringiendo los valores permitidos a nivel de base de datos."
    ))

    apa_heading(doc, "4.3 Constraints y Relaciones", level=2)
    apa_paragraph(doc, (
        "Se implementaron las siguientes restricciones de integridad referencial: clave primaria (PK) "
        "autoincremental en todas las tablas, clave única (UNIQUE) en email (usuarios), nit (clientes), "
        "codigo_inventario y numero_serie (activos), nombre (roles y permisos). Las claves foráneas (FK) "
        "garantizan la integridad referencial entre tablas relacionadas. Además, la tabla categorias_activo "
        "tiene una auto-referencia (id_categoria_padre → id) para soportar jerarquías de categorías, y "
        "la tabla mantenimientos utiliza herencia de tabla única (single table inheritance) discriminada "
        "por la columna tipo."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  5. DATOS DE PRUEBA
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "5. Datos de Prueba (50+ registros LATAM)", level=1)

    apa_paragraph(doc, (
        "Se generaron 117 registros de prueba con datos latinoamericanos realistas utilizando scripts "
        "Python que insertan datos directamente en la base de datos. Los datos incluyen nombres de "
        "empresas bolivianas, ciudades de Bolivia (Santa Cruz, La Paz, Cochabamba, Tarija, Sucre), "
        "moneda local (bolivianos), y NITs con formato boliviano."
    ))

    apa_heading(doc, "5.1 Distribución de Registros", level=2)

    count_data = [
        ("roles", "6", "Administrador, Gerente, Almacén, Técnico, Operador, Cliente"),
        ("permisos", "33", "Permisos granulares (modulo.accion) para 8 módulos"),
        ("usuarios", "1", "Usuario administrador por defecto (admin@tecnorenta.com)"),
        ("clientes", "10", "Empresas bolivianas (TechSolutions, DataCenter Bolivia, NetLogic, etc.)"),
        ("categorias_activo", "6", "2 categorías padre, 4 subcategorías (Laptops Gamer, Oficina, Ultraligeras, Monitores)"),
        ("activos", "20", "Laptops de todas las subcategorías con datos realistas de serie y compra"),
        ("contratos", "8", "Contratos con fechas, montos y estados variados"),
        ("pagos", "18", "Cuotas mensuales de contratos activos"),
        ("asignaciones_activo", "10", "Asignaciones con coordenadas GPS en territorio boliviano"),
        ("reportes_incidencia", "5", "Incidencias con gravedad (leve, moderado, grave)"),
    ]

    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, text in enumerate(["Tabla", "Registros", "Detalle"]):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.bold = True
        set_cell_shading(cell, "2B579A")
        run.font.color.rgb = RGBColor(255, 255, 255)

    for tn, cnt, det in count_data:
        add_table_row(table, [tn, cnt, det])

    apa_paragraph(doc, (
        "Además del administrador predeterminado, el sistema incluye datos de prueba generados con "
        "distribuciones aleatorias controladas para estados (disponible, rentado, mantenimiento), "
        "fechas de compra (2024-2025), valores depreciados (0-2500 BOB), y coordenadas geográficas "
        "centradas en Santa Cruz de la Sierra, Bolivia."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  6. AUTENTICACIÓN JWT
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "6. Autenticación JWT", level=1)

    apa_heading(doc, "6.1 Implementación", level=2)
    apa_paragraph(doc, (
        "El módulo de autenticación se implementó siguiendo el estándar JWT (RFC 7519) con las "
        "siguientes características técnicas: algoritmo de hash bcrypt con saltRounds=10 para el "
        "almacenamiento seguro de contraseñas; generación de tokens JWT firmados con HS256 y "
        "expiración de 24 horas; middleware HTTPBearer para la extracción automática del token "
        "del encabezado Authorization; y dependencia get_current_user que decodifica y valida el "
        "token en cada solicitud protegida."
    ))

    apa_heading(doc, "6.2 Endpoints de Autenticación", level=2)

    endpoints = [
        ("POST /api/v1/auth/login", "Login con email y password, retorna JWT"),
        ("POST /api/v1/auth/register", "Registro de nuevo usuario (asigna rol Cliente)"),
        ("GET /api/v1/auth/me", "Perfil del usuario autenticado (requiere token)"),
        ("POST /api/v1/auth/forgot-password", "Solicitud de recuperación de contraseña"),
        ("POST /api/v1/auth/reset-password", "Reseteo de contraseña con token"),
    ]

    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, text in enumerate(["Endpoint", "Descripción"]):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.bold = True
        set_cell_shading(cell, "2B579A")
        run.font.color.rgb = RGBColor(255, 255, 255)

    for ep, desc in endpoints:
        add_table_row(table, [ep, desc])

    apa_paragraph(doc, (
        "El siguiente ejemplo muestra la respuesta del endpoint de login con credenciales válidas. "
        "El token JWT retornado debe incluirse en el encabezado Authorization: Bearer <token> para "
        "acceder a los endpoints protegidos."
    ))

    # Thunder Client screenshot
    add_screenshot(doc, "login.png", width=Inches(4.0),
                   caption="Pantalla de inicio de sesión del frontend React.")

    apa_paragraph(doc, (
        "La Figura 2 muestra la interfaz de login del frontend, que envía las credenciales al "
        "endpoint POST /api/v1/auth/login y almacena el token JWT en localStorage para su uso "
        "en solicitudes posteriores."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  7. SISTEMA DE ROLES Y PERMISOS
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "7. Sistema de Roles y Permisos", level=1)

    apa_heading(doc, "7.1 Estructura de Datos", level=2)
    apa_paragraph(doc, (
        "El sistema de roles y permisos se implementó con tres tablas: roles (id, nombre), "
        "permisos (id, nombre, descripcion), y roles_permisos (id_rol, id_permiso) como tabla "
        "pivote para la relación muchos a muchos. Se definieron 6 roles y 33 permisos granulares "
        "con nomenclatura modulo.accion (ej: activos.listar, contratos.crear)."
    ))

    apa_heading(doc, "7.2 Middleware de Autorización", level=2)
    apa_paragraph(doc, (
        "Se implementaron dos middlewares: get_current_user, que valida el token JWT y retorna "
        "el objeto usuario; y require_role(*roles), que verifica que el usuario autenticado "
        "pertenezca a uno de los roles especificados. Ambos se integran mediante inyección de "
        "dependencias de FastAPI (Depends)."
    ))

    apa_heading(doc, "7.3 Asignación de Permisos por Rol", level=2)

    perm_data = [
        ("Administrador", "Todos los permisos (33)", "Acceso total al sistema"),
        ("Gerente", "contratos.*, clientes.*, reportes.crear, activos.listar, pagos.*, dashboard.ver", "Gestión comercial y supervisión"),
        ("Almacén", "activos.*, categorias.*, asignaciones.*, reportes.listar, dashboard.ver", "Gestión de inventario y asignaciones"),
        ("Técnico", "reportes.*, mantenimientos.*, activos.listar, asignaciones.listar, dashboard.ver", "Soporte técnico y mantenimiento"),
        ("Operador", "contratos.listar, contratos.crear, clientes.listar, reportes.*, activos.listar, pagos.listar, dashboard.ver", "Operaciones diarias"),
        ("Cliente", "Ninguno (sin permisos)", "Acceso restringido a visualización propia"),
    ]

    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, text in enumerate(["Rol", "Permisos asignados", "Alcance"]):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(9)
        run.bold = True
        set_cell_shading(cell, "2B579A")
        run.font.color.rgb = RGBColor(255, 255, 255)

    for rol, perms, alc in perm_data:
        add_table_row(table, [rol, perms, alc])

    # ════════════════════════════════════════════════════════════════════════════
    #  8. FRONTEND
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "8. Frontend", level=1)

    apa_heading(doc, "8.1 Arquitectura", level=2)
    apa_paragraph(doc, (
        "El frontend se desarrolló con React 19, TypeScript 6 y Vite 8, siguiendo una arquitectura "
        "basada en componentes. Cada módulo del backend tiene su correspondiente carpeta en pages/ "
        "con dos vistas: Lista (tabla con DataTable genérica) y Formulario (creación/edición). "
        "La capa de API se organiza en archivos separados por recurso en src/api/, y la autenticación "
        "se maneja mediante un AuthContext que almacena el token JWT en localStorage."
    ))

    apa_heading(doc, "8.2 Componentes Principales", level=2)
    apa_paragraph(doc, (
        "El frontend incorpora los siguientes componentes desarrollados por el equipo:"
    ))
    apa_paragraph(doc, (
        "• SearchableSelect: Componente de selección con búsqueda textual que permite a los usuarios "
        "buscar y seleccionar registros relacionados (categorías, clientes, activos) sin necesidad de "
        "recordar IDs numéricos. Se conecta a los endpoints de listado del backend y filtra en tiempo real."
    ))
    apa_paragraph(doc, (
        "• FormSection: Componente de agrupación visual que organiza los campos del formulario en "
        "secciones con título y grid responsivo, mejorando la legibilidad de formularios extensos."
    ))
    apa_paragraph(doc, (
        "• MapPicker: Componente de mapa interactivo basado en Leaflet y react-leaflet que permite "
        "seleccionar coordenadas geográficas mediante un marcador arrastrable. El marcador utiliza "
        "un icono rojo personalizado (L.divIcon) similar al de Google Maps. El centro predeterminado "
        "es Santa Cruz de la Sierra, Bolivia (-17.8, -63.19)."
    ))
    apa_paragraph(doc, (
        "• CameraCapture: Componente que permite capturar fotografías directamente desde la cámara "
        "web del dispositivo o subir archivos de imagen, con previsualización antes de enviar."
    ))
    apa_paragraph(doc, (
        "• DataTable: Tabla genérica con soporte para ordenamiento, skeleton loader, badges de estado "
        "y acciones por fila (editar, eliminar)."
    ))
    apa_paragraph(doc, (
        "• Dashboard: Panel principal con bento-grid que muestra estadísticas, gráficos circulares "
        "(PieChart) de activos por estado y gráficos de barras (BarChart) de contratos por estado, "
        "mantenimientos pendientes e incidencias recientes, utilizando Recharts."
    ))

    apa_heading(doc, "8.3 Capturas del Frontend", level=2)

    add_screenshot(doc, "dashboard.png", width=Inches(5.2),
                   caption="Dashboard principal con resumen de indicadores y gráficos Recharts.")

    apa_paragraph(doc, (
        "La Figura 3 muestra el Dashboard principal con el bento-grid que incluye estadísticas "
        "numéricas (usuarios activos, clientes activos, activos en uso, contratos activos), "
        "gráficos de contratos y activos por estado, mantenimientos pendientes, incidencias "
        "recientes y accesos rápidos."
    ))

    add_screenshot(doc, "activos_lista.png", width=Inches(5.2),
                   caption="Lista de activos con DataTable, badges de estado y acciones.")

    apa_paragraph(doc, (
        "La Figura 4 presenta la lista de activos con 20 registros, mostrando columnas de ID, "
        "código de inventario, modelo, categoría, estado (con badges de colores), número de serie "
        "y acciones de edición/eliminación."
    ))

    add_screenshot(doc, "activos_formulario.png", width=Inches(5.2),
                   caption="Formulario de activos con SearchableSelect, MapPicker y campos de información general.")

    apa_paragraph(doc, (
        "La Figura 5 muestra el formulario de creación de activos con tres secciones: Información "
        "General (código, modelo, serie, categoría, estado, valor, fecha de compra), y Ubicación "
        "(MapPicker con Leaflet). El SearchableSelect permite buscar categorías por nombre."
    ))

    add_screenshot(doc, "asignaciones_formulario.png", width=Inches(5.2),
                   caption="Formulario de asignaciones con MapPicker para capturar ubicación GPS.")

    apa_paragraph(doc, (
        "La Figura 6 presenta el formulario de asignaciones que ahora incluye el MapPicker para "
        "capturar la ubicación exacta donde se entrega el activo, junto con los campos de activo, "
        "usuario, fechas y motivo."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  9. CONTROL DE VERSIONES GITHUB
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "9. Control de Versiones GitHub", level=1)

    apa_paragraph(doc, (
        "El control de versiones se realizó con Git y GitHub, manteniendo dos ramas principales: "
        "main (producción estable) y develop (integración de funcionalidades). Se realizaron 13 "
        "commits con mensajes semántsiguiendo la convención Conventional Commits (feat, fix, refactor). "
        "El repositorio incluye un README.md con instrucciones de instalación y uso."
    ))

    apa_heading(doc, "9.1 Historial de Commits", level=2)

    commits = [
        ("74cab5d", "init", "Estructura inicial backend (FastAPI) + frontend (React) + BD (MySQL)"),
        ("544c1ba", "feat", "Seed de roles y administrador por defecto"),
        ("d8f0bbf", "feat", "Middleware JWT y schemas de autenticación"),
        ("29614e3", "feat", "CRUD de roles, permisos, categorías y clientes"),
        ("8e1b3fc", "feat", "CRUD completo de activos, contratos, pagos, asignaciones, etc."),
        ("509a678", "feat", "Datos de prueba realistas (10 clientes, 20 activos, contratos, pagos)"),
        ("88212bf", "feat", "Frontend completo con tema oscuro, CRUDs, autenticación y dashboard"),
        ("d2ac825", "feat", "Roles Gerente/Almacén/Técnico, MapPicker Leaflet, gráficas Dashboard"),
        ("2be06f8", "feat", "Lucide icons, Button component, Toast/ConfirmDialog, CSS variables"),
        ("a37af87", "feat", "CRUD backend+frontend para rol, pago, historial_ubicacion, checklist"),
        ("fbcee27", "feat", "Fotos para activos (webcam + upload) con almacenamiento local"),
        ("ee82b2f", "refactor", "SearchableSelect, FormSection, Button, fix bug edición activos"),
        ("d799c8e", "fix+feat", "Categoria_nombre, ruta fotos, centro mapa + MapPicker en Asignaciones"),
    ]

    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, text in enumerate(["Hash", "Tipo", "Descripción"]):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(9)
        run.bold = True
        set_cell_shading(cell, "2B579A")
        run.font.color.rgb = RGBColor(255, 255, 255)

    for h, t, d in commits:
        add_table_row(table, [h[:7], t, d])

    add_screenshot(doc, "github_repo.png", width=Inches(5.2),
                   caption="Repositorio GitHub del proyecto SIGTAR con ramas main/develop.")

    apa_paragraph(doc, (
        "La Figura 7 muestra el repositorio en GitHub con las dos ramas (main y develop) y el "
        "historial de commits semánticos. El README documenta el stack tecnológico, la estructura "
        "del proyecto y las instrucciones de ejecución."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  10. SPRINT REVIEW
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "10. Sprint Review", level=1)

    apa_paragraph(doc, (
        "La Sprint Review se realizó al finalizar el Sprint 1 con una demo de 10 minutos que "
        "incluyó los siguientes escenarios:"
    ))

    apa_paragraph(doc, (
        "1. Creación de usuario: Demostración del registro de un nuevo usuario a través del "
        "endpoint POST /api/v1/auth/register y del formulario de creación de usuarios en el frontend."
    ))
    apa_paragraph(doc, (
        "2. Inicio de sesión: Login con credenciales válidas (admin@tecnorenta.com / admin123) "
        "y generación del token JWT. Verificación del endpoint GET /api/v1/auth/me con el token."
    ))
    apa_paragraph(doc, (
        "3. Acceso según rol: Prueba del middleware require_role() con diferentes roles "
        "(Administrador acceso total, Gerente acceso a contratos y clientes, Cliente sin permisos)."
    ))
    apa_paragraph(doc, (
        "4. Token en API Client: Demostración del flujo completo usando Swagger UI (/docs) y "
        "Thunder Client, mostrando el encabezado Authorization: Bearer <token>."
    ))
    apa_paragraph(doc, (
        "5. CRUD de activos: Creación, listado, edición y eliminación de activos con el "
        "formulario que incluye SearchableSelect para categorías, MapPicker para ubicación "
        "y CameraCapture para fotos."
    ))

    apa_heading(doc, "10.1 Sprint Backlog vs. Completado", level=2)

    backlog = [
        ("US-01", "Inicio de sesión seguro (Must, 3 SP)", "Completado", "Login JWT funcional"),
        ("US-02", "Gestión de usuarios y roles (Must, 5 SP)", "Completado", "CRUD usuarios + 6 roles + 33 permisos"),
        ("US-03", "Registro de activo (Must, 5 SP)", "Completado", "CRUD activos con categorías, fotos y mapa"),
        ("US-04", "Actualizar estado activo (Must, 3 SP)", "Completado", "PATCH estado + badges frontend"),
        ("US-05", "Gestión de categorías (Should, 3 SP)", "Completado", "CRUD categorías jerárquicas"),
        ("US-06", "Búsqueda y filtros activos (Should, 3 SP)", "Completado", "Lista con columnas y datos"),
    ]

    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, text in enumerate(["ID", "Historia de Usuario", "Estado", "Resultado"]):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(9)
        run.bold = True
        set_cell_shading(cell, "2B579A")
        run.font.color.rgb = RGBColor(255, 255, 255)

    for hid, hu, est, res in backlog:
        add_table_row(table, [hid, hu, est, res])

    # ════════════════════════════════════════════════════════════════════════════
    #  11. RETROSPECTIVA
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "11. Retrospectiva (Start/Stop/Continue)", level=1)

    apa_paragraph(doc, (
        "Al finalizar el Sprint 1, el equipo realizó una reunión retrospectiva siguiendo la "
        "dinámica Start/Stop/Continue para identificar oportunidades de mejora. Los resultados "
        "se documentan en la siguiente tabla:"
    ))

    retro_data = [
        ("Start (Empezar a hacer)",
         "• Escribir pruebas unitarias antes del código (TDD)\n• Realizar Daily Scrum de 5 minutos\n• Documentar decisiones técnicas en ADRs",
         "Mejorar la calidad del código y la comunicación del equipo"),
        ("Stop (Dejar de hacer)",
         "• Trabajar en múltiples tareas sin terminar una\n• Hacer commits sin probar el build\n• Pasar más de 2 días sin hacer push",
         "Reducir el multitasking y mejorar la disciplina de versionado"),
        ("Continue (Seguir haciendo)",
         "• Arquitectura modular en capas (Router → Service → Repository → Model)\n• Commits semánticos con Conventional Commits\n• Integración de componentes visuales de alta calidad (Leaflet, Recharts)\n• Código en español alineado con el dominio del negocio",
         "Mantener las buenas prácticas que garantizan calidad y productividad"),
    ]

    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, text in enumerate(["Categoría", "Acciones", "Objetivo"]):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(9)
        run.bold = True
        set_cell_shading(cell, "2B579A")
        run.font.color.rgb = RGBColor(255, 255, 255)

    for cat, acc, obj in retro_data:
        add_table_row(table, [cat, acc, obj])

    # ════════════════════════════════════════════════════════════════════════════
    #  12. CONCLUSIONES
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "12. Conclusiones", level=1)

    apa_paragraph(doc, (
        "1. El Sprint 1 cumplió satisfactoriamente su objetivo de construir el núcleo técnico "
        "del sistema SIGTAR, incluyendo una base de datos relacional normalizada en 3FN con 15 "
        "tablas, 117 registros de prueba latinoamericanos, y un módulo de autenticación JWT "
        "completo con registro, login y recuperación de contraseña."
    ))
    apa_paragraph(doc, (
        "2. El sistema de roles y permisos con 6 roles y 33 permisos granulares, implementado "
        "mediante middlewares de autorización en FastAPI, proporciona un control de acceso "
        "robusto y flexible que se adapta a la estructura organizativa de TecnoRenta Oriente S.R.L."
    ))
    apa_paragraph(doc, (
        "3. El frontend React 19 con TypeScript ofrece una experiencia de usuario moderna con "
        "tema oscuro, componentes reutilizables (DataTable, SearchableSelect, FormSection, "
        "MapPicker, CameraCapture), y dashboards interactivos con gráficos Recharts."
    ))
    apa_paragraph(doc, (
        "4. El control de versiones en GitHub con 13 commits semánticos y dos ramas (main + "
        "develop) garantiza la trazabilidad del desarrollo y facilita la integración continua."
    ))
    apa_paragraph(doc, (
        "5. La contribución a los ODS 8, 9 y 12 se materializa en la digitalización de procesos "
        "manuales, la innovación tecnológica aplicada a una PYME boliviana, y la extensión de la "
        "vida útil de los activos mediante trazabilidad y mantenimiento preventivo."
    ))
    apa_paragraph(doc, (
        "6. Como trabajo futuro, el equipo planea implementar pruebas automatizadas, migrar el "
        "almacenamiento de fotos a Cloudinary para producción, y continuar con el Sprint 2 "
        "enfocado en contratos, trazabilidad y alertas de vencimiento."
    ))

    # ════════════════════════════════════════════════════════════════════════════
    #  REFERENCIAS (APA 7)
    # ════════════════════════════════════════════════════════════════════════════
    apa_heading(doc, "Referencias", level=1)

    refs = [
        "Codd, E. F. (1970). A relational model of data for large shared data banks. Communications of the ACM, 13(6), 377–387. https://doi.org/10.1145/362384.362685",
        "Date, C. J. (2004). An introduction to database systems (8th ed.). Addison-Wesley.",
        "Jones, M., Bradley, J., & Sakimura, N. (2015). JSON Web Token (JWT). RFC 7519. Internet Engineering Task Force. https://datatracker.ietf.org/doc/html/rfc7519",
        "Laudon, K. C., & Laudon, J. P. (2020). Management information systems: Managing the digital firm (16th ed.). Pearson.",
        "Provos, N., & Mazières, D. (1999). A future-adaptable password scheme. Proceedings of the 1999 USENIX Annual Technical Conference, 81–92.",
        "Schwaber, K., & Sutherland, J. (2020). The Scrum Guide: The definitive guide to Scrum: The rules of the game. https://scrumguides.org/scrum-guide.html",
        "Power, D. J. (2002). Decision support systems: Concepts and resources for managers. Quorum Books.",
        "Forsgren, N., Humble, J., & Kim, G. (2018). Accelerate: The science of lean software and DevOps: Building and scaling high performing technology organizations. IT Revolution Press.",
    ]

    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.left_indent = Cm(1.27)
        p.paragraph_format.line_spacing = 2.0
        # Hanging indent: first line at 0, rest indented
        fmt = p.paragraph_format
        fmt.first_line_indent = Cm(-1.27)
        fmt.left_indent = Cm(1.27)
        run = p.add_run(ref)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)

    # ── Save ──
    doc.save(OUTPUT_FILE)
    print(f"Documento generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_document()
