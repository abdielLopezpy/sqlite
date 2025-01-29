"""
Sistema de Inventario y Ventas con PostgreSQL
===========================================

Este script implementa un sistema de gestión de inventario y ventas
con análisis de datos en tiempo real. Es un ejemplo educativo que
muestra cómo usar SQL en un contexto empresarial real.

🎯 Objetivos de Aprendizaje:
--------------------------
1. Implementación de CRUD en PostgreSQL
2. Análisis de datos con SQL
3. Manejo de transacciones y relaciones
4. Generación de reportes empresariales

📝 Preguntas de Análisis:
-----------------------
1. ¿Por qué usamos DECIMAL(10,2) para los precios en lugar de FLOAT?
2. ¿Qué ventajas ofrece el uso de FOREIGN KEY en la tabla ventas?
3. ¿Por qué es importante el uso de transacciones en las ventas?
4. ¿Cómo ayuda el análisis de datos en la toma de decisiones?
5. ¿Qué mejoras sugieres para el sistema?


💡 Conceptos Clave:
----------------
- Relaciones entre tablas (productos -> ventas)
- Agregaciones SQL (SUM, AVG, COUNT)
- Análisis temporal de datos
- Gestión de inventario
- Reportes empresariales

"""

import psycopg2
import psycopg2.extras

# Usar la misma conexión que funciona en main.py
inventory_neo =
def get_inventory_connection():
    """
    Devuelve una conexión a la base de datos PostgreSQL para el inventario.
    """
    return psycopg2.connect(inventory_neo)


