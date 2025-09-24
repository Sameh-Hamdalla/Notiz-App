from sqlalchemy import create_engine, Column, Integer, String

"""
Imports aus SQLAlchemy für die Datenbankarbeit
create_engine:
    - Stellt die Verbindung zur Datenbank her z.B SQLite oder MySQL
Column:
    - Definiert eine Spalte in einer Tabelle ,Beispiel: id, text
Integer:
    - Spaltentyp für Ganzzahlen , Beispiel: 1, 2, 3
String:
    - Spaltentyp für Texte   - Beispiel: "Hallo", "Notiz"
"""
from sqlalchemy.orm import declarative_base

"""
declarative_base:
    - Erzeugt eine "Basisklasse" für alle Datenbankmodelle.
    - Jede Tabelle in der Datenbank wird als Klasse definiert,
      die von dieser Basisklasse erbt.
    - Beispiel:
        Base = declarative_base()
        class Note(Base):
            __tablename__ = "notes"
            id = Column(Integer, primary_key=True)
"""
from sqlalchemy.orm import sessionmaker

"""
sessionmaker:
    - Erzeugt eine Fabrikfunktion (Session-Klasse),
      die mit der Datenbank verbunden wird.
    - Eine Session ist wie ein "Arbeitsbereich",
      in dem Objekte (z.B. Notizen) hinzugefügt,
      geändert oder abgefragt werden.
    - Man braucht eine Session, um mit der Datenbank zu arbeiten
      (ähnlich wie ein "Cursor" in SQL).
    - Beispiel:
        Session = sessionmaker(bind=engine)
        session = Session()
"""

DATABASE_URL = "sqlite:///./notes.db"
# sqlite://=> das sagt Wir benutzen den SQLite Dialekt, das dritte / =>Pfadangabe für eine lokale Datei
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
"""
engine: Verbindung zur Datenbank, kümmert sich um die Kommunikation zwischen SQLAlchemy und SQLite
        connect_args={"check_same_thread": False} ist bei SQLite nötig,
        um parallele Zugriffe zu erlauben
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
SessionLocal:
    - Session-Fabrik, erzeugt Sitzungen für die Datenbankarbeit
    - autocommit=False -> speichert Änderungen nicht automatisch
    - autoflush=False  -> schreibt Daten nicht automatisch in die DB
"""

Base = declarative_base()
"""
Base:
    - Basisklasse für alle Models (Tabellen)
    - alle Tabellen-Klassen erben von dieser Base
"""


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)  # 🟢 Text-Spalte für den Notizinhalt
    date = Column(String, nullable=True)  # 🟢 neues Feld für Datum


"""
Note (Model):
    - Repräsentiert die Tabelle "notes" in der Datenbank
    - id:    Ganzzahl, Primärschlüssel (eindeutig)
    - text:  Textfeld für die eigentliche Notiz
    - date:  Datum/Uhrzeit als String (optional)
"""

Base.metadata.create_all(engine)
"""
Base.metadata.create_all(bind=engine):
    - Sagt SQLAlchemy: "Erstelle alle Tabellen, die auf Base basieren."
    - Falls notes.db noch nicht existiert -> wird automatisch erzeugt
    - Falls die Datei existiert, aber Tabelle fehlt -> wird hinzugefügt
"""
