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

# -----------------------------------------------------------------
# CREDENCIALES DE CONEXIÓN (Hardcodeadas, NO recomendado en prod)
# -----------------------------------------------------------------
DB_HOST = "TU_ENDPOINT_NEON"       # Por ejemplo: "ep-floral-fox-xxxxxx.us-east-2.aws.neon.tech"
DB_PORT = 5432                     # El puerto de Neon (normalmente 5432)
DB_NAME = "TU_BASE_DE_DATOS"       # Por ejemplo: "main" o el que hayas creado
DB_USER = "TU_USUARIO_NEON"        # Por ejemplo: "user"
DB_PASSWORD = "TU_CONTRASEÑA_NEON" # Por ejemplo: "password"

def get_connection():
    """
    Devuelve una conexión a la base de datos PostgreSQL en Neon.
    """
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def create_table():
    """
    Crea la tabla 'alumnos' en la base de datos, si no existe.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS alumnos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        carrera VARCHAR(100)
    );
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ [OK] Tabla 'alumnos' creada (o ya existe).")
    except Exception as e:
        print("❌ [ERROR] No se pudo crear la tabla:", e)

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
        cursor.execute(insert_query, (nombre, email, carrera))
        conn.commit()
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
        cursor.execute(select_query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if rows:
            print("\n📃 [READ] Registros en la tabla 'alumnos':")
            for row in rows:
                print(f"  🔑 ID: {row[0]} | 🏷️ Nombre: {row[1]} | 📧 Email: {row[2]} | 🎓 Carrera: {row[3]}")
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
        cursor.execute(update_query, (nuevo_nombre, alumno_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ [UPDATE] Alumno con ID={alumno_id} actualizado a nombre='{nuevo_nombre}'.")
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
        cursor.execute(delete_query, (alumno_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ [DELETE] Alumno con ID={alumno_id} eliminado correctamente.")
        else:
            print(f"⚠️ [DELETE] No se encontró un alumno con ID={alumno_id}.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ [DELETE - ERROR]", e)

def main_menu():
    """
    Muestra el menú principal de la aplicación y maneja la interacción con el usuario.
    """
    while True:
        print("=================================")
        print("    📚 MENÚ PRINCIPAL (Neon)     ")
        print("=================================")
        print("1) Crear tabla 'alumnos'")
        print("2) Insertar registro (CREATE)")
        print("3) Ver registros (READ)")
        print("4) Actualizar registro (UPDATE)")
        print("5) Eliminar registro (DELETE)")
        print("6) Salir")
        print("=================================")

        opcion = input("Elige una opción (1-6): ")

        if opcion == "1":
            create_table()
        elif opcion == "2":
            insert_data()
        elif opcion == "3":
            fetch_data()
        elif opcion == "4":
            update_data()
        elif opcion == "5":
            delete_data()
        elif opcion == "6":
            print("\n👋 Saliendo de la aplicación. ¡Hasta luego y sigue aprendiendo! 🚀")
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
