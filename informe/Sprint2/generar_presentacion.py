from pptx import Presentation
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

SNAPSHOTS_DIR = os.path.join(os.path.dirname(__file__), "capturas")

# Colors
DARK_BLUE = RGBColor(0x1B, 0x2A, 0x4A)
ACCENT_BLUE = RGBColor(0x2F, 0x54, 0x96)
ACCENT_GOLD = RGBColor(0xD4, 0xA0, 0x1E)
TEXT_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_DARK = RGBColor(0x1A, 0x1A, 0x2E)
TEXT_GRAY = RGBColor(0x4A, 0x4A, 0x6A)
BG_LIGHT = RGBColor(0xF5, 0xF5, 0xFA)
BG_CARD = RGBColor(0xE8, 0xEC, 0xF4)
ACCENT_RED = RGBColor(0xC0, 0x39, 0x2B)
ACCENT_GREEN = RGBColor(0x27, 0xAE, 0x60)
ACCENT_ORANGE = RGBColor(0xE6, 0x7E, 0x22)
LIGHT_BLUE = RGBColor(0xDB, 0xE6, 0xF5)

SPRINT_GOAL_TEXT = "Sprint Goal: Construir un sistema web funcional para la gestión y trazabilidad de activos rentados"

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

def add_sprint_goal_bar(slide):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, Inches(0.5)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_GOLD
    bar.line.fill.background()
    tf = bar.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = f"  {SPRINT_GOAL_TEXT}"
    run.font.size = Pt(11)
    run.font.color.rgb = TEXT_DARK
    run.font.bold = True
    run.font.name = 'Calibri'

def add_bottom_bar(slide):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.2), prs.slide_width, Inches(0.3)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_BLUE
    bar.line.fill.background()

def add_title_text(slide, text, top=Inches(0.7), left=Inches(0.6), width=Inches(12), size=28, color=DARK_BLUE, bold=True):
    txBox = slide.shapes.add_textbox(left, top, width, Inches(0.7))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = 'Calibri'
    return txBox

