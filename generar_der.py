"""Generate ER diagram for SIGTAR database and embed in a Word document."""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_IMG = os.path.join(os.path.dirname(__file__), "capturas", "der_diagram.png")
OUTPUT_DOCX = os.path.join(os.path.dirname(__file__), "SIGTAR_DER_Diagrama.docx")

# ─── Table definitions ───────────────────────────────────────────────────────

FONT_PATH = None  # use default

try:
    FONT_BOLD = ImageFont.truetype("arialbd.ttf", 14)
    FONT_NORMAL = ImageFont.truetype("arial.ttf", 11)
    FONT_SMALL = ImageFont.truetype("arial.ttf", 9)
except:
    FONT_BOLD = ImageFont.load_default()
    FONT_NORMAL = ImageFont.load_default()
    FONT_SMALL = ImageFont.load_default()

# Tables: (name, columns_display, x, y, width, height)
# Layout: grid of 3 cols x 5 rows
COL_W = 280
ROW_H = 130
START_X = 30
START_Y = 30
GAP_X = 40
GAP_Y = 30

tables_meta = {
    "roles": ["id (PK)", "nombre (UNIQUE)"],
    "permisos": ["id (PK)", "nombre (UNIQUE)", "descripcion"],
    "roles_permisos": ["id_rol (PK,FK)", "id_permiso (PK,FK)"],
    "usuarios": ["id (PK)", "email (UNIQUE)", "password_hash", "activo", "id_rol (FK)"],
    "categorias_activo": ["id (PK)", "nombre", "nivel", "id_categoria_padre (FK)"],
    "clientes": ["id (PK)", "razon_social", "nit (UNIQUE)", "direccion", "sector"],
    "activos": ["id (PK)", "codigo_inventario (UNIQUE)", "modelo", "numero_serie (UNIQUE)", "estado (ENUM)", "id_categoria (FK)", "latitud", "longitud"],
    "contratos": ["id (PK)", "fecha_inicio", "fecha_fin", "estado (ENUM)", "monto_mensual", "id_cliente (FK)"],
    "pagos": ["id (PK)", "id_contrato (FK)", "concepto", "monto", "fecha", "estado (ENUM)"],
    "asignaciones_activo": ["id (PK)", "fecha_asignacion", "fecha_devolucion", "latitud", "longitud", "id_contrato (FK)", "id_activo (FK)"],
    "historial_ubicacion": ["id (PK)", "id_asignacion (FK)", "latitud", "longitud", "timestamp"],
    "checklist_estado": ["id (PK)", "id_asignacion (FK)", "momento (ENUM)", "pantalla (ENUM)", "teclado (ENUM)", "carcasa (ENUM)", "cargador", "id_usuario (FK)"],
    "reportes_incidencia": ["id (PK)", "fecha", "descripcion", "gravedad (ENUM)", "estado (ENUM)", "id_activo (FK)"],
    "mantenimientos": ["id (PK)", "tipo (ENUM)", "fecha", "costo", "descripcion", "id_activo (FK)", "id_reporte_origen (FK)"],
    "activos_fotos": ["id (PK)", "id_activo (FK)", "url", "orden"],
}

# Grid positions: 3 cols, 5 rows
table_names = list(tables_meta.keys())
positions = {}
for idx, name in enumerate(table_names):
    col = idx % 3
    row = idx // 3
    x = START_X + col * (COL_W + GAP_X)
    y = START_Y + row * (ROW_H + GAP_Y)
    positions[name] = (x, y)

# ─── Relationships ──────────────────────────────────────────────────────────

relationships = [
    ("usuarios", "roles", "id_rol"),
    ("activos", "categorias_activo", "id_categoria"),
    ("contratos", "clientes", "id_cliente"),
    ("pagos", "contratos", "id_contrato"),
    ("asignaciones_activo", "contratos", "id_contrato"),
    ("asignaciones_activo", "activos", "id_activo"),
    ("historial_ubicacion", "asignaciones_activo", "id_asignacion"),
    ("checklist_estado", "asignaciones_activo", "id_asignacion"),
    ("checklist_estado", "usuarios", "id_usuario"),
    ("reportes_incidencia", "activos", "id_activo"),
    ("mantenimientos", "activos", "id_activo"),
    ("mantenimientos", "reportes_incidencia", "id_reporte_origen"),
    ("activos_fotos", "activos", "id_activo"),
]

# ─── Colors ──────────────────────────────────────────────────────────────────

BG = (15, 15, 15)           # dark background
HEADER_BG = (43, 87, 154)    # blue header
HEADER_FG = (255, 255, 255)
ROW_BG = (30, 30, 30)
ROW_ALT_BG = (38, 38, 38)
BORDER = (70, 130, 200)
LINE_COLOR = (200, 180, 80)  # gold lines
TEXT_FG = (220, 220, 220)
PK_FG = (255, 200, 80)      # gold for PK
FK_FG = (100, 200, 255)     # cyan for FK
TITLE_FG = (255, 255, 255)

