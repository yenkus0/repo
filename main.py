from database.connection import Base, engine
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

# Modèles
from app.services.animals.models import Animal
from app.services.auth.models import User
from app.services.enclosures.models import Enclosure
from app.services.staff.models import Staff

# Routers
from app.services.animals.routers import animal_router
from app.services.auth.routers import auth_router
from app.services.enclosures.routers import enclosure_router
from app.services.staff.routers import staff_router

app = FastAPI(title="RanchSmart API")

# --- Création des tables ---
def create_db_tables():
    print("Création des tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès !")
    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")

create_db_tables()

# --- CHEMINS STATIQUES ---
STATIC_DIR = Path(__file__).parent / "app" / "static"
ASSETS_DIR = STATIC_DIR / "assets"
DASHBOARD_DIR = STATIC_DIR / "template" / "pages" / "dashboardUser"

FRONTEND_DIR = Path(__file__).parent / "app" / "static" / "template" / "pages" / "dashboardUser"

# Monte le frontend à la racine
# Dossiers pour images
ANIMALS_IMG_DIR = ASSETS_DIR / "animals"
STAFF_IMG_DIR = ASSETS_DIR / "staff_profiles"

os.makedirs(ANIMALS_IMG_DIR, exist_ok=True)
os.makedirs(STAFF_IMG_DIR, exist_ok=True)

# --- MONTAGE DES FICHIERS STATIQUES ---
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
app.mount("/dashboardUser", StaticFiles(directory=DASHBOARD_DIR), name="dashboard")

# --- FONCTION DE LECTURE SÉCURISÉE ---
def read_html_file(file_path: Path) -> HTMLResponse:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content=f"<h1>404</h1><p>Fichier non trouvé : {file_path.name}</p>",
            status_code=404
        )

# --- ROUTES PAGES ---
@app.get("/", response_class=HTMLResponse)
def landing_page():
    file_path = STATIC_DIR / "template" / "pages" / "landing" / "landing.html"
    return read_html_file(file_path)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_index():
    file_path = DASHBOARD_DIR / "index.html"
    return read_html_file(file_path)

@app.get("/dashboard/animaux", response_class=HTMLResponse)
def dashboard_animals():
    file_path = DASHBOARD_DIR / "cards.html"
    return read_html_file(file_path)

@app.get("/dashboard/staff", response_class=HTMLResponse)
def dashboard_staff():
    file_path = DASHBOARD_DIR / "staff.html"
    return read_html_file(file_path)

# --- ROUTERS API ---
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(animal_router, prefix="/animals", tags=["Animaux"])
app.include_router(enclosure_router, prefix="/enclosures", tags=["Enclos"])
app.include_router(staff_router, prefix="/staff", tags=["Staff"])

# --- LANCEMENT ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENV") == "dev"
    )