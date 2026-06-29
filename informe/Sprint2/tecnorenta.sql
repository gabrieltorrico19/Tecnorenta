-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-06-2026 a las 03:00:01
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tecnorenta`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `activos`
--

CREATE TABLE `activos` (
  `id` int(11) NOT NULL,
  `codigo_inventario` varchar(50) NOT NULL,
  `modelo` varchar(100) NOT NULL,
  `numero_serie` varchar(100) NOT NULL,
  `estado` enum('DISPONIBLE','RENTADO','MANTENIMIENTO','BAJA') NOT NULL,
  `fecha_compra` date DEFAULT NULL,
  `valor_depreciado` float DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `creado_por` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `modificado_por` int(11) DEFAULT NULL,
  `fecha_modificacion` datetime DEFAULT current_timestamp(),
  `latitud` float DEFAULT NULL,
  `longitud` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `activos`
--

INSERT INTO `activos` (`id`, `codigo_inventario`, `modelo`, `numero_serie`, `estado`, `fecha_compra`, `valor_depreciado`, `id_categoria`, `creado_por`, `fecha_creacion`, `modificado_por`, `fecha_modificacion`, `latitud`, `longitud`) VALUES
(1, 'LPT-GAM-001', 'Alienware M18', 'SN-AW18-0001', 'DISPONIBLE', '2024-12-16', 1340.78, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-27 17:06:46', -20.6469, -54.7998),
(2, 'LPT-GAM-002', 'ASUS ROG Strix G16', 'SN-ROG16-0002', 'MANTENIMIENTO', '2024-02-02', 969.03, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-27 17:09:23', -15.7645, -64.7095),
(3, 'LPT-GAM-003', 'MSI Raider GE78', 'SN-MSI78-0003', 'DISPONIBLE', '2024-06-01', 2094.66, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(4, 'LPT-OFC-001', 'Lenovo ThinkPad X1', 'SN-LENX1-0004', 'RENTADO', '2024-06-03', 1687.12, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(5, 'LPT-OFC-002', 'Dell Latitude 5540', 'SN-DEL5540-5', 'MANTENIMIENTO', '2024-03-23', 2142.83, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(6, 'LPT-OFC-003', 'HP EliteBook 840', 'SN-HP840-0006', 'MANTENIMIENTO', '2024-07-15', 380.75, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(7, 'LPT-OFC-004', 'Lenovo ThinkPad T14', 'SN-T14-0007', 'MANTENIMIENTO', '2024-01-06', 1183.62, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(8, 'LPT-OFC-005', 'Dell Latitude 7440', 'SN-DEL7440-8', 'RENTADO', '2024-01-22', 1798.14, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(9, 'LPT-ULT-001', 'MacBook Air M3', 'SN-MBA-M3-009', 'RENTADO', '2024-11-20', 2193.51, 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(10, 'LPT-ULT-002', 'LG Gram 16', 'SN-LG16-0010', 'MANTENIMIENTO', '2024-05-10', 1510.19, 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(11, 'LPT-ULT-003', 'Samsung Galaxy Book3', 'SN-SAMGB3-011', 'DISPONIBLE', '2024-10-25', 1325.91, 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(12, 'LPT-ULT-004', 'ASUS ZenBook 14', 'SN-ZEN14-012', 'DISPONIBLE', '2024-05-28', 1752.67, 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(13, 'LPT-GAM-004', 'Razer Blade 16', 'SN-RAZ16-013', 'RENTADO', '2024-01-05', 128.1, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(14, 'LPT-OFC-006', 'Huawei MateBook 14', 'SN-HW14-0014', 'RENTADO', '2024-08-10', 2241.61, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(15, 'LPT-ULT-005', 'Acer Swift 5', 'SN-ACSW5-015', 'RENTADO', '2024-07-19', 1548.48, 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(16, 'LPT-GAM-005', 'Gigabyte Aorus 17', 'SN-GIG17-016', 'DISPONIBLE', '2024-03-07', 20.3, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(17, 'LPT-OFC-007', 'Fujitsu Lifebook U7', 'SN-FUJ-U7-017', 'DISPONIBLE', '2024-11-13', 1824.21, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(18, 'LPT-ULT-006', 'Microsoft Surface Laptop 5', 'SN-SRF5-018', 'RENTADO', '2024-06-08', 2119.17, 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(19, 'LPT-GAM-006', 'Lenovo Legion Pro 7', 'SN-LEG7-019', 'RENTADO', '2024-09-27', 279.67, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL),
(20, 'LPT-OFC-008', 'Dell Inspiron 16', 'SN-DELIN-020', 'RENTADO', '2024-04-06', 1292.77, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `activos_fotos`
--

CREATE TABLE `activos_fotos` (
  `id` int(11) NOT NULL,
  `id_activo` int(11) NOT NULL,
  `url` varchar(500) NOT NULL,
  `orden` int(11) DEFAULT NULL,
  `fecha_subida` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `activos_fotos`
--

INSERT INTO `activos_fotos` (`id`, `id_activo`, `url`, `orden`, `fecha_subida`) VALUES
(1, 1, 'activos/b54050829cc442e2a83686b970a95152.jpg', 0, '2026-06-27 16:09:42'),
(2, 1, 'activos/31159befdc134834b08a3cc07c1f5d52.jpg', 1, '2026-06-27 17:01:49');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('fea5c70ae009');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignaciones_activo`
--

