# main.py

from fastapi import FastAPI
from config import setup_cors  # eigene CORS-Einstellungen
from routes_db import router as db_router  # Router für die echte DB-Version


# 🟢 App erstellen
app = FastAPI(
    title="Notiz-App Backend",  # Titel der App
    description="Backend nur mit DB-Routen",  # Beschreibung
    version="1.0.0",  # Versionsnummer
)

# 🟢 CORS Setup (Frontend darf zugreifen)
setup_cors(app)

# 🟢 Nur noch DB-Routen einbinden
# → /db/... = dauerhafte Notizen in SQLite-Datenbank
app.include_router(db_router, prefix="/db", tags=["DB Notes"])


# ℹ️ Hinweis:
# - Memory-Router (In-Memory Notizen) ist entfernt
# - Es gibt jetzt nur noch die Routen mit DB-Anbindung
# - Vorteil: Alle Notizen bleiben nach Neustart erhalten


# Mit GET fragen wir nur Daten ab (lesen)
# Warum meherer Routen:
# weil die App meherer Dinge machen soll und hinter jeder Route steckt eine Funktion, die was bestimmtes machen kann
# Route /docs ist die Swagger UI und hier kann man die APP testen => Spielplatz für die Entwickler
# Route / redoc ist eine schön formatierte Dokumentation deiner API => Handbuch für die Entwickler
#
# python -m uvicorn main:app --reload
# http://127.0.0.1:8000/ => zeigt dein "Hallo Welt!"

# http://127.0.0.1:8000/about => zeigt dein "Dies ist meine erste kleine Notiz-App
# http://127.0.0.1:8000/notes/2 => Gibt eine einzelne Notiz anhand der ID zurück

# Was ist from pydantic import BaseModel:
# pydantic ist eine Bibliothek, die mit FastAPI mitkommt.Sie hilft uns dabei,
# Datenmodelle zu definieren und sicherzustellen, dass die Daten, die wir von Benutzern (z. B. per API) bekommen, auch gültig sind.

# Frontend anfangen:
# npm create vite@latest Frontend -- --template react-ts
