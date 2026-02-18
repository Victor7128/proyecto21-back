# Hotel API 🏨

Backend REST API para gestión hotelera, desarrollado con **FastAPI** y **Azure SQL Server**.

---

## Requisitos

- Python 3.11+
- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- Acceso a una instancia de Azure SQL Server

---

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd proyecto21-back

# Crear y activar entorno virtual
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DB_SERVER=tu-servidor.database.windows.net
DB_NAME=proyecto
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_PORT=1433

# JWT
SECRET_KEY=genera-una-clave-con-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# App
APP_NAME=Hotel API
DEBUG=True
```

> **Importante:** Agrega tu IP en el firewall de Azure SQL antes de conectarte.  
> Azure Portal → SQL Server → Networking → Add firewall rule.

---

## Base de datos

El esquema completo se encuentra en `esquemahotelevo.sql`. Ejecútalo en tu instancia de Azure SQL para crear todas las tablas, índices y relaciones.

Los stored procedures están en `stored_procedures.sql`.

### Datos semilla

Los usuarios de prueba tienen las siguientes credenciales:

| Nombre | Email | Password | Rol |
|--------|-------|----------|-----|
| Luis Fernando Cáceres | luis.caceres@hotel.com | hash_admin_001 | Administrador |
| Sandra Milagros Vega | sandra.vega@hotel.com | hash_recep_002 | Recepcionista |
| Jorge Enrique Díaz | jorge.diaz@hotel.com | hash_conserj_003 | Conserjería |
| Patricia Susana León | patricia.leon@hotel.com | hash_conta_004 | Contabilidad |
| Miguel Ángel Torres | miguel.torres@hotel.com | hash_superv_005 | Supervisor |

---

## Levantar el servidor

```bash
# Modo desarrollo
fastapi dev main.py

# Modo producción
fastapi run main.py
```

El servidor corre en `http://127.0.0.1:8000`.  
Documentación interactiva disponible en `http://127.0.0.1:8000/docs`.

---

## Autenticación

### POST `/auth/login`

Devuelve un JWT Bearer token.

**Request body:**
```json
{
  "email": "luis.caceres@hotel.com",
  "password": "hash_admin_001"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Para usar el token en rutas protegidas, incluye el header:
```
Authorization: Bearer <access_token>
```

---

## Verificar conexión a la BD

```bash
python test_db.py
```

---

## Estructura del proyecto

```
proyecto21-back/
├── main.py
├── config.py               # Variables de entorno con pydantic-settings
├── database.py             # Conexión a Azure SQL via pyodbc
├── dependencies.py         # Dependencias de FastAPI (get_db, etc.)
├── exceptions.py           # Excepciones personalizadas
├── routers/
│   └── auth_router.py
├── schemas/
│   └── auth.py
├── services/
│   ├── auth_service.py
│   ├── personal_service.py
│   └── utils.py
├── esquemahotelevo.sql
├── stored_procedures.sql
├── .env                    # No commitear
└── requirements.txt
```

---

## Notas de desarrollo

- El proyecto está en etapa de **desarrollo**. Las contraseñas en la BD son texto plano convertido a `VARBINARY`; `verify_password` maneja ambos casos (bcrypt real y texto plano).
- Para nuevos usuarios creados vía API, las contraseñas se hashean automáticamente con **bcrypt**.
- pyodbc usa pooling interno por defecto. Para mayor escala considerar SQLAlchemy Core o aioodbc.