def add_body_text(slide, text, top=Inches(1.5), left=Inches(0.8), width=Inches(11.5), size=16, color=TEXT_DARK, bold=False):
    txBox = slide.shapes.add_textbox(left, top, width, Inches(4.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = 'Calibri'
    return txBox

def add_bullet_text(slide, items, top=Inches(1.6), left=Inches(1), width=Inches(11), size=15, color=TEXT_DARK):
    txBox = slide.shapes.add_textbox(left, top, width, Inches(5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(8)
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = f"  {item}"
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.name = 'Calibri'
    return txBox

def add_bullet_text_rich(slide, items, top=Inches(1.6), left=Inches(1), width=Inches(11), size=15):
    txBox = slide.shapes.add_textbox(left, top, width, Inches(5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if isinstance(item, tuple):
            bold_text, normal_text = item
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.space_after = Pt(10)
            run1 = p.add_run()
            run1.text = f"  {bold_text}"
            run1.font.size = Pt(size)
            run1.font.color.rgb = DARK_BLUE
            run1.font.bold = True
            run1.font.name = 'Calibri'
            run2 = p.add_run()
            run2.text = normal_text
            run2.font.size = Pt(size)
            run2.font.color.rgb = TEXT_DARK
            run2.font.name = 'Calibri'
        else:
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.space_after = Pt(10)
            run = p.add_run()
            run.text = f"  {item}"
            run.font.size = Pt(size)
            run.font.color.rgb = TEXT_DARK
            run.font.name = 'Calibri'
    return txBox

def add_card(slide, text, top, left, width, height, fill_color=BG_CARD, text_color=TEXT_DARK, size=14, bold=False, align=PP_ALIGN.CENTER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = align
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = text_color
    run.font.bold = bold
    run.font.name = 'Calibri'
    return shape

def add_image_centered(slide, img_path, top, width=Inches(5)):
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, (prs.slide_width - width) / 2, top, width=width)
        return True
    return False

def add_image_left(slide, img_path, top, left, width=Inches(4.5)):
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, left, top, width=width)
        return True
    return False

def add_accent_line(slide, top=Inches(1.3)):
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.6), top, Inches(2), Inches(0.05)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_GOLD
    line.line.fill.background()

def new_slide():
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    add_sprint_goal_bar(slide)
    add_bottom_bar(slide)
    return slide


# ======================== SLIDE 1: PORTADA ========================
slide = new_slide()

bar_top = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(0), Inches(0.5), prs.slide_width, Inches(2.5)
)
bar_top.fill.solid()
bar_top.fill.fore_color.rgb = DARK_BLUE
bar_top.line.fill.background()

add_title_text(slide, "SIGTAR", top=Inches(0.7), left=Inches(0.8), size=44, color=TEXT_WHITE)
add_body_text(slide, "Sistema de Gestión y Trazabilidad de Activos Rentados", top=Inches(1.4), left=Inches(0.8), size=20, color=TEXT_WHITE)
add_body_text(slide, "Tecnorenta", top=Inches(1.9), left=Inches(0.8), size=16, color=ACCENT_GOLD)

add_body_text(slide, "Informe Técnico — Sprint 1 & 2", top=Inches(3.5), left=Inches(0.8), size=22, color=DARK_BLUE, bold=True)
add_accent_line(slide, top=Inches(4.0))

info_items = [
    "Asignatura: Programación de Sistemas II",
    "Docente: Ing. Juan Pérez López",
    "",
    "Estudiantes: Estudiante 1 • Estudiante 2 • Estudiante 3 • Estudiante 4",
    "2026"
]
add_bullet_text(slide, info_items, top=Inches(4.2), left=Inches(0.8), size=14, color=TEXT_GRAY)


# ======================== SLIDE 2: SPRINT GOAL GENERAL ========================
slide = new_slide()

add_title_text(slide, "Sprint Goal General", top=Inches(0.9), size=32)
add_accent_line(slide, top=Inches(1.5))

goal_box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(2.2), Inches(11.3), Inches(2.5)
)
goal_box.fill.solid()
goal_box.fill.fore_color.rgb = LIGHT_BLUE
goal_box.line.fill.background()

tf = goal_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "Construir un sistema web funcional para la gestión y trazabilidad de activos rentados, desde la base de datos hasta la interfaz de usuario, aplicando metodología Scrum."
run.font.size = Pt(20)
run.font.color.rgb = DARK_BLUE
run.font.bold = True
run.font.name = 'Calibri'

add_body_text(slide, "Metodología: Scrum  |  Duración: 2 Sprints (6 semanas)  |  Equipo: 4 desarrolladores",
              top=Inches(5.2), left=Inches(1), size=14, color=TEXT_GRAY)


# ======================== SLIDE 3: SPRINT 1 - GOAL ========================
slide = new_slide()

add_title_text(slide, "Sprint 1 — Goal", top=Inches(0.9), size=32)
add_accent_line(slide)

add_body_text(slide, "Establecer la base del sistema: autenticación, base de datos, API base y frontend inicial.",
              top=Inches(1.8), size=18, color=TEXT_GRAY)

items = [
    ("Base de Datos: ", "11 tablas modeladas con SQLAlchemy 2.0, migraciones con Alembic, datos de prueba"),
    ("Autenticación: ", "JWT + bcrypt, registro y login de usuarios, control de roles"),
    ("API Base: ", "FastAPI con 15 routers, documentación Swagger automática"),
    ("Frontend Inicial: ", "React 19 + TypeScript, layout con sidebar, contexto de autenticación"),
    ("Arquitectura: ", "3 capas: Router → Service → Repository → Model"),
]
add_bullet_text_rich(slide, items, top=Inches(2.6), size=16)


# ======================== SLIDE 4: ¿POR QUÉ ESTAS TECNOLOGÍAS? ========================
slide = new_slide()

add_title_text(slide, "Stack Tecnológico — ¿Por qué cada tecnología?", top=Inches(0.9), size=30)
add_accent_line(slide)

techs = [
    ("FastAPI", "Framework Python de alto rendimiento. Validación automática con Pydantic y documentación Swagger generada sola. Lo elegimos porque acelera el desarrollo y elimina errores de tipos.", ACCENT_BLUE),
    ("Python", "Lenguaje de curva de aprendizaje baja, enorme ecosistema para APIs y ciencia de datos. Elegido porque permite a equipos pequeños producir resultados rápido.", ACCENT_GREEN),
    ("React 19", "Biblioteca de componentes reutilizables con Virtual DOM. Lo elegimos porque el frontend se construye como piezas independientes que se actualizan sin recargar la página.", ACCENT_ORANGE),
    ("MySQL + SQLAlchemy", "MySQL: motor relacional confiable, transaccional (ACID). SQLAlchemy 2.0: ORM que convierte tablas SQL en objetos Python. Permite cambiar de BD sin modificar código.", ACCENT_RED),
]

for i, (name, desc, color) in enumerate(techs):
    top = Inches(1.6 + i * 1.35)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.15))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(0xF0, 0xF4, 0xF8)
    card.line.fill.background()
    
    # Color indicator bar
    indicator = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top, Inches(0.12), Inches(1.15))
    indicator.fill.solid()
    indicator.fill.fore_color.rgb = color
    indicator.line.fill.background()
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = f"  {name}"
    run.font.size = Pt(18)
    run.font.color.rgb = DARK_BLUE
    run.font.bold = True
    run.font.name = 'Calibri'
    
    p2 = tf.add_paragraph()
    run2 = p2.add_run()
    run2.text = f"     {desc}"
    run2.font.size = Pt(13)
    run2.font.color.rgb = TEXT_GRAY
    run2.font.name = 'Calibri'