CREATE TABLE `asignaciones_activo` (
  `id` int(11) NOT NULL,
  `fecha_asignacion` date NOT NULL,
  `fecha_devolucion` date DEFAULT NULL,
  `latitud` float DEFAULT NULL,
  `longitud` float DEFAULT NULL,
  `id_contrato` int(11) NOT NULL,
  `id_activo` int(11) NOT NULL,
  `creado_por` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `modificado_por` int(11) DEFAULT NULL,
  `fecha_modificacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asignaciones_activo`
--

INSERT INTO `asignaciones_activo` (`id`, `fecha_asignacion`, `fecha_devolucion`, `latitud`, `longitud`, `id_contrato`, `id_activo`, `creado_por`, `fecha_creacion`, `modificado_por`, `fecha_modificacion`) VALUES
(1, '2025-04-01', NULL, -17.4266, -60.6226, 4, 16, NULL, '2026-06-25 11:14:31', NULL, '2026-06-27 15:47:02'),
(2, '2025-06-01', NULL, -17.5219, -66.1738, 6, 10, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(3, '2025-02-03', NULL, -17.3771, -65.6701, 2, 6, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(4, '2025-03-01', NULL, -17.1674, -65.8463, 3, 6, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(5, '2025-01-06', NULL, -17.7045, -66.3899, 1, 10, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(6, '2025-08-03', NULL, -17.6547, -66.5955, 8, 6, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(7, '2025-06-05', NULL, -17.7239, -66.379, 6, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(8, '2025-08-01', NULL, -17.5481, -66.1012, 8, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(9, '2025-02-01', NULL, -17.8709, -66.4422, 2, 13, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(10, '2025-04-01', NULL, -17.6829, -65.6631, 4, 9, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(11, '2026-06-27', NULL, NULL, NULL, 1, 1, NULL, '2026-06-27 14:47:50', NULL, '2026-06-27 14:47:50'),
(12, '2026-06-27', NULL, NULL, NULL, 1, 1, NULL, '2026-06-27 14:49:16', NULL, '2026-06-27 14:49:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias_activo`
--

CREATE TABLE `categorias_activo` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `nivel` varchar(50) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `id_categoria_padre` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias_activo`
--

INSERT INTO `categorias_activo` (`id`, `nombre`, `nivel`, `descripcion`, `id_categoria_padre`) VALUES
(1, 'Laptops', '1', 'Equipos portátiles', NULL),
(2, 'Accesorios', '1', 'Periféricos y accesorios', NULL),
(3, 'Laptops Gamer', '2', 'Alto rendimiento', 1),
(4, 'Laptops Oficina', '2', 'Uso corporativo', 1),
(5, 'Laptops Ultraligeras', '2', 'Portabilidad extrema', 1),
(6, 'Monitores', '2', 'Pantallas externas', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `checklist_estado`
--

CREATE TABLE `checklist_estado` (
  `id` int(11) NOT NULL,
  `id_asignacion` int(11) NOT NULL,
  `momento` enum('ENTREGA','DEVOLUCION') NOT NULL,
  `pantalla` enum('BIEN','RAYADO','ROTO') NOT NULL,
  `teclado` enum('BIEN','RAYADO','ROTO') NOT NULL,
  `carcasa` enum('BIEN','RAYADO','ROTO') NOT NULL,
  `cargador` tinyint(1) NOT NULL,
  `observaciones` varchar(500) DEFAULT NULL,
  `url_fotos` varchar(500) DEFAULT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `razon_social` varchar(150) NOT NULL,
  `nit` varchar(50) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `latitud` float DEFAULT NULL,
  `longitud` float DEFAULT NULL,
  `sector` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `razon_social`, `nit`, `direccion`, `latitud`, `longitud`, `sector`) VALUES
(1, 'TechSolutions SRL', '1023457011', 'Av. Ballivián 123, Santa Cruz', -17.7833, -63.1825, 'Centro'),
(2, 'DataCenter Bolivia', '2015678022', 'Calle Potosí 456, La Paz', -16.5, -68.15, 'Sopocachi'),
(3, 'NetLogic Solutions', '3045789033', 'Av. Prado 789, Cochabamba', -17.3935, -66.157, 'Queru Queru'),
(4, 'Grupo InnovaTech', '4056891044', 'Calle Comercio 321, Santa Cruz', -17.7894, -63.1974, 'Equipetrol'),
(5, 'Sistemas del Sur', '5067902055', 'Av. Integración 654, Tarija', -21.5315, -64.7296, 'Centro'),
(6, 'Cloud Works SA', '6078913066', 'Calle 21 de Mayo 987, La Paz', -16.4944, -68.1357, 'Zona Sur'),
(7, 'TecnoExpress Ltda', '7089024077', 'Av. Busch 147, Santa Cruz', -17.7755, -63.175, 'El Pourrí'),
(8, 'ByteCorp Bolivia', '8090135088', 'Calle Colombia 258, Cochabamba', -17.38, -66.15, 'Norte'),
(9, 'Digital Solutions', '9101246099', 'Av. San Martín 369, Santa Cruz', -17.78, -63.16, 'Urb. Los Olivos'),
(10, 'InfraNet Group', '1012357000', 'Calle Junín 741, Sucre', -19.0333, -65.2627, 'Recoleta');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contratos`
--

CREATE TABLE `contratos` (
  `id` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `condiciones_uso` varchar(500) DEFAULT NULL,
  `estado` enum('ACTIVO','VENCIDO','CANCELADO','RENOVADO') NOT NULL,
  `monto_mensual` float NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `creado_por` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `modificado_por` int(11) DEFAULT NULL,
  `fecha_modificacion` datetime DEFAULT current_timestamp(),
  `url_documento` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `contratos`
--

INSERT INTO `contratos` (`id`, `fecha_inicio`, `fecha_fin`, `condiciones_uso`, `estado`, `monto_mensual`, `id_cliente`, `creado_por`, `fecha_creacion`, `modificado_por`, `fecha_modificacion`, `url_documento`) VALUES
(1, '2025-01-01', '2025-11-27', 'Uso exclusivo para desarrollo de software', 'ACTIVO', 4000, 6, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL),
(2, '2025-02-01', '2025-11-28', 'Equipo para diseño gráfico', 'ACTIVO', 2500, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL),
(3, '2025-03-01', '2025-11-26', 'Uso corporativo 24/7', 'ACTIVO', 3200, 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL),
(4, '2025-04-01', '2025-09-28', 'Trabajo remoto - facturación mensual', 'ACTIVO', 1800, 3, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL),
(5, '2025-05-01', '2025-10-28', 'Servidor de pruebas', 'VENCIDO', 5500, 6, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL),
(6, '2025-06-01', '2025-12-28', 'Oficina administrativa', 'ACTIVO', 2800, 2, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL),
(7, '2025-07-01', '2026-03-28', 'Desarrollo y testing', 'ACTIVO', 3500, 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL),
(8, '2025-08-01', '2026-04-28', 'Uso educativo', 'CANCELADO', 2100, 4, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_ubicacion`
--

CREATE TABLE `historial_ubicacion` (
  `id` int(11) NOT NULL,
  `id_asignacion` int(11) NOT NULL,
  `latitud` float NOT NULL,
  `longitud` float NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mantenimientos`
--

CREATE TABLE `mantenimientos` (
  `id` int(11) NOT NULL,
  `tipo` enum('PREVENTIVO','CORRECTIVO') NOT NULL,
  `fecha` date NOT NULL,
  `costo` float DEFAULT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  `url_foto` varchar(500) DEFAULT NULL,
  `id_activo` int(11) NOT NULL,
  `frecuencia_dias` int(11) DEFAULT NULL,
  `proxima_fecha` date DEFAULT NULL,
  `id_reporte_origen` int(11) DEFAULT NULL,
  `tiempo_reparacion` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id` int(11) NOT NULL,
  `id_contrato` int(11) NOT NULL,
  `concepto` varchar(200) NOT NULL,
  `monto` float NOT NULL,
  `fecha` date NOT NULL,
  `estado` enum('PENDIENTE','PAGADO','VENCIDO') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id`, `id_contrato`, `concepto`, `monto`, `fecha`, `estado`) VALUES
(1, 1, 'Cuota mes 1', 4000, '2025-01-05', 'PAGADO'),
(2, 1, 'Cuota mes 2', 4000, '2025-02-05', 'PAGADO'),
(3, 1, 'Cuota mes 3', 4000, '2025-03-05', 'PAGADO'),
(4, 2, 'Cuota mes 1', 2500, '2025-01-05', 'PAGADO'),
(5, 2, 'Cuota mes 2', 2500, '2025-02-05', 'PAGADO'),
(6, 2, 'Cuota mes 3', 2500, '2025-03-05', 'PENDIENTE'),
(7, 3, 'Cuota mes 1', 3200, '2025-01-05', 'PAGADO'),
(8, 3, 'Cuota mes 2', 3200, '2025-02-05', 'PAGADO'),
(9, 3, 'Cuota mes 3', 3200, '2025-03-05', 'PENDIENTE'),
(10, 4, 'Cuota mes 1', 1800, '2025-01-05', 'PENDIENTE'),
(11, 4, 'Cuota mes 2', 1800, '2025-02-05', 'PAGADO'),
(12, 4, 'Cuota mes 3', 1800, '2025-03-05', 'PAGADO'),
(13, 5, 'Cuota mes 1', 5500, '2025-01-05', 'PAGADO'),
(14, 5, 'Cuota mes 2', 5500, '2025-02-05', 'PENDIENTE'),
(15, 5, 'Cuota mes 3', 5500, '2025-03-05', 'PAGADO'),
(16, 6, 'Cuota mes 1', 2800, '2025-01-05', 'PAGADO'),
(17, 6, 'Cuota mes 2', 2800, '2025-02-05', 'PAGADO'),
(18, 6, 'Cuota mes 3', 2800, '2025-03-05', 'PAGADO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id`, `nombre`, `descripcion`) VALUES
(1, 'usuarios.listar', 'Listar usuarios'),
(2, 'usuarios.crear', 'Crear usuarios'),
(3, 'usuarios.editar', 'Editar usuarios'),
(4, 'usuarios.eliminar', 'Eliminar usuarios'),
(5, 'activos.listar', 'Listar activos'),
(6, 'activos.crear', 'Crear activos'),
(7, 'activos.editar', 'Editar activos'),
(8, 'activos.eliminar', 'Eliminar activos'),
(9, 'contratos.listar', 'Listar contratos'),
(10, 'contratos.crear', 'Crear contratos'),
(11, 'contratos.editar', 'Editar contratos'),
(12, 'reportes.listar', 'Listar reportes'),
(13, 'reportes.crear', 'Crear reportes'),
(14, 'clientes.listar', 'Listar clientes'),
(15, 'clientes.crear', 'Crear clientes'),
(16, 'contratos.eliminar', 'Eliminar contratos'),
(17, 'reportes.editar', 'Editar reportes/incidencias'),
(18, 'reportes.eliminar', 'Eliminar reportes/incidencias'),
(19, 'clientes.editar', 'Editar clientes'),
(20, 'clientes.eliminar', 'Eliminar clientes'),
(21, 'categorias.listar', 'Listar categorías'),
(22, 'categorias.crear', 'Crear categorías'),
(23, 'categorias.editar', 'Editar categorías'),
(24, 'categorias.eliminar', 'Eliminar categorías'),
(25, 'pagos.listar', 'Listar pagos'),
(26, 'pagos.crear', 'Registrar pagos'),
(27, 'pagos.editar', 'Editar pagos'),
(28, 'asignaciones.listar', 'Listar asignaciones'),
(29, 'asignaciones.crear', 'Crear asignaciones'),
(30, 'mantenimientos.listar', 'Listar mantenimientos'),
(31, 'mantenimientos.crear', 'Crear mantenimientos'),
(32, 'mantenimientos.editar', 'Editar mantenimientos'),
(33, 'dashboard.ver', 'Ver dashboard y estadísticas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes_incidencia`
--

CREATE TABLE `reportes_incidencia` (
  `id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `descripcion` varchar(500) NOT NULL,
  `gravedad` enum('LEVE','MODERADO','GRAVE') NOT NULL,
  `url_foto` varchar(500) DEFAULT NULL,
  `estado` enum('ABIERTO','EN_ATENCION','CERRADO') NOT NULL,
  `id_activo` int(11) NOT NULL,
  `creado_por` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `modificado_por` int(11) DEFAULT NULL,
  `fecha_modificacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reportes_incidencia`
--

INSERT INTO `reportes_incidencia` (`id`, `fecha`, `descripcion`, `gravedad`, `url_foto`, `estado`, `id_activo`, `creado_por`, `fecha_creacion`, `modificado_por`, `fecha_modificacion`) VALUES
(1, '2025-05-15', 'Pantalla con píxeles muertos en esquina superior derecha', 'LEVE', 'https://placehold.co/600x400?text=foto_incidencia', 'ABIERTO', 2, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(2, '2025-04-27', 'Teclado no responde teclas WASD después de derrame de café', 'MODERADO', 'https://placehold.co/600x400?text=foto_incidencia', 'EN_ATENCION', 5, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(3, '2025-06-20', 'Equipo no enciende, posible falla de motherboard', 'GRAVE', 'https://placehold.co/600x400?text=foto_incidencia', 'ABIERTO', 18, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(4, '2025-05-05', 'Batería dura menos de 30 minutos', 'MODERADO', 'https://placehold.co/600x400?text=foto_incidencia', 'CERRADO', 20, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31'),
(5, '2025-03-22', 'Cargador original dañado, requiere reemplazo', 'LEVE', 'https://placehold.co/600x400?text=foto_incidencia', 'CERRADO', 1, NULL, '2026-06-25 11:14:31', NULL, '2026-06-25 11:14:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `nombre`) VALUES
(4, 'Administrador'),
(8, 'Almacén'),
(6, 'Cliente'),
(7, 'Gerente'),
(5, 'Operador'),
(9, 'Técnico');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles_permisos`
--

CREATE TABLE `roles_permisos` (
  `id_rol` int(11) NOT NULL,
  `id_permiso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles_permisos`
--

INSERT INTO `roles_permisos` (`id_rol`, `id_permiso`) VALUES
(4, 1),
(4, 2),
(4, 3),
(4, 4),
(4, 5),
(4, 6),
(4, 7),
(4, 8),
(4, 9),
(4, 10),
(4, 11),
(4, 12),
(4, 13),
(4, 14),
(4, 15),
(5, 5),
(5, 9),
(5, 10),
(5, 11),
(5, 12),
(5, 13),
(5, 14),
(5, 15),
(7, 5),
(7, 9),
(7, 10),
(7, 11),
(7, 12),
(7, 13),
(7, 14),
(7, 15),
(8, 5),
(8, 6),
(8, 7),
(8, 8),
(8, 12),
(9, 5),
(9, 12),
(9, 13);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  `id_rol` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password_hash`, `telefono`, `activo`, `id_rol`, `created_at`, `updated_at`) VALUES
(1, 'Administrador', 'admin@tecnorenta.com', '$2b$10$fVMCZqItKuOtNE/34p.geevvfdQEA6JyYk1c9CduLXPiruLdMxz72', '000000000', 1, 4, '2026-06-25 10:35:42', '2026-06-25 10:35:42');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `activos`
--
ALTER TABLE `activos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_serie` (`numero_serie`),
  ADD UNIQUE KEY `ix_activos_codigo_inventario` (`codigo_inventario`),
  ADD KEY `creado_por` (`creado_por`),
  ADD KEY `id_categoria` (`id_categoria`),
  ADD KEY `modificado_por` (`modificado_por`),
  ADD KEY `ix_activos_id` (`id`);

--
-- Indices de la tabla `activos_fotos`
--
ALTER TABLE `activos_fotos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_activo` (`id_activo`),
  ADD KEY `ix_activos_fotos_id` (`id`);

--
-- Indices de la tabla `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indices de la tabla `asignaciones_activo`
--
ALTER TABLE `asignaciones_activo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `creado_por` (`creado_por`),
  ADD KEY `id_activo` (`id_activo`),
  ADD KEY `id_contrato` (`id_contrato`),
  ADD KEY `modificado_por` (`modificado_por`),
  ADD KEY `ix_asignaciones_activo_id` (`id`);

--
-- Indices de la tabla `categorias_activo`
--
ALTER TABLE `categorias_activo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_categorias_activo_id` (`id`),
  ADD KEY `fk_categoria_padre` (`id_categoria_padre`);

--
-- Indices de la tabla `checklist_estado`
--
ALTER TABLE `checklist_estado`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_asignacion` (`id_asignacion`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `ix_checklist_estado_id` (`id`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_clientes_nit` (`nit`),
  ADD KEY `ix_clientes_id` (`id`);

--
-- Indices de la tabla `contratos`
--
ALTER TABLE `contratos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `creado_por` (`creado_por`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `modificado_por` (`modificado_por`),
  ADD KEY `ix_contratos_id` (`id`);

--
-- Indices de la tabla `historial_ubicacion`
--
ALTER TABLE `historial_ubicacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_asignacion` (`id_asignacion`),
  ADD KEY `ix_historial_ubicacion_id` (`id`);

--
-- Indices de la tabla `mantenimientos`
--
ALTER TABLE `mantenimientos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_activo` (`id_activo`),
  ADD KEY `id_reporte_origen` (`id_reporte_origen`),
  ADD KEY `ix_mantenimientos_id` (`id`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_contrato` (`id_contrato`),
  ADD KEY `ix_pagos_id` (`id`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`),
  ADD KEY `ix_permisos_id` (`id`);

--
-- Indices de la tabla `reportes_incidencia`
--
ALTER TABLE `reportes_incidencia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `creado_por` (`creado_por`),
  ADD KEY `id_activo` (`id_activo`),
  ADD KEY `modificado_por` (`modificado_por`),
  ADD KEY `ix_reportes_incidencia_id` (`id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`),
  ADD KEY `ix_roles_id` (`id`);

--
-- Indices de la tabla `roles_permisos`
--
ALTER TABLE `roles_permisos`
  ADD PRIMARY KEY (`id_rol`,`id_permiso`),
  ADD KEY `id_permiso` (`id_permiso`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_usuarios_email` (`email`),
  ADD KEY `id_rol` (`id_rol`),
  ADD KEY `ix_usuarios_id` (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `activos`
--
ALTER TABLE `activos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `activos_fotos`
--
ALTER TABLE `activos_fotos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `asignaciones_activo`
--
ALTER TABLE `asignaciones_activo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `categorias_activo`
--
ALTER TABLE `categorias_activo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `checklist_estado`
--
ALTER TABLE `checklist_estado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `contratos`
--
ALTER TABLE `contratos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `historial_ubicacion`
--
ALTER TABLE `historial_ubicacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `mantenimientos`
--
ALTER TABLE `mantenimientos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `reportes_incidencia`
--
ALTER TABLE `reportes_incidencia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `activos`
--
ALTER TABLE `activos`
  ADD CONSTRAINT `activos_ibfk_1` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `activos_ibfk_2` FOREIGN KEY (`id_categoria`) REFERENCES `categorias_activo` (`id`),
  ADD CONSTRAINT `activos_ibfk_3` FOREIGN KEY (`modificado_por`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `activos_fotos`
--
ALTER TABLE `activos_fotos`
  ADD CONSTRAINT `activos_fotos_ibfk_1` FOREIGN KEY (`id_activo`) REFERENCES `activos` (`id`);

--
-- Filtros para la tabla `asignaciones_activo`
--
ALTER TABLE `asignaciones_activo`
  ADD CONSTRAINT `asignaciones_activo_ibfk_1` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `asignaciones_activo_ibfk_2` FOREIGN KEY (`id_activo`) REFERENCES `activos` (`id`),
  ADD CONSTRAINT `asignaciones_activo_ibfk_3` FOREIGN KEY (`id_contrato`) REFERENCES `contratos` (`id`),
  ADD CONSTRAINT `asignaciones_activo_ibfk_4` FOREIGN KEY (`modificado_por`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `categorias_activo`
--
ALTER TABLE `categorias_activo`
  ADD CONSTRAINT `fk_categoria_padre` FOREIGN KEY (`id_categoria_padre`) REFERENCES `categorias_activo` (`id`);

--
-- Filtros para la tabla `checklist_estado`
--
ALTER TABLE `checklist_estado`
  ADD CONSTRAINT `checklist_estado_ibfk_1` FOREIGN KEY (`id_asignacion`) REFERENCES `asignaciones_activo` (`id`),
  ADD CONSTRAINT `checklist_estado_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `contratos`
--
ALTER TABLE `contratos`
  ADD CONSTRAINT `contratos_ibfk_1` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `contratos_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `contratos_ibfk_3` FOREIGN KEY (`modificado_por`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `historial_ubicacion`
--
ALTER TABLE `historial_ubicacion`
  ADD CONSTRAINT `historial_ubicacion_ibfk_1` FOREIGN KEY (`id_asignacion`) REFERENCES `asignaciones_activo` (`id`);

--
-- Filtros para la tabla `mantenimientos`
--
ALTER TABLE `mantenimientos`
  ADD CONSTRAINT `mantenimientos_ibfk_1` FOREIGN KEY (`id_activo`) REFERENCES `activos` (`id`),
  ADD CONSTRAINT `mantenimientos_ibfk_2` FOREIGN KEY (`id_reporte_origen`) REFERENCES `reportes_incidencia` (`id`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_contrato`) REFERENCES `contratos` (`id`);

--
-- Filtros para la tabla `reportes_incidencia`
--
ALTER TABLE `reportes_incidencia`
  ADD CONSTRAINT `reportes_incidencia_ibfk_1` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `reportes_incidencia_ibfk_2` FOREIGN KEY (`id_activo`) REFERENCES `activos` (`id`),
  ADD CONSTRAINT `reportes_incidencia_ibfk_3` FOREIGN KEY (`modificado_por`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `roles_permisos`
--
ALTER TABLE `roles_permisos`
  ADD CONSTRAINT `roles_permisos_ibfk_1` FOREIGN KEY (`id_permiso`) REFERENCES `permisos` (`id`),
  ADD CONSTRAINT `roles_permisos_ibfk_2` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
