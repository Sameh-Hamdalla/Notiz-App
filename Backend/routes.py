# routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# -------------------------
# Datenmodell
# -------------------------
class Note(BaseModel):
    """Definiert eine einzelne Notiz"""
    id: int
    text: str


# -------------------------
# Globale Notizen-Liste
# -------------------------
def get_notes_storage():
    """Initiale Standard-Notizen"""
    return [
        {"id": 1, "text": "Einkaufen gehen"},
        {"id": 2, "text": "Python lernen"},
        {"id": 3, "text": "Backend lernen"}
    ]

notes = get_notes_storage()


# -------------------------
# Routen
# -------------------------

@router.get("/")
def home():
    """Startseite"""
    return {"message": "Hello World"}

@router.get("/about")
def about():
    """Info über die App"""
    return {"message": "Dies ist meine erste kleine Notiz-App 🎉"}

@router.get("/notes")
def get_notes():
    """Gibt alle Notizen zurück"""
    return notes

# Read
@router.get("/notes/{note_id}")
def get_note(note_id: int):
    """Gibt eine einzelne Notiz anhand der ID zurück"""
    for note in notes:
        if note["id"] == note_id:
            return note
    return {"error": "Notiz nicht gefunden"}

# Create
@router.post("/notes")
def create_note(note: Note):
    """Neue Notiz hinzufügen"""
    for n in notes:
        if n["id"] == note.id:
            raise HTTPException(
                status_code=400,
                detail=f"Eine Notiz mit der ID {note.id} existiert schon!"
            )
    notes.append(note.dict())
    return {"message": "Notiz hinzugefügt", "note": note}

@router.post("/reset")
def reset_notes():
    """Setzt die Notizen-Liste zurück"""
    global notes
    notes = get_notes_storage()
    return {"message": "Notizen wurden zurückgesetzt", "notes": notes}

# Delete
@router.delete("/notes/{note_id}")
def delete_note(note_id: int):
    """
    Route: /notes/{note_id}
    -----------------
    Methode: DELETE
    → Diese Route löscht eine Notiz anhand ihrer ID.
    """
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return {"message": f"Notiz mit ID {note_id} wurde gelöscht."}
    return {"error": f"Keine Notiz mit ID {note_id} gefunden."}

# Update
@router.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Note):
    """
    Route: /notes/{note_id} (PUT)
    → Aktualisiert eine bestehende Notiz.
    """
    if updated_note.id != note_id:
        raise HTTPException(
            status_code=400,
            detail="Die ID darf nicht geändert werden."
        )
    for note in notes:
        if note["id"] == note_id:
            note["text"] = updated_note.text
            return {"message": f"Notiz {note_id} wurde aktualisiert.", "note": note}
    raise HTTPException(status_code=404, detail="Notiz nicht gefunden.")