# ======================== SLIDE 5: ARQUITECTURA 3 CAPAS ========================
slide = new_slide()

add_title_text(slide, "Arquitectura — ¿Por qué 3 capas?", top=Inches(0.9), size=30)
add_accent_line(slide)

add_body_text(slide, "Separación estricta de responsabilidades: cada capa hace solo una cosa",
              top=Inches(1.6), size=16, color=TEXT_GRAY)

# Architecture layers as cards
layers = [
    ("Router", "Recibe peticiones HTTP, valida parámetros, delega al Service", ACCENT_BLUE),
    ("Service", "Lógica de negocio, reglas, coordinación entre repositorios", ACCENT_GREEN),
    ("Repository", "Consultas a la base de datos, CRUD, filtros", ACCENT_ORANGE),
    ("Model", "Define tablas, relaciones, enums, tipos de datos", ACCENT_RED),
]

# Arrow connectors
for i, (name, desc, color) in enumerate(layers):
    top = Inches(2.3 + i * 1.15)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), top, Inches(10.3), Inches(0.95))
    card.fill.solid()
    card.fill.fore_color.rgb = color
    card.line.fill.background()
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = f"  {name}"
    run.font.size = Pt(18)
    run.font.color.rgb = TEXT_WHITE
    run.font.bold = True
    run.font.name = 'Calibri'
    p2 = tf.add_paragraph()
    run2 = p2.add_run()
    run2.text = f"  {desc}"
    run2.font.size = Pt(12)
    run2.font.color.rgb = TEXT_WHITE
    run2.font.name = 'Calibri'

reasons = [
    "Mantenible: cambios en una capa no afectan las otras",
    "Testable: cada capa se prueba por separado",
    "Escalable: cada capa puede escalar independientemente",
]
add_bullet_text(slide, reasons, top=Inches(6.0), left=Inches(1.5), size=13, color=TEXT_GRAY)


# ======================== SLIDE 6: SPRINT 1 - BASE DE DATOS ========================
slide = new_slide()

add_title_text(slide, "Sprint 1 — Base de Datos", top=Inches(0.9), size=30)
add_accent_line(slide)

