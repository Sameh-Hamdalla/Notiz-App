# main.py
from fastapi import FastAPI
from config import setup_cors
from routes import router as memory_router      # Router für die "Demo-Version" (In-Memory Notizen)
from routes_db import router as db_router       # Router für die "echte DB-Version"

# App erstellen
app = FastAPI()

# CORS Setup
setup_cors(app)

# Routen einbinden
app.include_router(memory_router, prefix="/memory", tags=["Memory Notes"])  # → Swagger-Gruppe "Memory Notes"
app.include_router(db_router, prefix="/db", tags=["DB Notes"])              # → Swagger-Gruppe "DB Notes"





# Mit GET fragen wir nur Daten ab (lesen)
# Warum meherer Routen:
# weil die App meherer Dinge machen soll und hinter jeder Route steckt eine Funktion, die was bestimmtes machen kann
# Route /docs ist die Swagger UI und hier kann man die APP testen => Spielplatz für die Entwickler
#Route / redoc ist eine schön formatierte Dokumentation deiner API => Handbuch für die Entwickler
#
#python -m uvicorn main:app --reload
#http://127.0.0.1:8000/ => zeigt dein "Hallo Welt!"

#http://127.0.0.1:8000/about => zeigt dein "Dies ist meine erste kleine Notiz-App
#http://127.0.0.1:8000/notes/2 => Gibt eine einzelne Notiz anhand der ID zurück

# Was ist from pydantic import BaseModel:
#pydantic ist eine Bibliothek, die mit FastAPI mitkommt.Sie hilft uns dabei,
# Datenmodelle zu definieren und sicherzustellen, dass die Daten, die wir von Benutzern (z. B. per API) bekommen, auch gültig sind.

# Frontend anfangen:
#npm create vite@latest Frontend -- --template react-ts
