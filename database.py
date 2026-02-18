import pyodbc
from config import get_settings

settings = get_settings()

_CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER=tcp:{settings.DB_SERVER},{settings.DB_PORT};"
    f"DATABASE={settings.DB_NAME};"
    f"UID={settings.DB_USER};"
    f"PWD={settings.DB_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "MultipleActiveResultSets=False;"
    "Connection Timeout=30;"
)


def get_connection() -> pyodbc.Connection:
    """
    Abre y devuelve una conexión nueva a Azure SQL.
    Se usa como dependencia en FastAPI (ver dependencies.py):

        def get_db():
            conn = get_connection()
            try:
                yield conn
            finally:
                conn.close()

    No usamos pool externo porque pyodbc tiene pool interno por defecto
    (pooling=True en el driver). Para apps de mayor escala se puede
    reemplazar por SQLAlchemy Core o aioodbc.
    """
    return pyodbc.connect(_CONNECTION_STRING)


def test_connection() -> bool:
    """
    Verifica que la conexión funcione.
    Llamar desde main.py al iniciar la app (evento startup).
    Devuelve True si OK, lanza excepción si falla.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    conn.close()
    return True