db_info = [
    "11 tablas: usuarios, roles, clientes, activos, categorías, contratos, pagos, asignaciones, reportes, mantenimientos, checklist",
    "Relaciones: 1 a muchos (cliente → contratos), muchos a muchos (roles ↔ permisos), herencia (mantenimiento → preventivo/correctivo)",
    "Enums fijos: estado_activo, estado_contrato, estado_pago, gravedad_incidencia — sin strings libres",
    "Auditoría: creado_por, fecha_creacion, modificado_por, fecha_modificacion en tablas críticas",
    "Migraciones: 4 migraciones Alembic (schema inicial, lat/long, fotos, documentos)",
]
add_bullet_text(slide, db_info, top=Inches(1.7), left=Inches(0.8), size=14)

add_image_centered(slide, os.path.join(SNAPSHOTS_DIR, "der_diagram.jpeg"), top=Inches(4.0), width=Inches(8))


# ======================== SLIDE 7: SPRINT 2 - GOAL ========================
slide = new_slide()

add_title_text(slide, "Sprint 2 — Goal", top=Inches(0.9), size=32)
add_accent_line(slide)

add_body_text(slide, "Implementar todos los módulos CRUD del negocio, dashboard gerencial con KPIs, consultas SQL complejas y documentación de API.",
              top=Inches(1.8), size=18, color=TEXT_GRAY)

items = [
    ("12 módulos CRUD: ", "usuarios, roles, clientes, activos, categorías, contratos, pagos, asignaciones, reportes, mantenimientos, historial, checklist"),
    ("Dashboard gerencial: ", "7 KPIs, 2 gráficos (barras + pastel), alertas de contratos próximos a vencer"),
    ("6 consultas SQL complejas: ", "GROUP BY, JOINs, COUNT, SUM, subconsultas con fechas"),
    ("API documentada: ", "Swagger UI con 45 endpoints, colección importable a Postman"),
    ("Mapa + Fotos: ", "Leaflet para ubicación GPS, cámara/archivo para fotos de activos"),
]
add_bullet_text_rich(slide, items, top=Inches(2.6), size=16)


# ======================== SLIDE 8: 12 MÓDULOS CRUD ========================
slide = new_slide()

add_title_text(slide, "Sprint 2 — 12 Módulos CRUD", top=Inches(0.9), size=30)
add_accent_line(slide)

modules_data = [
    ("1. Usuarios", "JWT + bcrypt, roles", "7. Pagos", "Filtros vencidos/próximos"),
    ("2. Roles", "Permisos asignables", "8. Asignaciones", "Activo ↔ Contrato + mapa"),
    ("3. Clientes", "NIT, dirección, mapa", "9. Reportes", "Gravedad, estado, foto"),
    ("4. Activos", "CSV, fotos, mapa GPS", "10. Mantenimiento", "Preventivo / Correctivo"),
    ("5. Categorías", "Jerarquía padre-hijo", "11. Historial", "Ubicación GPS por asignación"),
    ("6. Contratos", "Documento adjunto", "12. Checklist", "Componentes entrega/devolución"),
]

for i, (a, b, c, d) in enumerate(modules_data):
    row = i // 2
    col = i % 2
    left = Inches(0.8 + col * 6.2)
    top = Inches(1.6 + row * 0.85)
    
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.8), Inches(0.7))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_BLUE if i % 2 == 0 else BG_CARD
    card.line.fill.background()
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = f"  {a}  —  {b}"
    run.font.size = Pt(13)
    run.font.color.rgb = DARK_BLUE
    run.font.bold = True
    run.font.name = 'Calibri'

add_image_left(slide, os.path.join(SNAPSHOTS_DIR, "activos_lista.png"), top=Inches(4.5), left=Inches(0.8), width=Inches(5.5))
add_image_left(slide, os.path.join(SNAPSHOTS_DIR, "contratos_lista.png"), top=Inches(4.5), left=Inches(6.8), width=Inches(5.5))

# ======================== SLIDE 9: DASHBOARD ========================
slide = new_slide()

