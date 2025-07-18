# src/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings # Importamos el objeto settings de tu configuración

# Define el motor de la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    # La opción connect_args={"check_same_thread": False} es necesaria para SQLite
    # porque por defecto SQLite permite que solo un hilo interactúe con la conexión.
    # Para otros motores de DB (PostgreSQL, MySQL, etc.), esto no es necesario y puede omitirse.
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    # echo=True # Descomenta para ver las sentencias SQL en la consola (útil para depurar)
)

# Crea una clase SessionLocal.
# Cada instancia de SessionLocal será una sesión de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos declarativos de SQLAlchemy.
Base = declarative_base()

# Función de dependencia para FastAPI para obtener una sesión de base de datos.
def get_db():
    db = SessionLocal()
    try:
        yield db # Proporciona la sesión de DB a la ruta de FastAPI
    finally:
        db.close() # Cierra la sesión después de que se usa (importante para liberar recursos)

# Función para crear todas las tablas definidas en tus modelos (si no existen).
# Normalmente llamas a esto al inicio de tu aplicación (ej. en main.py o un script de inicialización).
def create_db_tables():
    Base.metadata.create_all(bind=engine)