# Group colors
COLOR_AUTH = (43, 87, 154)       # blue - auth
COLOR_INV = (34, 139, 34)        # green - inventory
COLOR_CONTRACT = (180, 100, 30)  # orange - contracts
COLOR_OPS = (130, 50, 160)       # purple - operations
COLOR_PHOTO = (70, 130, 180)     # steel blue - photos

group_colors = {
    "roles": COLOR_AUTH,
    "permisos": COLOR_AUTH,
    "roles_permisos": COLOR_AUTH,
    "usuarios": COLOR_AUTH,
    "categorias_activo": COLOR_INV,
    "activos": COLOR_INV,
    "clientes": COLOR_INV,
    "contratos": COLOR_CONTRACT,
    "pagos": COLOR_CONTRACT,
    "asignaciones_activo": COLOR_CONTRACT,
    "historial_ubicacion": COLOR_OPS,
    "checklist_estado": COLOR_OPS,
    "reportes_incidencia": COLOR_OPS,
    "mantenimientos": COLOR_OPS,
    "activos_fotos": COLOR_PHOTO,
}

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline or fill, width=width)

# ─── Create image ────────────────────────────────────────────────────────────

IMG_W = START_X * 2 + 3 * COL_W + 2 * GAP_X + 100
IMG_H = START_Y * 2 + 5 * ROW_H + 4 * GAP_Y + 80

img = Image.new("RGB", (IMG_W, IMG_H), BG)
draw = ImageDraw.Draw(img)

