#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════╗
║                 CLI Interactivo con SQLite                ║
║       Aprende CRUD (Create, Read, Update, Delete)         ║
║         de forma fácil, divertida y super cool 🎉          ║
╚════════════════════════════════════════════════════════════╝

Proyecto guiado por Alejandro López (profesor).
¡Este script está pensado para que aprendas los fundamentos
de las bases de datos usando SQLite y Python!

-------------------------------------------------------------
FUNCIONALIDADES
-------------------------------------------------------------
1. Crear la base de datos y la tabla 'alumnos'.
2. Insertar registros (CREATE).
3. Ver registros (READ).
4. Actualizar el nombre de un registro (UPDATE).
5. Eliminar un registro (DELETE).
6. Salir del programa.

-------------------------------------------------------------
FLUJO DE LA APLICACIÓN
-------------------------------------------------------------
1. El usuario ejecuta en la terminal:
       python cli_app.py
2. El programa muestra un MENÚ PRINCIPAL en la consola.
3. El usuario elige una opción (1-6).
4. Según la opción seleccionada:
   - Se llama a una función que maneja la operación CRUD (Create, Read, Update, Delete).
   - La función se conecta a la base de datos 'alumnos_cli.db'
     (si no existe, se crea al momento).
   - Se realiza la operación SQL correspondiente
     (CREATE TABLE, INSERT, SELECT, UPDATE, DELETE).
5. El programa muestra en pantalla el resultado de la operación.
6. El menú vuelve a aparecer para permitir más operaciones.
7. Cuando el usuario elige "6) Salir", el programa finaliza.

-------------------------------------------------------------
¡A PROGRAMAR!
-------------------------------------------------------------
No necesitas instalar nada extra. Python ya incluye SQLite.
Haz tus primeros pasos en el mundo de las bases de datos de
manera sencilla, práctica y entretenida.

Autor: Alejandro López
Fecha: 2025
"""

import sqlite3  # Librería estándar de Python para usar bases de datos SQLite
import os  # Para gestionar archivos (por si quisieras eliminar o comprobar la existencia del .db)

# Nombre del archivo de base de datos que crearemos/usaremos
DB_NAME = "alumnos_cli.db"


def create_database_and_table(db_path: str) -> None:
    """
    Crea la base de datos (si no existe) y la tabla 'alumnos'.

    Parámetros:
    -----------
    db_path : str
        Ruta o nombre del archivo de la base de datos SQLite.

    ¿Qué hace?
    -----------
    1. Se conecta (o crea) la base de datos db_path.
    2. Crea una tabla 'alumnos' con columnas:
       - id (PRIMARY KEY, autoincremental)
       - nombre (texto obligatorio)
       - email (texto obligatorio)
       - carrera (texto opcional)
    3. Si la tabla ya existe, no pasa nada.
    4. Cierra la conexión.

    ¡Listo para almacenar datos de nuestros alumnos!
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            carrera TEXT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        cursor.close()
        conn.close()
        print("✅ [OK] Base de datos y tabla 'alumnos' creadas (o ya existen).")
    except Exception as e:
        print("❌ [ERROR] No se pudo crear la base de datos o la tabla:", e)


def insert_data(db_path: str) -> None:
    """
    Inserta un nuevo alumno en la tabla 'alumnos' pidiendo los datos
    a través de la consola de forma interactiva.

    Parámetros:
    -----------
    db_path : str
        Ruta o nombre del archivo de la base de datos SQLite.

    ¿Qué hace?
    -----------
    1. Pide al usuario:
       - Nombre
       - Email
       - Carrera
    2. Inserta un nuevo registro en la tabla 'alumnos'.
    3. Muestra un mensaje de confirmación o error.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n👨‍🎓 Vamos a registrar un alumno. Por favor, ingresa los datos:")
    nombre = input("  🏷️ Nombre: ")
    email = input("  📧 Email: ")
    carrera = input("  🎓 Carrera: ")

    query = """
    INSERT INTO alumnos (nombre, email, carrera)
    VALUES (?, ?, ?);
    """
    try:
        cursor.execute(query, (nombre, email, carrera))
        conn.commit()
        print("✅ [INSERT] Registro insertado con éxito.")
    except Exception as e:
        print("❌ [INSERT - ERROR]", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def fetch_data(db_path: str) -> None:
    """
    Muestra todos los registros actuales en la tabla 'alumnos'.

    Parámetros:
    -----------
    db_path : str
        Ruta o nombre del archivo de la base de datos SQLite.

    ¿Qué hace?
    -----------
    1. Ejecuta un SELECT para obtener todos los registros.
    2. Imprime cada registro con sus valores (id, nombre, email, carrera).
    3. Si no hay registros, informa que la tabla está vacía.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT id, nombre, email, carrera FROM alumnos;"
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        print("\n📃 [READ] Registros en la tabla 'alumnos':")
        for row in rows:
            print(f"  🔑 ID: {row[0]} | 🏷️ Nombre: {row[1]} | 📧 Email: {row[2]} | 🎓 Carrera: {row[3]}")
    else:
        print("⚠️ [READ] No hay registros en la tabla.")

    cursor.close()
    conn.close()
    print()  # Salto de línea adicional para limpieza visual


