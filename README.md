# Notiz-App

Eine kleine Fullstack-App zum Verwalten von Notizen.  
Projekt besteht aus **Frontend (React + TypeScript)** und **Backend (Python + FastAPI)**.

## Features
- Notizen erstellen, bearbeiten und löschen
- Validierung: leere Texte werden blockiert
- Datenbank angebunden
- Docker-Support integriert

## Projektstruktur

Backend/ → Python FastAPI Backend
Frontend/ → React + TypeScript Frontend
tests/ → Tests


## Installation & Start

### Backend starten
```bash
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend starten
cd Frontend
npm install
npm run dev

Mit Docker starten
docker build -t notiz-app .
docker run -p 8000:8000 notiz-app

Autor

👤 Sameh Hamdalla


---

### 3. Commit & Push
Nachdem du die Datei erstellt hast:
```bash
git add README.md
git commit -m "README hinzugefügt"
git push origin main


