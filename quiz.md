
# 🐘 Aplicación CLI Interactiva con PostgreSQL (Neon)

## 📝 Descripción
Este proyecto implementa una interfaz de línea de comandos (CLI) para gestionar una base de datos PostgreSQL alojada en Neon. Permite realizar operaciones CRUD (Create, Read, Update, Delete) sobre registros de alumnos y cursos.

## 🚀 Características
- Gestión completa de alumnos y cursos
- Sistema de logging para auditoría
- Interfaz CLI intuitiva
- Conexión con PostgreSQL en la nube (Neon)

## 📋 Requisitos
- Python 3.x
- psycopg2-binary
- Cuenta en Neon (PostgreSQL serverless)

## 🎯 Quiz de Comprensión

### 🤔 Preguntas

1. **¿Cuál es el propósito principal de este script en Python?**
   - [ ] Crear una interfaz gráfica de usuario
   - [ ] Establecer una conexión con PostgreSQL y realizar operaciones CRUD vía CLI
   - [ ] Desarrollar una aplicación web
   - [ ] Implementar autenticación de usuarios

2. **¿Qué biblioteca se utiliza para manejar PostgreSQL?**
   - [ ] sqlite3
   - [ ] sqlalchemy
   - [ ] psycopg2
   - [ ] django.db

3. **¿Cuál tabla NO se crea en la base de datos?**
   - [ ] cursos
   - [ ] alumnos
   - [ ] operaciones_log
   - [ ] profesores

4. **¿Qué hace la función log_operation?**
   - [ ] Inserta registros en alumnos
   - [ ] Registra operaciones en operaciones_log
   - [ ] Actualiza cursos
   - [ ] Elimina registros

5. **¿Cómo manejar credenciales en producción?**
   - [ ] Definirlas en el código
   - [ ] Usar variables de entorno
   - [ ] Guardarlas en texto plano
   - [ ] No protegerlas

### 🎮 ¿Cómo jugar?
1. Lee cada pregunta cuidadosamente
2. Marca solo UNA respuesta por pregunta
3. Verifica tus respuestas al final
4. ¡Aprende de tus errores!

### ✅ Respuestas Correctas
<details>
<summary>Ver respuestas (¡No hacer trampa! 😉)</summary>

1. b) Establecer una conexión con PostgreSQL y realizar operaciones CRUD vía CLI
2. c) psycopg2
3. d) profesores
4. b) Registra operaciones en operaciones_log
5. b) Usar variables de entorno

</details>

## 🎯 Quiz Avanzado de PostgreSQL y Python

### 📚 Sección 1: Fundamentos de PostgreSQL

1. **¿Qué significa SERIAL en PostgreSQL?**
   - [ ] Es solo un alias para INTEGER
   - [ ] Es un tipo auto-incrementable que crea una secuencia automáticamente
   - [ ] Es un tipo de dato para almacenar texto
   - [ ] Es un índice especial para claves primarias

2. **En la tabla 'alumnos', ¿qué significa la restricción REFERENCES cursos(id)?**
   - [ ] Es una simple sugerencia para el desarrollador
   - [ ] Establece una llave foránea que garantiza integridad referencial
   - [ ] Crea una copia de la tabla cursos
   - [ ] Define un índice de búsqueda

### 🐍 Sección 2: Python y psycopg2

3. **¿Por qué usamos cursor.execute() con parámetros en lugar de string formatting?**
   - [ ] Es más fácil de leer
   - [ ] Mejora el rendimiento
   - [ ] Previene inyección SQL
   - [ ] Es requisito de PostgreSQL

4. **¿Qué sucede si no hacemos conn.commit() después de un INSERT?**
   - [ ] Los datos se guardan automáticamente
   - [ ] PostgreSQL lanza un error
   - [ ] Los cambios se pierden al cerrar la conexión
   - [ ] Los datos quedan en estado pendiente

### 🔧 Sección 3: Arquitectura y Diseño

5. **¿Por qué la tabla operaciones_log usa JSONB para detalles?**
   - [ ] Porque es más rápido que TEXT
   - [ ] Permite almacenar datos estructurados y hacer consultas sobre ellos
   - [ ] Es un requisito de PostgreSQL
   - [ ] Ocupa menos espacio en disco

6. **¿Cuál es la ventaja de usar DEFAULT CURRENT_TIMESTAMP?**
   - [ ] No tiene ventajas significativas
   - [ ] Es más rápido que usar NOW()
   - [ ] Garantiza que cada registro tenga su timestamp de creación automáticamente
   - [ ] Permite modificar el tiempo manualmente

### 🛠 Sección 4: Buenas Prácticas

7. **¿Por qué es importante cerrar el cursor y la conexión?**
   - [ ] No es importante, PostgreSQL lo hace automáticamente
   - [ ] Solo por buenas prácticas
   - [ ] Para liberar recursos y evitar fugas de memoria
   - [ ] Es un requisito de psycopg2

8. **¿Cuál es el propósito del WITH IF NOT EXISTS?**
   - [ ] Mejorar el rendimiento
   - [ ] Evitar errores si la tabla ya existe
   - [ ] Es solo sintaxis opcional
   - [ ] Crear tablas temporales

### 🔍 Sección 5: Debugging y Mantenimiento

9. **¿Cómo podemos monitorear las operaciones en la base de datos?**
   - [ ] Revisando los logs del sistema operativo
   - [ ] No es posible monitorear las operaciones
   - [ ] Consultando la tabla operaciones_log
   - [ ] Usando print statements

10. **¿Qué ventaja ofrece el uso de try-except en las operaciones de BD?**
    - [ ] Ninguna ventaja significativa
    - [ ] Solo mejora la legibilidad
    - [ ] Permite manejar errores de manera controlada y mantener la aplicación funcionando
    - [ ] Es un requisito de Python

### ✨ Bonus: Pregunta de Diseño

11. **¿Por qué la tabla 'cursos' tiene un campo 'activo'?**
    - [ ] Es un campo obligatorio de PostgreSQL
    - [ ] Permite hacer soft deletes sin perder datos históricos
    - [ ] No tiene un propósito específico
    - [ ] Es para mejorar el rendimiento

### 🎮 Instrucciones
1. Tómate tu tiempo para analizar cada pregunta
2. Considera el contexto completo del sistema
3. Piensa en las implicaciones de cada respuesta
4. ¡No te limites a memorizar, comprende!




## 📚 Recursos Adicionales
- [Documentación de PostgreSQL](https://www.postgresql.org/docs/)
- [Python psycopg2](https://www.psycopg.org/docs/)
- [Neon - PostgreSQL Serverless](https://neon.tech/)

## 👨‍💻 Autor
Alejandro López © 2025