def create_inventory_tables():
    """
    Crea las tablas necesarias para el sistema de inventario.

    📚 Análisis de la Estructura:
    --------------------------
    1. Tabla productos: Almacena el catálogo de productos
       - ¿Por qué usamos SERIAL para el ID?
       - ¿Qué implica NOT NULL en nombre y precio?

    2. Tabla ventas: Registra las transacciones
       - ¿Cómo se relaciona con productos?
       - ¿Por qué usamos DEFAULT CURRENT_TIMESTAMP?
    """
    create_tables_query = """
    CREATE TABLE IF NOT EXISTS productos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        precio DECIMAL(10, 2) NOT NULL,
        stock INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS ventas (
        id SERIAL PRIMARY KEY,
        producto_id INTEGER REFERENCES productos(id),
        cantidad INTEGER NOT NULL,
        fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()
        cursor.execute(create_tables_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ [OK] Tablas de inventario creadas (o ya existen).")
    except Exception as e:
        print("❌ [ERROR] No se pudieron crear las tablas de inventario:", e)


def insert_product():
    """
    Inserta un nuevo producto en la tabla 'productos'.
    """
    print("\n📦 Registro de nuevo producto:")
    nombre = input("  🏷️ Nombre del producto: ")
    precio = input("  💲 Precio: ")
    stock = input("  📦 Stock: ")

    insert_query = """
    INSERT INTO productos (nombre, precio, stock)
    VALUES (%s, %s, %s)
    RETURNING id, nombre;
    """
    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, (nombre, precio, stock))
        producto_id, producto_nombre = cursor.fetchone()
        conn.commit()
        print(
            f"✅ [INSERT] Producto '{producto_nombre}' registrado con ID={producto_id}"
        )
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [INSERT - ERROR]", e)


def view_products():
    """
    Muestra todos los productos disponibles.
    """
    select_query = "SELECT id, nombre, precio, stock FROM productos;"
    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()
        cursor.execute(select_query)
        productos = cursor.fetchall()
        cursor.close()
        conn.close()

        if productos:
            print("\n📦 Lista de Productos:")
            print("=" * 80)
            for producto in productos:
                print(f"ID: {producto[0]}")
                print(f"🏷️ Nombre: {producto[1]}")
                print(f"💲 Precio: {producto[2]}")
                print(f"📦 Stock: {producto[3]}")
                print("-" * 80)
        else:
            print("⚠️ No hay productos registrados")
    except Exception as e:
        print("❌ [SELECT - ERROR]", e)


def insert_sale():
    """
    Registra una venta en la tabla 'ventas'.
    """
    print("\n🛒 Registro de nueva venta:")
    producto_id = input("  🏷️ ID del producto: ")
    cantidad = input("  🔢 Cantidad: ")

    insert_query = """
    INSERT INTO ventas (producto_id, cantidad)
    VALUES (%s, %s)
    RETURNING id;
    """
    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, (producto_id, cantidad))
        venta_id = cursor.fetchone()[0]
        conn.commit()
        print(f"✅ [INSERT] Venta registrada con ID={venta_id}")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [INSERT - ERROR]", e)


def view_sales():
    """
    Muestra el historial de ventas.
    """
    select_query = """
    SELECT v.id, p.nombre, v.cantidad, v.fecha_venta
    FROM ventas v
    JOIN productos p ON v.producto_id = p.id
    ORDER BY v.fecha_venta DESC;
    """
    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()
        cursor.execute(select_query)
        ventas = cursor.fetchall()
        cursor.close()
        conn.close()

        if ventas:
            print("\n🛒 Historial de Ventas:")
            print("=" * 80)
            for venta in ventas:
                print(f"ID Venta: {venta[0]}")
                print(f"🏷️ Producto: {venta[1]}")
                print(f"🔢 Cantidad: {venta[2]}")
                print(f"📅 Fecha: {venta[3]}")
                print("-" * 80)
        else:
            print("⚠️ No hay ventas registradas")
    except Exception as e:
        print("❌ [SELECT - ERROR]", e)


def generate_analytics():
    """
    Genera reportes y análisis automáticos de ventas e inventario
    """
    analytics_queries = {
        "ventas_por_dia": """
            SELECT DATE(fecha_venta) as dia,
                   COUNT(*) as total_ventas,
                   SUM(v.cantidad * p.precio) as ingresos_total
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            GROUP BY dia
            ORDER BY dia DESC
            LIMIT 7;
        """,
        "productos_mas_vendidos": """
            SELECT p.nombre,
                   SUM(v.cantidad) as unidades_vendidas,
                   SUM(v.cantidad * p.precio) as ingresos_generados
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            GROUP BY p.id, p.nombre
            ORDER BY unidades_vendidas DESC
            LIMIT 5;
        """,
        "stock_critico": """
            SELECT nombre, stock,
                   CASE 
                       WHEN stock = 0 THEN '❌ Sin stock'
                       WHEN stock < 5 THEN '⚠️ Crítico'
                       WHEN stock < 10 THEN '📊 Bajo'
                       ELSE '✅ Normal'
                   END as estado
            FROM productos
            WHERE stock < 10
            ORDER BY stock ASC;
        """,
        "promedio_ventas": """
            SELECT p.nombre,
                   ROUND(AVG(v.cantidad), 2) as promedio_unidades,
                   ROUND(AVG(v.cantidad * p.precio), 2) as promedio_ingresos
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            GROUP BY p.id, p.nombre
            ORDER BY promedio_ingresos DESC;
        """,
    }

    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()

        # Ventas por día
        print("\n📊 ANÁLISIS DE VENTAS (Últimos 7 días)")
        print("=" * 50)
        cursor.execute(analytics_queries["ventas_por_dia"])
        for dia, total, ingresos in cursor.fetchall():
            print(f"📅 {dia}: {total} ventas | 💰 ${ingresos:.2f}")

        # Productos más vendidos
        print("\n🏆 TOP 5 PRODUCTOS MÁS VENDIDOS")
        print("=" * 50)
        cursor.execute(analytics_queries["productos_mas_vendidos"])
        for nombre, unidades, ingresos in cursor.fetchall():
            print(f"📦 {nombre}: {unidades} uds | 💰 ${ingresos:.2f}")

        # Stock crítico
        print("\n⚠️ ALERTAS DE STOCK")
        print("=" * 50)
        cursor.execute(analytics_queries["stock_critico"])
        for nombre, stock, estado in cursor.fetchall():
            print(f"{estado} {nombre}: {stock} unidades")

        # Promedios
        print("\n📈 PROMEDIOS DE VENTA")
        print("=" * 50)
        cursor.execute(analytics_queries["promedio_ventas"])
        for nombre, prom_uds, prom_ing in cursor.fetchall():
            print(f"📦 {nombre}:")
            print(f"   Promedio uds: {prom_uds}/venta")
            print(f"   Promedio $: ${prom_ing}/venta")

        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [ANALYTICS - ERROR]", e)


def insert_sample_data():
    """
    Inserta datos de ejemplo para pruebas y aprendizaje.
    """
    productos_ejemplo = [
        ("Laptop Gaming", 1299.99, 5),
        ("Monitor 24'", 199.99, 15),
        ("Teclado Mecánico", 89.99, 20),
        ("Mouse Gamer", 49.99, 30),
        ("Auriculares RGB", 79.99, 12),
        ("Webcam HD", 59.99, 8),
        ("Mousepad XL", 19.99, 25),
        ("Hub USB", 29.99, 18),
    ]

    # Ventas con más datos históricos y patrones realistas
    ventas_ejemplo = [
        # Enero 2024
        (1, 2, "2024-01-01"),
        (2, 3, "2024-01-01"),
        (3, 1, "2024-01-02"),
        (4, 2, "2024-01-02"),
        (5, 2, "2024-01-03"),
        (1, 1, "2024-01-03"),
        (2, 2, "2024-01-04"),
        (3, 3, "2024-01-05"),
        # Febrero 2024
        (1, 3, "2024-02-01"),
        (2, 2, "2024-02-01"),
        (4, 4, "2024-02-02"),
        (5, 1, "2024-02-02"),
        (3, 2, "2024-02-03"),
        (1, 1, "2024-02-03"),
        (2, 3, "2024-02-04"),
        (4, 2, "2024-02-05"),
        # Marzo 2024
        (1, 2, "2024-03-01"),
        (5, 3, "2024-03-01"),
        (2, 2, "2024-03-02"),
        (3, 4, "2024-03-02"),
        (4, 1, "2024-03-03"),
        (1, 2, "2024-03-03"),
        (5, 2, "2024-03-04"),
        (2, 1, "2024-03-05"),
        # Ventas recientes con más frecuencia
        (1, 3, "2024-03-15"),
        (2, 2, "2024-03-15"),
        (3, 2, "2024-03-16"),
        (4, 3, "2024-03-16"),
        (5, 1, "2024-03-17"),
        (1, 2, "2024-03-17"),
        (2, 4, "2024-03-18"),
        (3, 1, "2024-03-18"),
        (4, 2, "2024-03-19"),
        (5, 3, "2024-03-19"),
        (1, 1, "2024-03-20"),
        (2, 2, "2024-03-20"),
        # Últimos días con patrón de alta demanda
        (3, 3, "2024-03-21"),
        (4, 4, "2024-03-21"),
        (5, 2, "2024-03-22"),
        (1, 3, "2024-03-22"),
        (2, 3, "2024-03-23"),
        (3, 2, "2024-03-23"),
        (4, 3, "2024-03-24"),
        (5, 4, "2024-03-24"),
        (1, 2, "2024-03-25"),
        (2, 3, "2024-03-25"),
    ]

    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()

        # Limpiar datos existentes
        cursor.execute("TRUNCATE TABLE ventas RESTART IDENTITY CASCADE")
        cursor.execute("TRUNCATE TABLE productos RESTART IDENTITY CASCADE")

        # Insertar productos
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
            productos_ejemplo,
        )

        # Insertar ventas
        cursor.executemany(
            """
            INSERT INTO ventas (producto_id, cantidad, fecha_venta) 
            VALUES (%s, %s, %s::timestamp)
            """,
            ventas_ejemplo,
        )

        conn.commit()
        print("✅ Datos de ejemplo insertados correctamente")

        # Mostrar resumen
        print("\n📊 Resumen de datos insertados:")
        print(f"- Productos: {len(productos_ejemplo)}")
        print(f"- Ventas registradas: {len(ventas_ejemplo)}")
        print("- Período: Enero 2024 - Marzo 2024")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Error al insertar datos de ejemplo:", e)


def generate_advanced_analytics():
    """
    Genera reportes avanzados de ventas e inventario.

    📊 Análisis de Consultas:
    ----------------------
    1. Tendencia de ventas:
       - GROUP BY con funciones temporales
       - Cálculo de métricas agregadas

    2. Rentabilidad:
       - JOIN entre productos y ventas
       - Cálculos financieros básicos

    🤔 Preguntas para Reflexionar:
    ---------------------------
    1. ¿Qué otros análisis serían útiles?
    2. ¿Cómo podríamos mejorar el rendimiento?
    3. ¿Qué insights de negocio podemos obtener?
    """
    advanced_queries = {
        "tendencia_ventas": """
            SELECT 
                DATE_TRUNC('day', fecha_venta) as dia,
                COUNT(*) as total_ventas,
                SUM(v.cantidad * p.precio) as ingresos,
                ROUND(AVG(v.cantidad * p.precio), 2) as ticket_promedio
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
            GROUP BY dia
            ORDER BY dia DESC;
        """,
        "rentabilidad_productos": """
            SELECT 
                p.nombre,
                p.precio,
                COUNT(v.id) as veces_vendido,
                SUM(v.cantidad) as unidades_vendidas,
                SUM(v.cantidad * p.precio) as ingresos_totales,
                ROUND(SUM(v.cantidad * p.precio) / NULLIF(COUNT(v.id), 0), 2) as ingreso_por_venta
            FROM productos p
            LEFT JOIN ventas v ON p.id = v.producto_id
            GROUP BY p.id, p.nombre, p.precio
            ORDER BY ingresos_totales DESC NULLS LAST;
        """,
        "inventario_valor": """
            SELECT 
                SUM(stock * precio) as valor_total_inventario,
                ROUND(AVG(stock * precio), 2) as valor_promedio_producto,
                COUNT(CASE WHEN stock < 10 THEN 1 END) as productos_stock_bajo
            FROM productos;
        """,
    }

    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()

        print("\n📊 ANÁLISIS AVANZADO DE VENTAS E INVENTARIO")
        print("=" * 60)

        # Tendencia de ventas
        cursor.execute(advanced_queries["tendencia_ventas"])
        print("\n📈 TENDENCIA DE VENTAS POR DÍA")
        print("-" * 60)
        for dia, total, ingresos, ticket in cursor.fetchall():
            print(f"📅 {dia.strftime('%Y-%m-%d')}:")
            print(
                f"   Ventas: {total} | 💰 ${ingresos:.2f} | 🎫 Ticket promedio: ${ticket}"
            )

        # Rentabilidad de productos
        cursor.execute(advanced_queries["rentabilidad_productos"])
        print("\n💹 RENTABILIDAD POR PRODUCTO")
        print("-" * 60)
        for nombre, precio, veces, uds, ingresos, promedio in cursor.fetchall():
            print(f"📦 {nombre}")
            print(f"   Precio: ${precio:.2f} | Vendido: {veces} veces")
            print(f"   Unidades: {uds or 0} | Ingresos: ${ingresos or 0:.2f}")
            print(f"   Promedio por venta: ${promedio or 0:.2f}")

        # Valor del inventario
        cursor.execute(advanced_queries["inventario_valor"])
        valor = cursor.fetchone()
        print("\n💎 VALOR DEL INVENTARIO")
        print("-" * 60)
        print(f"📊 Valor total: ${valor[0]:.2f}")
        print(f"📈 Promedio por producto: ${valor[1]:.2f}")
        print(f"⚠️ Productos en stock bajo: {valor[2]}")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ [ANALYTICS ERROR]:", e)


def generate_projections():
    """
    Genera proyecciones de ventas basadas en datos históricos.

    📊 Análisis Predictivo Simple:
    ---------------------------
    - Proyección lineal de ventas
    - Estimación de stock necesario
    - Predicción de ingresos
    """
    projection_queries = {
        "tendencia_mensual": """
            WITH datos_mensuales AS (
                SELECT 
                    DATE_TRUNC('month', fecha_venta) as mes,
                    SUM(v.cantidad * p.precio) as ingresos,
                    COUNT(*) as total_ventas,
                    SUM(v.cantidad) as unidades_vendidas
                FROM ventas v
                JOIN productos p ON v.producto_id = p.id
                GROUP BY mes
                ORDER BY mes
            )
            SELECT 
                mes,
                ingresos,
                unidades_vendidas,
                ROUND(AVG(ingresos) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) as tendencia_ingresos,
                ROUND(AVG(unidades_vendidas) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) as tendencia_unidades
            FROM datos_mensuales;
        """,
        "proyeccion_productos": """
            WITH datos_producto AS (
                SELECT 
                    p.id,
                    p.nombre,
                    p.stock,
                    COUNT(v.id) as frecuencia_ventas,
                    COALESCE(SUM(v.cantidad), 0) as total_vendido,
                    COALESCE(AVG(v.cantidad), 0) as promedio_por_venta,
                    COUNT(DISTINCT DATE_TRUNC('day', v.fecha_venta)) as dias_con_ventas,
                    (SELECT COUNT(DISTINCT DATE_TRUNC('day', fecha_venta)) FROM ventas) as total_dias
                FROM productos p
                LEFT JOIN ventas v ON p.id = v.producto_id
                GROUP BY p.id, p.nombre, p.stock
            )
            SELECT 
                nombre,
                stock,
                ROUND(promedio_por_venta, 2) as venta_promedio,
                ROUND(total_vendido / NULLIF(total_dias, 0), 2) as ventas_por_dia,
                ROUND(stock / NULLIF(total_vendido / NULLIF(total_dias, 0), 0), 0) as dias_restantes_stock,
                CASE 
                    WHEN stock / NULLIF(total_vendido / NULLIF(total_dias, 0), 0) < 7 THEN '🚨 Crítico'
                    WHEN stock / NULLIF(total_vendido / NULLIF(total_dias, 0), 0) < 14 THEN '⚠️ Atención'
                    ELSE '✅ Normal'
                END as estado_proyectado
            FROM datos_producto
            WHERE total_vendido > 0
            ORDER BY dias_restantes_stock ASC;
        """,
    }

    try:
        conn = get_inventory_connection()
        cursor = conn.cursor()

        # Tendencia mensual
        print("\n📈 TENDENCIAS Y PROYECCIONES")
        print("=" * 70)
        cursor.execute(projection_queries["tendencia_mensual"])
        print("\n📅 ANÁLISIS MENSUAL:")
        print("-" * 70)
        for mes, ingresos, unidades, tend_ing, tend_unid in cursor.fetchall():
            print(f"📆 {mes.strftime('%B %Y')}:")
            print(f"   💰 Ingresos: ${ingresos:.2f} | 📦 Unidades: {unidades}")
            print(f"   📈 Tendencia ingresos: ${tend_ing:.2f}")
            print(f"   📊 Tendencia unidades: {tend_unid:.1f}")
            print("-" * 50)

        # Proyección por producto
        print("\n🔮 PROYECCIÓN DE INVENTARIO")
        print("-" * 70)
        cursor.execute(projection_queries["proyeccion_productos"])
        for nombre, stock, prom, diario, dias, estado in cursor.fetchall():
            print(f"\n📦 {nombre}")
            print(f"   Stock actual: {stock} unidades")
            print(f"   Venta promedio: {prom:.1f} unidades por venta")
            print(f"   Venta diaria: {diario:.1f} unidades")
            if dias is not None:
                print(f"   {estado} - Stock dura aprox. {dias:.0f} días")
            else:
                print(f"   ℹ️ Datos insuficientes para proyección")

        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [PROJECTIONS ERROR]:", e)


def main_inventory_menu():
    """
    Menú principal del sistema.

    🎓 Nota Educativa:
    ---------------
    Este sistema simula un entorno real de negocio.
    Analiza cómo cada opción del menú corresponde a
    una necesidad empresarial específica.

    📝 Ejercicios de Análisis:
    -----------------------
    1. ¿Qué otras opciones serían útiles?
    2. ¿Cómo mejorarías la interfaz?
    3. ¿Qué validaciones adicionales agregarías?
    """
    while True:
        print("\n=== 🏪 SISTEMA DE INVENTARIO Y ANALYTICS ===")
        print("1) Crear tablas")
        print("2) Insertar datos de ejemplo ✨")
        print("3) Gestión de Productos:")
        print("   3.1) Registrar producto")
        print("   3.2) Ver productos")
        print("4) Gestión de Ventas:")
        print("   4.1) Registrar venta")
        print("   4.2) Ver ventas")
        print("5) Analytics:")
        print("   5.1) Ver analytics básicos")
        print("   5.2) Ver analytics avanzados 📊")
        print("   5.3) Ver proyecciones 🔮")
        print("6) Salir")

        opcion = input("\nElige una opción: ")

        if opcion == "1":
            create_inventory_tables()
        elif opcion == "2":
            insert_sample_data()
        elif opcion == "3.1":
            insert_product()
        elif opcion == "3.2":
            view_products()
        elif opcion == "4.1":
            insert_sale()
        elif opcion == "4.2":
            view_sales()
        elif opcion == "5.1":
            generate_analytics()
        elif opcion == "5.2":
            generate_advanced_analytics()
        elif opcion == "5.3":
            generate_projections()
        elif opcion == "6":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")


def main():
    main_inventory_menu()


if __name__ == "__main__":
    main()
