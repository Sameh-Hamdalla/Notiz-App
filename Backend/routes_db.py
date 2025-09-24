from fastapi import APIRouter, Depends, HTTPException
from pydantic import (
    BaseModel,
)  ## BaseModel = Datenmodell für Requests (Eingaben im Body)

from routes import router

from sqlalchemy.orm import Session
from database import SessionLocal, Note
from datetime import datetime  # 🟢 neu: für aktuelles Datum


class NoteUpdate(BaseModel):  # Schema für Update-Requests
    text: str  # Neuer Text, den wir setzen wollen


"""
APIRouter:
    - Erlaubt, Routen in Gruppen zu organisieren (z. B. alle Notizen-Routen).
    - Macht den Code übersichtlicher, wenn die App größer wird.
Depends:
    - Hilfsmittel von FastAPI für Dependency Injection.
    - Bedeutet: FastAPI führt eine Funktion (z. B. get_db()) automatisch aus
      und gibt das Ergebnis an die Route weiter.
"""

"""
Session:
    - Stammt aus SQLAlchemy.
    - Eine Session ist ein "Arbeitsbereich", in dem man mit der DB arbeitet.
    - Mit einer Session können wir:
        * Objekte (z. B. Notizen) hinzufügen
        * Abfragen an die Datenbank stellen
        * Änderungen speichern (commit)
"""

"""
SessionLocal:
    - Wurde in database.py definiert.
    - Ist eine "Fabrik", die neue Datenbank-Sessions erzeugt.
    - Immer wenn SessionLocal() aufgerufen wird, entsteht eine frische Verbindung zur DB.
Note:
    - Unser Datenbankmodell (entspricht der Tabelle 'notes').
    - Damit können wir neue Notizen anlegen oder bestehende auslesen.
"""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
get_db():
    - Öffnet eine neue Datenbank-Session (db = SessionLocal()).
    - yield db → gibt die Session an die Route weiter,
                 damit dort mit der Datenbank gearbeitet werden kann.
    - finally: db.close() → schließt die Session IMMER,
                auch wenn ein Fehler auftritt.
    - Vorteil: Jede Anfrage bekommt ihre eigene DB-Session,
               die sauber geöffnet und geschlossen wird.
"""


class NoteCreate(BaseModel):  # Definiert das Schema für neue Notizen
    text: str  # Im Body muss ein Feld "text" übergeben werden
    # date brauchen wir hier NICHT im Request, das setzt das Backend automatisch


# Create
@router.post("/notes")  # Definiert die Route POST /notes → neue Notiz anlegen
def create_note_db(
    note: NoteCreate, db: Session = Depends(get_db)
):  # Funktion, erwartet ein NoteCreate-Objekt und eine DB-Session
    new_note = Note(
        text=note.text,
        date=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),  # 🟢 aktuelles Datum automatisch setzen
    )
    db.add(
        new_note
    )  # Fügt das Objekt in die aktuelle DB-Session ein (merkt sich: soll gespeichert werden)
    db.commit()  # Schreibt die Änderung dauerhaft in die Datenbank (führt INSERT aus)
    db.refresh(
        new_note
    )  # Holt die aktualisierten Daten zurück (z. B. die automatisch vergebene ID)
    return {
        "id": new_note.id,
        "text": new_note.text,
        "date": new_note.date,
    }  # 🟢 gibt jetzt auch das Datum zurück


# Read all
@router.get("/notes")  # Definiert die Route GET /notes → alle Notizen abrufen
def get_notes_db(db: Session = Depends(get_db)):  # Funktion: erwartet eine DB-Session
    notes = db.query(Note).all()  # Holt alle Notizen aus der Tabelle "notes"
    return [
        {"id": n.id, "text": n.text, "date": n.date} for n in notes
    ]  # 🟢 gibt auch Datum zurück


# Read one
@router.get("/notes/{note_id}")  # Definiert die Route GET /notes/{id}
def get_note_db(
    note_id: int, db: Session = Depends(get_db)
):  # Funktion: erwartet eine ID + DB-Session
    note = (
        db.query(Note).filter(Note.id == note_id).first()
    )  # Holt die erste Notiz, die zur ID passt
    if note is None:  # Falls keine Notiz mit dieser ID existiert
        raise HTTPException(
            status_code=404, detail="Notiz nicht gefunden"
        )  # Fehler zurückgeben
    return {
        "id": note.id,
        "text": note.text,
        "date": note.date,
    }  # 🟢 gibt auch Datum zurück


# Update
@router.put("/notes/{note_id}")  # Definiert die Route PUT /notes/{id}
def update_note_db(
    note_id: int,  # note_id: Die ID der Notiz, die wir ändern wollen (kommt aus der URL)
    updated_note: NoteUpdate,  # updated_note: Das Pydantic-Modell mit dem neuen Text (kommt aus dem Request-Body)
    db: Session = Depends(
        get_db
    ),  # db: Die Datenbank-Session, die FastAPI automatisch mit get_db() erstellt
):
    note = db.query(Note).filter(Note.id == note_id).first()  # Notiz aus DB holen
    if note is None:  # Falls nicht gefunden
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")

    note.text = updated_note.text  # Text der Notiz ändern
    note.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 🟢 Datum aktualisieren
    db.commit()  # Änderung speichern
    db.refresh(note)  # Neu laden, um aktualisierte Werte zu bekommen

    return {
        "id": note.id,
        "text": note.text,
        "date": note.date,
    }  # 🟢 Geänderte Notiz zurückgeben


# Delete
@router.delete("/notes/{note_id}")  # Route: DELETE /notes/{id}
def delete_note_db(note_id: int, db: Session = Depends(get_db)):
    note = (
        db.query(Note).filter(Note.id == note_id).first()
    )  # Notiz mit passender ID holen
    if note is None:  # Wenn keine Notiz gefunden wurde
        raise HTTPException(
            status_code=404, detail="Notiz nicht gefunden"
        )  # Fehler zurückgeben
    db.delete(note)  # Notiz zum Löschen markieren
    db.commit()  # Änderungen in der DB speichern
    return {"message": f"Notiz mit ID {note.id} wurde gelöscht"}  # Bestätigung als JSON
