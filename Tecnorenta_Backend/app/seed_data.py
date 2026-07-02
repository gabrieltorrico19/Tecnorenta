"""Seed de datos de demostración (idempotente y determinista).

Los datos se anclan a ``date.today()`` para que el dashboard/DSS siempre
cuente una "historia viva": contratos por vencer, cuotas vencidas y
mantenimientos programados relativos al momento en que se ejecuta el seed.

Reglas de negocio que este seed materializa (ver docs/DSS_KPIs_SIGTAR.md):
  - Ocupación de flota por debajo de la meta (11 rentados / 18 operativos).
  - 3 contratos activos vencen en <= 30 días (ingreso en riesgo).
  - Cartera vencida concentrada en 3 contratos (6 cuotas en estado vencido).
  - Mantenimiento correctivo > preventivo (plan preventivo insuficiente).
"""
import calendar
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.cliente import Cliente
from app.models.categoria_activo import CategoriaActivo
from app.models.activo import Activo, EstadoActivo
from app.models.contrato import Contrato, EstadoContrato
from app.models.pago import Pago, EstadoPago
from app.models.asignacion_activo import AsignacionActivo
from app.models.reporte_incidencia import ReporteIncidencia, GravedadIncidencia, EstadoIncidencia
from app.models.mantenimiento import (
    MantenimientoPreventivo,
    MantenimientoCorrectivo,
    Mantenimiento,
)

# Prefijo con el que se etiquetan las filas sembradas, para permitir
# limpieza selectiva (downgrade de migraciones) sin tocar datos reales.
SEED_TAG = "[demo]"


def _add_months(base: date, months: int) -> date:
    """Suma (o resta) meses a una fecha respetando el fin de mes."""
    m = base.month - 1 + months
    y = base.year + m // 12
    m = m % 12 + 1
    d = min(base.day, calendar.monthrange(y, m)[1])
    return date(y, m, d)


def seed_clientes(db: Session) -> list[Cliente]:
    data = [
        {"razon_social": "TechSolutions SRL", "nit": "1023457011", "direccion": "Av. Ballivián 123, Santa Cruz", "latitud": -17.7833, "longitud": -63.1825, "sector": "Centro"},
        {"razon_social": "DataCenter Bolivia", "nit": "2015678022", "direccion": "Calle Potosí 456, La Paz", "latitud": -16.5000, "longitud": -68.1500, "sector": "Sopocachi"},
        {"razon_social": "NetLogic Solutions", "nit": "3045789033", "direccion": "Av. Prado 789, Cochabamba", "latitud": -17.3935, "longitud": -66.1570, "sector": "Queru Queru"},
        {"razon_social": "Grupo InnovaTech", "nit": "4056891044", "direccion": "Calle Comercio 321, Santa Cruz", "latitud": -17.7894, "longitud": -63.1974, "sector": "Equipetrol"},
        {"razon_social": "Sistemas del Sur", "nit": "5067902055", "direccion": "Av. Integración 654, Tarija", "latitud": -21.5315, "longitud": -64.7296, "sector": "Centro"},
        {"razon_social": "Cloud Works SA", "nit": "6078913066", "direccion": "Calle 21 de Mayo 987, La Paz", "latitud": -16.4944, "longitud": -68.1357, "sector": "Zona Sur"},
        {"razon_social": "TecnoExpress Ltda", "nit": "7089024077", "direccion": "Av. Busch 147, Santa Cruz", "latitud": -17.7755, "longitud": -63.1750, "sector": "El Pourrí"},
        {"razon_social": "ByteCorp Bolivia", "nit": "8090135088", "direccion": "Calle Colombia 258, Cochabamba", "latitud": -17.3800, "longitud": -66.1500, "sector": "Norte"},
        {"razon_social": "Digital Solutions", "nit": "9101246099", "direccion": "Av. San Martín 369, Santa Cruz", "latitud": -17.7800, "longitud": -63.1600, "sector": "Urb. Los Olivos"},
        {"razon_social": "InfraNet Group", "nit": "1012357000", "direccion": "Calle Junín 741, Sucre", "latitud": -19.0333, "longitud": -65.2627, "sector": "Recoleta"},
    ]
    for d in data:
        existing = db.query(Cliente).filter(Cliente.nit == d["nit"]).first()
        if not existing:
            db.add(Cliente(**d))
    db.flush()
    return db.query(Cliente).order_by(Cliente.id).all()


