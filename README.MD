# 🐘 Sistema de Gestión de Alumnos - PostgreSQL (Neon)

Aplicación CLI para gestionar alumnos usando PostgreSQL serverless con Neon.

## ⚡ Requisitos Previos

1. **Cuenta en Neon.tech**
   - Crear cuenta en [Neon](https://neon.tech)
   - Crear un nuevo proyecto
   - Obtener credenciales de conexión

2. **Dependencias Python**
```bash
pip install psycopg2-binary
```

## 🔧 Configuración

Modifica las siguientes variables en `main.py`:
```python
DB_HOST = "tu-endpoint.neon.tech"
DB_PORT = 5432
DB_NAME = "tu-base-de-datos"
DB_USER = "tu-usuario"
DB_PASSWORD = "tu-contraseña"
```

## 🚀 Funcionalidades

1. **Gestión de Tabla** 📋
   - Crear tabla 'alumnos' en Neon
   - Estructura optimizada para PostgreSQL

2. **Gestión de Alumnos**
   - ✨ CREATE: Agregar nuevos alumnos
   - 🔍 READ: Consultar lista de alumnos
   - 📝 UPDATE: Modificar nombres
   - 🗑️ DELETE: Eliminar registros

## 📖 Uso Básico

1. **Iniciar el programa:**
```bash
python main.py
```

2. **Menú de Opciones:**
```
=================================
    📚 MENÚ PRINCIPAL (Neon)     
=================================
1) Crear tabla 'alumnos'
2) Insertar registro (CREATE)
3) Ver registros (READ)
4) Actualizar registro (UPDATE)
5) Eliminar registro (DELETE)
6) Salir
```

## 📌 Notas Importantes

- La conexión es segura mediante SSL (proporcionado por Neon)
- Persistencia de datos garantizada en la nube
- Backups automáticos gestionados por Neon
- Escalabilidad serverless

## ⚠️ Advertencias

- No uses las credenciales directamente en el código en producción
- Considera usar variables de entorno
- Mantén seguros tus datos de conexión

## 🆘 Solución de Problemas

1. **Error de Conexión**
   - Verifica las credenciales de Neon
   - Confirma que tu IP esté permitida
   - Revisa la conexión a internet

2. **Error en Operaciones**
   - Verifica los permisos de usuario
   - Confirma que la tabla existe
   - Revisa el formato de los datos

## 💡 Tips de Uso

- Guarda los IDs de los registros importantes
- Usa emails únicos para los alumnos
- Realiza backups periódicos
- Monitorea el uso en el dashboard de Neon

¡Disfruta de tu aplicación con PostgreSQL en la nube! 🚀