add_title_text(slide, "Sprint 2 — Dashboard Gerencial", top=Inches(0.9), size=30)
add_accent_line(slide)

kpis = [
    ("Usuarios", "Clientes", "Activos", "Contratos"),
    ("Ingresos/mes", "Próx. vencer", "Incidencias", "Pagos vencidos"),
]
for row_idx, row_data in enumerate(kpis):
    for col_idx, kpi in enumerate(row_data):
        left = Inches(0.6 + col_idx * 3.1)
        top = Inches(1.6 + row_idx * 0.8)
        add_card(slide, kpi, top, left, Inches(2.8), Inches(0.6), 
                 fill_color=ACCENT_BLUE if row_idx == 0 else BG_CARD,
                 text_color=TEXT_WHITE if row_idx == 0 else TEXT_DARK,
                 size=14, bold=True)

add_image_centered(slide, os.path.join(SNAPSHOTS_DIR, "dashboard.png"), top=Inches(3.4), width=Inches(12))

# ======================== SLIDE 10: CONSULTAS SQL ========================
slide = new_slide()

add_title_text(slide, "Sprint 2 — 6 Consultas SQL Complejas", top=Inches(0.9), size=30)
add_accent_line(slide)

sqls = [
    ("Activos por estado", "GROUP BY → conteo por categoría"),
    ("Contratos por estado", "GROUP BY → distribución"),
    ("Próximos a vencer", "WHERE fecha_fin BETWEEN hoy AND hoy+30"),
    ("Ingresos mensuales", "SUM(monto_mensual) WHERE activo"),
    ("Contratos + Cliente", "JOIN para datos completos"),
    ("Incidencias abiertas", "COUNT WHERE estado != cerrado"),
]

for i, (title, desc) in enumerate(sqls):
    col = i % 3
    row = i // 3
    left = Inches(0.6 + col * 4.1)
    top = Inches(1.6 + row * 1.6)
    
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.8), Inches(1.3))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_BLUE
    card.line.fill.background()
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = title
    run.font.size = Pt(16)
    run.font.color.rgb = DARK_BLUE
    run.font.bold = True
    run.font.name = 'Calibri'
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = desc
    run2.font.size = Pt(12)
    run2.font.color.rgb = TEXT_GRAY
    run2.font.name = 'Calibri'

add_body_text(slide, "Todas implementadas con SQLAlchemy ORM + funciones de agregación de MySQL",
              top=Inches(5.2), left=Inches(0.8), size=14, color=TEXT_GRAY)


# ======================== SLIDE 11: SWAGGER ========================
slide = new_slide()

add_title_text(slide, "Sprint 2 — Documentación de API", top=Inches(0.9), size=30)
add_accent_line(slide)

add_body_text(slide, "Swagger UI — Documentación interactiva generada automáticamente por FastAPI",
              top=Inches(1.6), size=16, color=TEXT_GRAY)

swagger_info = [
    "45 endpoints documentados con schemas de request/response",
    "Pruebas interactivas desde el navegador en /docs",
    "Exportable a Postman: File → Import → tecnorenta_openapi.json",
    "Cobertura: Auth, Usuarios, Roles, Activos, Contratos, Pagos, Dashboard + más",
]
add_bullet_text(slide, swagger_info, top=Inches(2.2), left=Inches(0.8), size=14)

add_image_centered(slide, os.path.join(SNAPSHOTS_DIR, "swagger_docs.png"), top=Inches(4.3), width=Inches(10))


# ======================== SLIDE 12: SCRUM ========================
slide = new_slide()

add_title_text(slide, "Scrum — Organización del Trabajo", top=Inches(0.9), size=30)
add_accent_line(slide)

# Roles
roles_data = [
    ("Product Owner", "Define prioridades y valida entregables"),
    ("Scrum Master", "Facilita ceremonias y elimina bloqueos"),
    ("Dev Team (4)", "Desarrolla los incrementos del producto"),
]
for i, (role, desc) in enumerate(roles_data):
    left = Inches(0.6 + i * 4.1)
    top = Inches(1.6)
    add_card(slide, f"{role}\n{desc}", top, left, Inches(3.8), Inches(1.0),
             fill_color=ACCENT_BLUE, text_color=TEXT_WHITE, size=13, bold=True)