def seed_categorias(db: Session) -> dict[str, int]:
    cats: dict[str, int] = {}
    padres = [
        {"nombre": "Laptops", "nivel": "1", "descripcion": "Equipos portátiles"},
        {"nombre": "Accesorios", "nivel": "1", "descripcion": "Periféricos y accesorios"},
    ]
    for p in padres:
        existing = db.query(CategoriaActivo).filter(CategoriaActivo.nombre == p["nombre"], CategoriaActivo.nivel == "1").first()
        if not existing:
            existing = CategoriaActivo(**p)
            db.add(existing)
            db.flush()
        cats[p["nombre"]] = existing.id

    hijos = [
        {"nombre": "Laptops Gamer", "nivel": "2", "descripcion": "Alto rendimiento", "id_categoria_padre": cats["Laptops"]},
        {"nombre": "Laptops Oficina", "nivel": "2", "descripcion": "Uso corporativo", "id_categoria_padre": cats["Laptops"]},
        {"nombre": "Laptops Ultraligeras", "nivel": "2", "descripcion": "Portabilidad extrema", "id_categoria_padre": cats["Laptops"]},
        {"nombre": "Monitores", "nivel": "2", "descripcion": "Pantallas externas", "id_categoria_padre": cats["Accesorios"]},
    ]
    for h in hijos:
        existing = db.query(CategoriaActivo).filter(CategoriaActivo.nombre == h["nombre"]).first()
        if not existing:
            existing = CategoriaActivo(**h)
            db.add(existing)
            db.flush()
        cats[h["nombre"]] = existing.id
    return cats


def seed_activos(db: Session, cats: dict[str, int]) -> list[Activo]:
    modelos = [
        ("LPT-GAM-001", "Alienware M18", "SN-AW18-0001", "Laptops Gamer"),
        ("LPT-GAM-002", "ASUS ROG Strix G16", "SN-ROG16-0002", "Laptops Gamer"),
        ("LPT-GAM-003", "MSI Raider GE78", "SN-MSI78-0003", "Laptops Gamer"),
        ("LPT-OFC-001", "Lenovo ThinkPad X1", "SN-LENX1-0004", "Laptops Oficina"),
        ("LPT-OFC-002", "Dell Latitude 5540", "SN-DEL5540-5", "Laptops Oficina"),
        ("LPT-OFC-003", "HP EliteBook 840", "SN-HP840-0006", "Laptops Oficina"),
        ("LPT-OFC-004", "Lenovo ThinkPad T14", "SN-T14-0007", "Laptops Oficina"),
        ("LPT-OFC-005", "Dell Latitude 7440", "SN-DEL7440-8", "Laptops Oficina"),
        ("LPT-ULT-001", "MacBook Air M3", "SN-MBA-M3-009", "Laptops Ultraligeras"),
        ("LPT-ULT-002", "LG Gram 16", "SN-LG16-0010", "Laptops Ultraligeras"),
        ("LPT-ULT-003", "Samsung Galaxy Book3", "SN-SAMGB3-011", "Laptops Ultraligeras"),
        ("LPT-ULT-004", "ASUS ZenBook 14", "SN-ZEN14-012", "Laptops Ultraligeras"),
        ("LPT-GAM-004", "Razer Blade 16", "SN-RAZ16-013", "Laptops Gamer"),
        ("LPT-OFC-006", "Huawei MateBook 14", "SN-HW14-0014", "Laptops Oficina"),
        ("LPT-ULT-005", "Acer Swift 5", "SN-ACSW5-015", "Laptops Ultraligeras"),
        ("LPT-GAM-005", "Gigabyte Aorus 17", "SN-GIG17-016", "Laptops Gamer"),
        ("LPT-OFC-007", "Fujitsu Lifebook U7", "SN-FUJ-U7-017", "Laptops Oficina"),
        ("LPT-ULT-006", "Microsoft Surface Laptop 5", "SN-SRF5-018", "Laptops Ultraligeras"),
        ("LPT-GAM-006", "Lenovo Legion Pro 7", "SN-LEG7-019", "Laptops Gamer"),
        ("LPT-OFC-008", "Dell Inspiron 16", "SN-DELIN-020", "Laptops Oficina"),
    ]
    # Distribución determinista: 11 rentado, 4 disponible, 3 mantenimiento, 2 baja.
    estados = (
        [EstadoActivo.RENTADO] * 11
        + [EstadoActivo.DISPONIBLE] * 4
        + [EstadoActivo.MANTENIMIENTO] * 3
        + [EstadoActivo.BAJA] * 2
    )
    for i, (cod, modelo, serie, cat_nombre) in enumerate(modelos):
        existing = db.query(Activo).filter(Activo.codigo_inventario == cod).first()
        if not existing:
            db.add(Activo(
                codigo_inventario=cod,
                modelo=modelo,
                numero_serie=serie,
                estado=estados[i],
                # Antigüedad escalonada 2022-2024 para el KPI de edad de flota.
                fecha_compra=date(2022 + (i % 3), ((i * 7) % 12) + 1, 15),
                valor_depreciado=float(800 + 90 * i),
                id_categoria=cats.get(cat_nombre),
            ))
    db.flush()
    return db.query(Activo).order_by(Activo.id).all()