def update_data(db_path: str) -> None:
    """
    Actualiza el nombre de un alumno en la tabla 'alumnos' según el ID.

    Parámetros:
    -----------
    db_path : str
        Ruta o nombre del archivo de la base de datos SQLite.

    ¿Qué hace?
    -----------
    1. Pide el ID del alumno a actualizar.
    2. Pide el nuevo nombre.
    3. Realiza un UPDATE en la tabla 'alumnos' para ese ID.
    4. Si el ID no existe, lo notifica.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n🔄 Vamos a actualizar un alumno.")
    alumno_id = input("  Ingresa el ID del alumno a actualizar: ")
    nuevo_nombre = input("  Ingresa el nuevo nombre: ")

    query = """
    UPDATE alumnos
    SET nombre = ?
    WHERE id = ?;
    """
    try:
        cursor.execute(query, (nuevo_nombre, alumno_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ [UPDATE] El alumno con ID={alumno_id} ahora se llama '{nuevo_nombre}'.")
        else:
            print(f"⚠️ [UPDATE] No se encontró un alumno con ID={alumno_id}.")
    except Exception as e:
        print("❌ [UPDATE - ERROR]", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def delete_data(db_path: str) -> None:
    """
    Elimina un alumno de la tabla 'alumnos' según su ID.

    Parámetros:
    -----------
    db_path : str
        Ruta o nombre del archivo de la base de datos SQLite.

    ¿Qué hace?
    -----------
    1. Pide el ID del alumno a eliminar.
    2. Realiza un DELETE sobre la tabla 'alumnos' para ese ID.
    3. Notifica si el alumno se eliminó o si no existía.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n🗑️ Vamos a eliminar un alumno de la BD.")
    alumno_id = input("  Ingresa el ID del alumno a eliminar: ")

    query = "DELETE FROM alumnos WHERE id = ?;"
    try:
        cursor.execute(query, (alumno_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ [DELETE] Alumno con ID={alumno_id} eliminado correctamente.")
        else:
            print(f"⚠️ [DELETE] No se encontró un alumno con ID={alumno_id}.")
    except Exception as e:
        print("❌ [DELETE - ERROR]", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def main_menu():
    """
    Muestra el menú principal de la aplicación y gestiona
    la interacción con el usuario.

    ¿Qué hace?
    -----------
    1. Despliega un menú con opciones numeradas (1 a 6).
    2. Espera que el usuario ingrese un número.
    3. Llama a la función correspondiente según la elección.
    4. Continúa hasta que el usuario elija la opción de salir (6).
    """
    while True:
        print("=================================")
        print("      📚 MENÚ PRINCIPAL 📚       ")
        print("=================================")
        print("1) Crear base de datos y tabla")
        print("2) Insertar registro (CREATE)")
        print("3) Ver registros (READ)")
        print("4) Actualizar registro (UPDATE)")
        print("5) Eliminar registro (DELETE)")
        print("6) Salir")
        print("=================================")

        opcion = input("Elige una opción (1-6): ")

        if opcion == "1":
            create_database_and_table(DB_NAME)
        elif opcion == "2":
            insert_data(DB_NAME)
        elif opcion == "3":
            fetch_data(DB_NAME)
        elif opcion == "4":
            update_data(DB_NAME)
        elif opcion == "5":
            delete_data(DB_NAME)
        elif opcion == "6":
            print("\n👋 Saliendo de la aplicación. ¡Hasta luego y sigue aprendiendo! 🚀")
            break
        else:
            print("❌ [ERROR] Opción inválida. Intenta de nuevo.")


def main():
    """
    Punto de entrada principal del programa.
    Muestra el menú y gestiona la aplicación en bucle
    hasta que el usuario decida salir.

    Si deseas reiniciar la base de datos en cada ejecución,
    descomenta las siguientes líneas:

    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("💣 Se ha eliminado la base de datos anterior para un inicio limpio.")
    """
    # if os.path.exists(DB_NAME):
    #     os.remove(DB_NAME)
    #     print("💣 Se ha eliminado la base de datos anterior para un inicio limpio.")

    main_menu()


if __name__ == "__main__":
    main()