# Ceremonies
cerm = [
    "Sprint Planning: definición de objetivos y tareas del sprint",
    "Daily Standup: reunión diaria de 15 min para sincronizar avances",
    "Sprint Review: presentación de resultados al Product Owner",
    "Retrospectiva: mejora continua (Start / Stop / Continue)",
]
add_bullet_text(slide, cerm, top=Inches(2.9), left=Inches(0.8), size=14)

add_image_centered(slide, os.path.join(SNAPSHOTS_DIR, "burndown_chart.png"), top=Inches(4.3), width=Inches(6))


# ======================== SLIDE 13: SPRINT 3 ========================
slide = new_slide()

add_title_text(slide, "Sprint 3 — Lo que viene", top=Inches(0.8), size=32)
add_accent_line(slide)

goal_box3 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.0)
)
goal_box3.fill.solid()
goal_box3.fill.fore_color.rgb = ACCENT_GOLD
goal_box3.line.fill.background()
tf = goal_box3.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "Sprint Goal 3: Dashboard avanzado con 5+ KPIs gráficos, pruebas de integración (10+ casos) y preparación para despliegue."
run.font.size = Pt(18)
run.font.color.rgb = TEXT_DARK
run.font.bold = True
run.font.name = 'Calibri'

items_s3 = [
    ("Dashboard avanzado: ", "Nuevos KPIs gráficos con Recharts, filtros por rango de fechas, exportación de reportes"),
    ("Pruebas de integración: ", "10+ casos probando flujos completos (backend + frontend)"),
    ("Despliegue: ", "Preparación para producción: variables de entorno, CORS, build optimizado"),
    ("Mejoras: ", "Notificaciones de contratos próximos a vencer, optimización de consultas SQL"),
]
add_bullet_text_rich(slide, items_s3, top=Inches(3.0), size=16)


# ======================== SLIDE 14: SPRINT 2 - CAPTURAS ========================
slide = new_slide()

add_title_text(slide, "Sprint 2 — Sistema en Funcionamiento", top=Inches(0.9), size=28)
add_accent_line(slide)

imgs = [
    ("activos_lista.png", "activos_formulario.png"),
    ("pagos_lista.png", "asignaciones_lista.png"),
]

for row_idx, (img1, img2) in enumerate(imgs):
    top = Inches(1.6 + row_idx * 2.8)
    add_image_left(slide, os.path.join(SNAPSHOTS_DIR, img1), top=top, left=Inches(0.5), width=Inches(5.8))
    add_image_left(slide, os.path.join(SNAPSHOTS_DIR, img2), top=top, left=Inches(6.8), width=Inches(5.8))


# ======================== SLIDE 15: GRACIAS ========================
slide = new_slide()

bar_bottom = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(0), Inches(2.0), prs.slide_width, Inches(3.5)
)
bar_bottom.fill.solid()
bar_bottom.fill.fore_color.rgb = DARK_BLUE
bar_bottom.line.fill.background()

add_title_text(slide, "¿Preguntas?", top=Inches(2.5), left=Inches(0.8), size=44, color=TEXT_WHITE)
add_body_text(slide, "SIGTAR — Tecnorenta", top=Inches(3.5), left=Inches(0.8), size=18, color=ACCENT_GOLD)
add_body_text(slide, "Sprint 1 & 2 completados • Sprint 3 en marcha", top=Inches(4.0), left=Inches(0.8), size=14, color=RGBColor(0xAA, 0xBB, 0xDD))


# ======================== SAVE ========================
output_path = os.path.join(os.path.dirname(__file__), 'SIGTAR_Sprint1_Sprint2_Presentacion.pptx')
prs.save(output_path)
print(f"Presentación generada: {output_path}")