def seed_contratos(db: Session, clientes: list[Cliente]) -> list[Contrato]:
    hoy = date.today()
    # (cliente_idx, monto_mensual, condiciones, estado, offset_fin_en_dias)
    #  Índices 0-2: activos que vencen pronto (ingreso en riesgo).
    #  Índices 3-5: reciben cartera vencida (clientes morosos).
    #  Índices 6-7: activo sano + contrato cancelado (churn).
    data = [
        (0, 4000, "Uso exclusivo para desarrollo de software", "activo", 15),
        (2, 2500, "Equipo para diseño gráfico", "activo", 25),
        (3, 3200, "Uso corporativo 24/7", "activo", 28),
        (1, 1800, "Trabajo remoto - facturación mensual", "activo", 120),
        (4, 5500, "Servidor de pruebas (contrato expirado con saldo)", "vencido", -40),
        (5, 2800, "Oficina administrativa", "activo", 210),
        (6, 3500, "Desarrollo y testing", "activo", 300),
        (7, 2100, "Uso educativo", "cancelado", -100),
    ]
    # Idempotencia por ETIQUETA (no por COUNT global): si ya existen contratos
    # reales del usuario, no se los sobreescribe ni se les estampan pagos demo.
    # seed_pagos/seed_asignaciones operan solo sobre estos contratos demo.
    demo = db.query(Contrato).filter(
        Contrato.condiciones_uso.like(f"{SEED_TAG}%")
    ).order_by(Contrato.id).all()
    if demo:
        return demo

    for cli_idx, monto, cond, estado, off_fin in data:
        cliente = clientes[cli_idx % len(clientes)]
        fin = hoy + timedelta(days=off_fin)
        inicio = fin - timedelta(days=365)
        db.add(Contrato(
            fecha_inicio=inicio,
            fecha_fin=fin,
            condiciones_uso=f"{SEED_TAG} {cond}",
            estado=EstadoContrato(estado),
            monto_mensual=float(monto),
            id_cliente=cliente.id,
        ))
    db.flush()
    return db.query(Contrato).filter(
        Contrato.condiciones_uso.like(f"{SEED_TAG}%")
    ).order_by(Contrato.id).all()


def seed_pagos(db: Session, contratos: list[Contrato]) -> None:
    """Genera 5 cuotas mensuales para los primeros 6 contratos.

    Grupo A (índices 0-2): clientes al día  -> 4 pagado + 1 pendiente.
    Grupo B (índices 3-5): clientes morosos -> 2 pagado + 2 vencido + 1 pendiente.
    """
    hoy = date.today()
    objetivo = contratos[:6]
    # offset_mes -> estado de la cuota
    plan_al_dia = {-4: "pagado", -3: "pagado", -2: "pagado", -1: "pagado", 0: "pendiente"}
    plan_moroso = {-4: "pagado", -3: "pagado", -2: "vencido", -1: "vencido", 0: "pendiente"}

    for idx, cont in enumerate(objetivo):
        plan = plan_al_dia if idx < 3 else plan_moroso
        for off, estado in plan.items():
            fecha = _add_months(hoy.replace(day=5), off)
            periodo = fecha.strftime("%Y-%m")
            concepto = f"Cuota {periodo}"
            existing = db.query(Pago).filter(
                Pago.id_contrato == cont.id,
                Pago.concepto == concepto,
            ).first()
            if not existing:
                db.add(Pago(
                    id_contrato=cont.id,
                    concepto=concepto,
                    monto=cont.monto_mensual,
                    fecha=fecha,
                    estado=EstadoPago(estado),
                ))
    db.flush()


def seed_asignaciones(db: Session, contratos: list[Contrato], activos: list[Activo]) -> None:
    if db.query(AsignacionActivo).count() > 0:
        return
    # (activo_idx, contrato_idx). Los activos 0 y 1 se rentan dos veces
    # (alta utilización) para dar variedad al KPI revenue-per-asset.
    pares = [(i, i % len(contratos)) for i in range(11)] + [(0, 6), (1, 5)]
    for activo_idx, cont_idx in pares:
        contrato = contratos[cont_idx]
        activo = activos[activo_idx]
        db.add(AsignacionActivo(
            fecha_asignacion=contrato.fecha_inicio + timedelta(days=3),
            id_contrato=contrato.id,
            id_activo=activo.id,
            latitud=-17.38 + (activo_idx % 5) * 0.03,
            longitud=-66.15 + (activo_idx % 5) * 0.03,
        ))
    db.flush()


