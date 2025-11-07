from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.config import settings  # ← OK

# UTILISE settings.DATABASE_URL (pas SQLALCHEMY...)
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# AJOUTE UNE VÉRIFICATION
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL n'est pas définie dans les variables d'environnement")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()