# ─── Title ───────────────────────────────────────────────────────────────────
title = "SIGTAR — Diagrama Entidad-Relación (Base de Datos MySQL)"
tw, th = draw.textbbox((0, 0), title, font=FONT_BOLD)[2:4]
draw.text(((IMG_W - tw) // 2, 8), title, fill=TITLE_FG, font=FONT_BOLD)

# ─── Draw tables ─────────────────────────────────────────────────────────────

for name, cols in tables_meta.items():
    x, y = positions[name]
    header_color = group_colors.get(name, HEADER_BG)
    row_h = 20

    # Calculate actual height needed
    n_rows = len(cols) + 1  # +1 for header
    box_h = n_rows * row_h + 6
    bw = COL_W - 10

    # Draw table background
    draw_rounded_rect(draw, (x, y, x + bw, y + box_h), radius=6, fill=ROW_BG, outline=header_color, width=2)

    # Draw header
    draw_rounded_rect(draw, (x + 2, y + 2, x + bw - 2, y + row_h + 2), radius=4, fill=header_color)
    draw.text((x + 8, y + 4), name.upper(), fill=HEADER_FG, font=FONT_BOLD)

    # Draw rows
    for i, col in enumerate(cols):
        ry = y + row_h + 4 + i * row_h
        if i % 2 == 0:
            draw.rectangle((x + 4, ry, x + bw - 4, ry + row_h), fill=ROW_BG)
        else:
            draw.rectangle((x + 4, ry, x + bw - 4, ry + row_h), fill=ROW_ALT_BG)

        # Color coding for PK and FK
        fg = TEXT_FG
        if "(PK)" in col:
            fg = PK_FG
        elif "(FK)" in col and "(PK)" not in col:
            fg = FK_FG

        draw.text((x + 8, ry + 2), col, fill=fg, font=FONT_NORMAL)

    # Draw border
    draw.rounded_rectangle((x, y, x + bw, y + box_h), radius=6, outline=header_color, width=2)

# ─── Draw relationship lines ─────────────────────────────────────────────────

for from_tab, to_tab, fk_col in relationships:
    fx, fy = positions[from_tab]
    tx, ty = positions[to_tab]

    # Calculate connection points (right side of from table, left side of to table)
    bw = COL_W - 10
    n_rows_from = len(tables_meta[from_tab]) + 1
    n_rows_to = len(tables_meta[to_tab]) + 1

    from_center_x = fx + bw
    from_center_y = fy + (n_rows_from * 20 + 6) // 2

    to_center_x = tx
    to_center_y = ty + (n_rows_to * 20 + 6) // 2

    # Only draw horizontal lines (from right to left) or vertical lines
    # Check if from_tab is to the left of to_tab
    if fx < tx:
        x1, y1 = from_center_x, from_center_y
        x2, y2 = to_center_x, to_center_y
    else:
        # Reverse direction: draw from left of from_tab to right of to_tab
        x1, y1 = fx, from_center_y
        x2, y2 = tx + bw, to_center_y

    mid_x = (x1 + x2) // 2
    draw.line([(x1, y1), (mid_x, y1), (mid_x, y2), (x2, y2)], fill=LINE_COLOR, width=2)

    # Draw small circle at ends
    draw.ellipse((x1 - 3, y1 - 3, x1 + 3, y1 + 3), fill=LINE_COLOR, outline=None)
    draw.ellipse((x2 - 3, y2 - 3, x2 + 3, y2 + 3), fill=LINE_COLOR, outline=None)

# ─── Legend ───────────────────────────────────────────────────────────────────

legend_y = IMG_H - 60
draw.text((START_X, legend_y), "Leyenda:", fill=TITLE_FG, font=FONT_BOLD)
legend_items = [
    ("PK", PK_FG, "Primary Key"),
    ("FK", FK_FG, "Foreign Key"),
    ("UNIQUE", (180, 255, 180), "Unique Constraint"),
    ("ENUM", (255, 200, 150), "Enum Type"),
]
lx = START_X + 100
for label, color, desc in legend_items:
    draw.rectangle((lx, legend_y - 2, lx + 12, legend_y + 10), fill=color)
    draw.text((lx + 16, legend_y - 2), f"{label} = {desc}", fill=TEXT_FG, font=FONT_SMALL)
    lx += draw.textbbox((0, 0), f"  {label} = {desc}  ", font=FONT_SMALL)[2] + 100

# Group colors in legend
gx = START_X
gy = legend_y + 22
draw.text((gx, gy), "Grupos:", fill=TITLE_FG, font=FONT_BOLD)
gx += 80
for name, color in [("Autenticación", COLOR_AUTH), ("Inventario", COLOR_INV),
                     ("Contratos", COLOR_CONTRACT), ("Operaciones", COLOR_OPS), ("Fotos", COLOR_PHOTO)]:
    draw.rectangle((gx, gy, gx + 12, gy + 12), fill=color)
    draw.text((gx + 16, gy), name, fill=TEXT_FG, font=FONT_SMALL)
    gx += draw.textbbox((0, 0), f"  {name}  ", font=FONT_SMALL)[2] + 40

# ─── Save ────────────────────────────────────────────────────────────────────
img.save(OUTPUT_IMG)
print(f"Diagrama guardado: {OUTPUT_IMG}")

# ─── Create Word document ────────────────────────────────────────────────────

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

doc = Document()
style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(12)
style.paragraph_format.line_spacing = 2.0

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# Title
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Diagrama Entidad-Relación\nBase de Datos SIGTAR")
r.font.name = "Times New Roman"
r.font.size = Pt(16)
r.bold = True

doc.add_paragraph()

# Image
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run()
r.add_picture(OUTPUT_IMG, width=Inches(6.0))

cap = doc.add_paragraph()
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = cap.add_run("Figura. Diagrama entidad-relación de la base de datos SIGTAR (15 tablas).")
r.font.name = "Times New Roman"
r.font.size = Pt(10)
r.italic = True

doc.add_paragraph()

# Tables list
h = doc.add_heading("Lista de Tablas", level=1)
for run in h.runs:
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.bold = True

table = doc.add_table(rows=1, cols=3)
table.style = "Table Grid"
table.alignment = WD_TABLE_ALIGNMENT.CENTER

def set_cell_shading(cell, color):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

hdr = table.rows[0]
for i, text in enumerate(["#", "Tabla", "Grupo"]):
    cell = hdr.cells[i]
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.bold = True
    set_cell_shading(cell, "2B579A")
    run.font.color.rgb = RGBColor(255, 255, 255)

group_map = {
    "Autenticación": ["roles", "permisos", "roles_permisos", "usuarios"],
    "Inventario": ["categorias_activo", "activos", "clientes"],
    "Contratos": ["contratos", "pagos", "asignaciones_activo"],
    "Operaciones": ["historial_ubicacion", "checklist_estado", "reportes_incidencia", "mantenimientos"],
    "Fotos": ["activos_fotos"],
}
table_group = {}
for g, tbls in group_map.items():
    for t in tbls:
        table_group[t] = g

for idx, name in enumerate(table_names, 1):
    row = table.add_row()
    for i, text in enumerate([str(idx), name, table_group.get(name, "-")]):
        cell = row.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)

# Relationships
doc.add_paragraph()
h = doc.add_heading("Relaciones entre Tablas", level=1)
for run in h.runs:
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.bold = True

rel_table = doc.add_table(rows=1, cols=3)
rel_table.style = "Table Grid"
rel_table.alignment = WD_TABLE_ALIGNMENT.CENTER

hdr = rel_table.rows[0]
for i, text in enumerate(["Tabla origen", "Tabla destino", "Columna FK"]):
    cell = hdr.cells[i]
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.bold = True
    set_cell_shading(cell, "2B579A")
    run.font.color.rgb = RGBColor(255, 255, 255)

for frm, to, col in relationships:
    row = rel_table.add_row()
    for i, text in enumerate([frm, to, col]):
        cell = row.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)

doc.save(OUTPUT_DOCX)
print(f"Documento guardado: {OUTPUT_DOCX}")