def seed_reportes(db: Session, activos: list[Activo]) -> list[ReporteIncidencia]:
    hoy = date.today()
    # (descripcion, gravedad, estado, activo_idx, dias_atras)
    data = [
        ("Pantalla con píxeles muertos en esquina superior derecha", "leve", "abierto", 0, 12),
        ("Teclado no responde teclas WASD después de derrame de café", "moderado", "en_atencion", 1, 20),
        ("Equipo no enciende, posible falla de motherboard", "grave", "abierto", 2, 9),
        ("Batería dura menos de 30 minutos", "moderado", "cerrado", 3, 40),
        ("Cargador original dañado, requiere reemplazo", "leve", "cerrado", 4, 55),
    ]
    if db.query(ReporteIncidencia).count() == 0:
        for desc, grav, est, activo_idx, dias in data:
            db.add(ReporteIncidencia(
                fecha=hoy - timedelta(days=dias),
                descripcion=desc,
                gravedad=GravedadIncidencia(grav),
                url_foto="https://placehold.co/600x400?text=foto_incidencia",
                estado=EstadoIncidencia(est),
                id_activo=activos[activo_idx].id,
            ))
        db.flush()
    return db.query(ReporteIncidencia).order_by(ReporteIncidencia.id).all()


def seed_mantenimientos(db: Session, activos: list[Activo], reportes: list[ReporteIncidencia]) -> None:
    """Siembra mantenimientos preventivos y correctivos con costo.

    El costo correctivo (1.850) supera al preventivo (910) para disparar la
    recomendación "reforzar plan preventivo". Dos preventivos vencen en <=30
    días para alimentar el KPI de mantenimientos programados.
    """
    if db.query(Mantenimiento).count() > 0:
        return
    hoy = date.today()

    # Preventivos: (activo_idx, costo, dias_ultima, frecuencia, offset_proxima)
    preventivos = [
        (0, 150.0, 60, 90, 30),
        (4, 200.0, 45, 90, 45),
        (15, 180.0, 20, 90, 70),
        (16, 220.0, 10, 60, 50),
        (17, 160.0, 5, 60, 25),
    ]
    for activo_idx, costo, dias, frec, prox in preventivos:
        db.add(MantenimientoPreventivo(
            fecha=hoy - timedelta(days=dias),
            costo=costo,
            descripcion=f"{SEED_TAG} Mantenimiento preventivo programado (limpieza + revisión)",
            id_activo=activos[activo_idx].id,
            frecuencia_dias=frec,
            proxima_fecha=hoy + timedelta(days=prox),
        ))

    # Correctivos ligados a incidencias graves/moderadas.
    reportes_por_gravedad: dict[str, list[ReporteIncidencia]] = {}
    for r in reportes:
        grav = r.gravedad.value if hasattr(r.gravedad, "value") else str(r.gravedad)
        reportes_por_gravedad.setdefault(grav, []).append(r)

    correctivos_plan = [
        ("grave", 0, 600.0, 8, 5),
        ("moderado", 0, 450.0, 15, 3),
        ("moderado", 1, 800.0, 3, 2),
    ]
    for gravedad, ridx, costo, dias, reparacion in correctivos_plan:
        candidatos = reportes_por_gravedad.get(gravedad, [])
        if len(candidatos) <= ridx:
            continue
        rep = candidatos[ridx]
        db.add(MantenimientoCorrectivo(
            fecha=hoy - timedelta(days=dias),
            costo=costo,
            descripcion=f"{SEED_TAG} Reparación correctiva por incidencia #{rep.id}",
            id_activo=rep.id_activo,
            id_reporte_origen=rep.id,
            tiempo_reparacion=reparacion,
        ))
    db.flush()


def run(db: Session) -> dict[str, int]:
    """Ejecuta todo el pipeline de datos de demo sobre una sesión dada.

    Reutilizable desde ``main()`` (CLI) y desde las migraciones Alembic.
    """
    clientes = seed_clientes(db)
    cats = seed_categorias(db)
    activos = seed_activos(db, cats)
    contratos = seed_contratos(db, clientes)
    seed_pagos(db, contratos)
    seed_asignaciones(db, contratos, activos)
    reportes = seed_reportes(db, activos)
    seed_mantenimientos(db, activos, reportes)
    return {
        "clientes": len(clientes),
        "activos": len(activos),
        "contratos": len(contratos),
        "reportes": len(reportes),
    }


def main() -> None:
    db = SessionLocal()
    try:
        resumen = run(db)
        db.commit()
        print(f"Seed data: {resumen}")
    except Exception as e:  # pragma: no cover
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
