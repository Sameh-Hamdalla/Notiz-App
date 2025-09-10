from database import SessionLocal, Note

# ---- Create (INSERT) ----
session = SessionLocal()  # Session starten
new_note = Note(text="Meine erste Notiz")  # Neue Notiz erstellen
session.add(new_note)  # Notiz zur Session hinzufügen
session.commit()  # Änderungen speichern (commit)
session.close()  # Session schließen
print("Notiz gespeichert")

"""
Create (INSERT):
    - Erstellt eine neue Session
    - Fügt ein neues Note-Objekt zur Session hinzu
    - Speichert die Änderung mit commit in der DB
    - Schließt die Session
"""


# ---- Read (SELECT all) ----
session = SessionLocal()
notes = session.query(Note).all()  # holt alle Notizen (Liste von Objekten)

for note in notes:  # durchläuft die Liste
    print(f"{note.id}: {note.text}")

session.close()

"""
Read (SELECT all):
    - Erstellt eine Session
    - Fragt alle Notizen aus der Tabelle ab (.all())
    - Gibt jede Notiz mit ID und Text aus
    - Schließt die Session
"""


# ---- Read (SELECT one) ----
session = SessionLocal()
note = session.query(Note).filter_by(id=1).first()  # eine Notiz holen

if note:
    print(f"Note mit der ID 1: {note.text}")
else:
    print("Keine Notiz mit ID 1 gefunden")

session.close()

"""
Read (SELECT one):
    - Holt mit filter_by(id=1).first() die erste Notiz mit ID=1
    - Gibt den Text der Notiz aus, falls sie existiert
    - Schließt die Session
"""


# ---- Update (UPDATE) ----
session = SessionLocal()
note = session.query(Note).filter_by(id=1).first()  # Notiz mit ID=1 holen

if note:
    note.text = "Geänderter Text"  # Text ändern
    session.commit()  # Änderung speichern
    print("Notiz aktualisiert")
else:
    print("Keine Notiz mit ID 1 gefunden")

session.close()

"""
Update (UPDATE):
    - Holt eine bestimmte Notiz (z. B. ID=1)
    - Ändert den Text dieser Notiz
    - Speichert die Änderung mit commit
    - Schließt die Session
"""


# ---- Delete (DELETE) ----
session = SessionLocal()
note = session.query(Note).filter_by(id=3).first()  # Notiz mit ID=3 holen

if note:
    session.delete(note)  # Notiz löschen
    session.commit()  # Änderung speichern
    print("Notiz gelöscht")
else:
    print("Keine Notiz mit ID 3 gefunden")

session.close()

"""
Delete (DELETE):
    - Holt eine bestimmte Notiz (z. B. ID=3)
    - Löscht diese Notiz mit session.delete()
    - Speichert die Änderung mit commit
    - Schließt die Session
"""

# ---- Alle IDs anzeigen ----
session = SessionLocal()
notes = session.query(Note).all()  # alle Notizen holen

for note in notes:
    print(f"{note.id}: {note.text}")

session.close()

"""
Alle IDs anzeigen:
    - Holt alle Notizen mit .all()
    - Gibt jede ID und den Text aus
    - Praktisch zur Kontrolle, welche Datensätze noch existieren
"""

#Ein Query ist eine Abfrage an die Datenbank
#Bei SELECT one, UPDATE, DELETE  note (Singular) benutzt – weil es nur eine einzelne Notiz ist.

#Bei SELECT all, Alle IDs   notes (Plural) benutzt – weil es eine Liste ist.
