#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════╗
║             CLI Interactivo con PostgreSQL (Neon)         ║
║       CRUD: Create, Read, Update, Delete con psycopg2     ║
╚════════════════════════════════════════════════════════════╝

Este script se conecta a una base de datos en Neon (serverless
PostgreSQL). Aquí no se usan variables de entorno; las credenciales
están definidas en el código. Para fines de demostración en un
ambiente de aprendizaje, está bien, pero NO se recomienda en
producción.

Operaciones disponibles:
1) Crear tabla 'alumnos'.
2) Insertar registro (CREATE).
3) Ver registros (READ).
4) Actualizar registro (UPDATE).
5) Eliminar registro (DELETE).
6) Salir.

Requisitos:
- Python 3.x
- psycopg2 (se instala con: pip install psycopg2-binary)

Autor: Alejandro López
Fecha: 2025
"""

import psycopg2
import psycopg2.extras
from datetime import datetime

neo =


def get_connection():
    """
    Devuelve una conexión a la base de datos PostgreSQL en Neon.
    """
    return psycopg2.connect(neo)


def print_sql_operation(query: str, params: tuple = None):
    """
    Muestra la operación SQL que se está ejecutando
    """
    print("\n" + "=" * 50)
    print("📝 SQL Query:")
    print("-" * 50)
    # Reemplazar %s con los parámetros reales si existen
    if params:
        for param in params:
            query = query.replace("%s", repr(param), 1)
    print(query)
    print("=" * 50 + "\n")


def create_tables():
    """
    Crea las tablas 'alumnos' y 'operaciones_log' en la base de datos.
    """
    create_tables_query = """
    CREATE TABLE IF NOT EXISTS cursos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        profesor VARCHAR(100) NOT NULL,
        creditos INTEGER DEFAULT 0,
        activo BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS alumnos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        carrera VARCHAR(100),
        curso_id INTEGER REFERENCES cursos(id),
        activo BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS operaciones_log (
        id SERIAL PRIMARY KEY,
        fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        operacion VARCHAR(50) NOT NULL,
        descripcion TEXT,
        usuario TEXT DEFAULT CURRENT_USER,
        tabla TEXT NOT NULL,
        query_ejecutado TEXT,
        detalles JSONB
    );
    """
    print_sql_operation(create_tables_query)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(create_tables_query)
        conn.commit()

        # Agregar log de creación de tablas
        log_operation(
            "CREATE",
            "Creación/verificación de tablas",
            {"tablas": ["alumnos", "operaciones_log", "cursos"]},
        )

        cursor.close()
        conn.close()
        print("✅ [OK] Tablas creadas (o ya existen).")
    except Exception as e:
        print("❌ [ERROR] No se pudieron crear las tablas:", e)


def log_operation(operacion: str, descripcion: str, detalles: dict = None):
    """
    Registra una operación en la tabla de logs.
    """
    insert_log_query = """
    INSERT INTO operaciones_log (operacion, descripcion, tabla, detalles)
    VALUES (%s, %s, %s, %s::jsonb);
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            insert_log_query,
            (
                operacion,
                descripcion,
                "alumnos",
                psycopg2.extras.Json(detalles) if detalles else None,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("⚠️ [LOG - ERROR]", e)


def view_logs():
    """
    Muestra el historial de operaciones realizadas.
    """
    select_query = """
    SELECT fecha_hora, operacion, descripcion, usuario, detalles 
    FROM operaciones_log 
    ORDER BY fecha_hora DESC 
    LIMIT 10;
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(select_query)
        logs = cursor.fetchall()
        cursor.close()
        conn.close()

        if logs:
            print("\n📋 [LOGS] Últimas 10 operaciones:")
            print("=" * 80)
            for log in logs:
                print(f"⏰ {log[0]} | 🔄 {log[1]}")
                print(f"📝 {log[2]}")
                print(f"👤 Usuario: {log[3]}")
                if log[4]:
                    print(f"📊 Detalles: {log[4]}")
                print("-" * 80)
        else:
            print("⚠️ No hay registros en el log.")
    except Exception as e:
        print("❌ [LOGS - ERROR]", e)


def insert_data():
    """
    Inserta un registro en la tabla 'alumnos' pidiendo datos por consola.
    """
    print("\n👨‍🎓 Vamos a registrar un alumno. Ingresa los datos:")
    nombre = input("  🏷️ Nombre: ")
    email = input("  📧 Email: ")
    carrera = input("  🎓 Carrera: ")

    insert_query = """
    INSERT INTO alumnos (nombre, email, carrera)
    VALUES (%s, %s, %s);
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print_sql_operation(insert_query, (nombre, email, carrera))
        cursor.execute(insert_query, (nombre, email, carrera))
        conn.commit()

        # Agregar log
        log_operation(
            "INSERT",
            f"Nuevo alumno registrado: {nombre}",
            {"nombre": nombre, "email": email, "carrera": carrera},
        )

        cursor.close()
        conn.close()
        print("✅ [INSERT] Registro insertado con éxito.")
    except Exception as e:
        print("❌ [INSERT - ERROR]", e)


def fetch_data():
    """
    Muestra todos los registros de la tabla 'alumnos'.
    """
    select_query = "SELECT id, nombre, email, carrera FROM alumnos;"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        print_sql_operation(select_query)
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # Agregar log de consulta
        log_operation(
            "SELECT", "Consulta de todos los registros", {"total_registros": len(rows)}
        )

        cursor.close()
        conn.close()

        if rows:
            print("\n📃 [READ] Registros en la tabla 'alumnos':")
            for row in rows:
                print(
                    f"  🔑 ID: {row[0]} | 🏷️ Nombre: {row[1]} | 📧 Email: {row[2]} | 🎓 Carrera: {row[3]}"
                )
        else:
            print("⚠️ [READ] No hay registros en la tabla.")

    except Exception as e:
        print("❌ [READ - ERROR]", e)


def update_data():
    """
    Actualiza el nombre de un alumno según el ID indicado por consola.
    """
    print("\n🔄 Vamos a actualizar un alumno.")
    alumno_id = input("  Ingresa el ID del alumno a actualizar: ")
    nuevo_nombre = input("  Ingresa el nuevo nombre: ")

    update_query = """
    UPDATE alumnos
    SET nombre = %s
    WHERE id = %s;
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()
        print_sql_operation(update_query, (nuevo_nombre, alumno_id))
        cursor.execute(update_query, (nuevo_nombre, alumno_id))
        conn.commit()
        if cursor.rowcount > 0:
            # Agregar log de actualización
            log_operation(
                "UPDATE",
                f"Actualización de nombre para ID={alumno_id}",
                {"id": alumno_id, "nuevo_nombre": nuevo_nombre},
            )
            print(
                f"✅ [UPDATE] Alumno con ID={alumno_id} actualizado a nombre='{nuevo_nombre}'."
            )
        else:
            print(f"⚠️ [UPDATE] No se encontró un alumno con ID={alumno_id}.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [UPDATE - ERROR]", e)


def delete_data():
    """
    Elimina un alumno de la tabla 'alumnos' según el ID indicado por consola.
    """
    print("\n🗑️ Vamos a eliminar un alumno de la BD.")
    alumno_id = input("  Ingresa el ID del alumno a eliminar: ")

    delete_query = "DELETE FROM alumnos WHERE id = %s;"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        print_sql_operation(delete_query, (alumno_id,))
        cursor.execute(delete_query, (alumno_id,))
        conn.commit()
        if cursor.rowcount > 0:
            # Agregar log de eliminación
            log_operation(
                "DELETE", f"Eliminación de alumno ID={alumno_id}", {"id": alumno_id}
            )
            print(f"✅ [DELETE] Alumno con ID={alumno_id} eliminado correctamente.")
        else:
            print(f"⚠️ [DELETE] No se encontró un alumno con ID={alumno_id}.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [DELETE - ERROR]", e)


def insert_curso():
    """
    Inserta un nuevo curso
    """
    print("\n📚 Registro de nuevo curso:")
    nombre = input("  📖 Nombre del curso: ")
    profesor = input("  👨‍🏫 Profesor: ")
    creditos = input("  ⭐ Créditos: ")

    insert_query = """
    INSERT INTO cursos (nombre, profesor, creditos)
    VALUES (%s, %s, %s)
    RETURNING id, nombre;
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()
        print_sql_operation(insert_query, (nombre, profesor, creditos))
        cursor.execute(insert_query, (nombre, profesor, creditos))
        curso_id, curso_nombre = cursor.fetchone()
        conn.commit()

        log_operation(
            "INSERT",
            f"Nuevo curso registrado: {curso_nombre}",
            {"id": curso_id, "nombre": nombre, "profesor": profesor},
        )

        print(f"✅ [INSERT] Curso '{curso_nombre}' registrado con ID={curso_id}")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [INSERT - ERROR]", e)


def view_cursos():
    """
    Muestra todos los cursos disponibles
    """
    select_query = """
    SELECT c.id, c.nombre, c.profesor, c.creditos, 
           COUNT(a.id) as total_alumnos
    FROM cursos c
    LEFT JOIN alumnos a ON c.id = a.curso_id
    GROUP BY c.id
    ORDER BY c.id;
    """

    print_sql_operation(select_query)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(select_query)
        cursos = cursor.fetchall()

        if cursos:
            print("\n📚 Lista de Cursos:")
            print("=" * 80)
            for curso in cursos:
                print(f"ID: {curso[0]}")
                print(f"📖 Nombre: {curso[1]}")
                print(f"👨‍🏫 Profesor: {curso[2]}")
                print(f"⭐ Créditos: {curso[3]}")
                print(f"👥 Alumnos inscritos: {curso[4]}")
                print("-" * 80)
        else:
            print("⚠️ No hay cursos registrados")

        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [SELECT - ERROR]", e)


def main_menu():
    """
    Muestra el menú principal de la aplicación y maneja la interacción con el usuario.
    """
    while True:
        print("\n=================================")
        print("    📚 MENÚ PRINCIPAL (Neon)     ")
        print("=================================")
        print("1) Crear tablas")
        print("2) Gestión de Cursos:")
        print("   2.1) Registrar nuevo curso")
        print("   2.2) Ver cursos y alumnos")
        print("3) Gestión de Alumnos:")
        print("   3.1) Registrar alumno")
        print("   3.2) Ver alumnos")
        print("   3.3) Actualizar alumno")
        print("   3.4) Eliminar alumno")
        print("4) Ver historial de operaciones")
        print("5) Salir")
        print("=================================")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            create_tables()
        elif opcion == "2.1":
            insert_curso()
        elif opcion == "2.2":
            view_cursos()
        elif opcion == "3.1":
            insert_data()
        elif opcion == "3.2":
            fetch_data()
        elif opcion == "3.3":
            update_data()
        elif opcion == "3.4":
            delete_data()
        elif opcion == "4":
            view_logs()
        elif opcion == "5":
            print("\n👋 ¡Hasta luego! Recuerda revisar los logs para ver qué sucedió.")
            break
        else:
            print("❌ [ERROR] Opción inválida. Intenta de nuevo.")


def main():
    """
    Punto de entrada principal de la aplicación.
    """
    main_menu()


if __name__ == "__main__":
    main()
