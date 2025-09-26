import { useEffect, useState } from "react";
import "./App.css";


// React-Hook "useState" importieren → brauchen wir, um State (Zustand) zu speichern

type Note = {
  id: number,       // id kommt jetzt sicher von der DB
  text: string,     // Text der Notiz
  date: string      // 🟢 Datum kommt vom Backend
}
//Wir legen fest, wie eine Notiz aussieht: sie hat Text, ID und Datum (aus DB).

function App() {
  const [text, setText] = useState(""); 
  //Hier speichern wir, was gerade im Eingabefeld steht.

  const [notes, setNotes] = useState<Note[]>([]);
  // Hier speichern wir alle Notizen. Am Anfang ist die Liste leer.

  const [editId, setEditId] = useState<number | null>(null);  
  // editId = merkt sich, welche Notiz gerade bearbeitet wird
  // Startwert = null → bedeutet: keine Notiz wird bearbeitet

  const [searchText, setSearchText] = useState("");
  // merkt sich den aktuellen Text im Suchfeld


   // 🟢 Backend-Notizen beim Laden holen
  useEffect(()=>{   //Wenn die App startet, wird useEffect einmal ausgeführt ([]).
    loadNotes();    // eigene Funktion, die alle Notizen holt
  }, []);

  // 🟢 Funktion zum Laden aller Notizen vom Backend (DB)
  function loadNotes() {
    fetch("http://127.0.0.1:8000/db/notes")
      .then((res) => res.json())
      .then((data) => {
        console.log("Daten vom Backend:", data);  // Kontrolle
        setNotes(data);                           // State mit DB-Inhalt füllen
      })
      .catch((err) => console.error("Fehler beim Laden:", err));
  }

  const filteredNotes = notes.filter(note =>
    note.text.toLowerCase().includes(searchText.toLowerCase())
  )

// 🟢 Neue Notiz anlegen
function handleAdd() {
  const newNote = {
    text: text // Inhalt aus dem Eingabefeld
  };

  fetch("http://127.0.0.1:8000/db/notes", {
    method: "POST",                          // POST = neue Daten anlegen
    headers: {
      "Content-Type": "application/json",    // sagt dem Backend: ich schicke JSON
    },
    body: JSON.stringify(newNote),           // Notiz in JSON umwandeln und senden
  })
    // Antwort vom Backend prüfen
    .then(async (res) => {
      // Prüfen: war die Antwort erfolgreich? (Status 200–299)
      if (!res.ok) {
        // Falls Fehler → Text vom Backend holen
        const err = await res.json();

        // Fehler dem Nutzer im Browser anzeigen
        alert("Fehler: " + err.detail);

        // Abbrechen und ins .catch(...) springen
        throw new Error(err.detail);
      }

      // Wenn alles OK → Antwort weitergeben
      return res.json();
    })
    // Wenn es geklappt hat → neu laden + Eingabe leeren
    .then(() => {
      loadNotes();  // frisch vom Backend holen
      setText("");  // Eingabefeld leeren
    })
    // Falls Fehler auftritt → in die Konsole schreiben
    .catch((err) => console.error("Fehler beim Speichern:", err));
}


  // 🟢 Notiz löschen
  function handleDelete(id: number) {
    fetch(`http://127.0.0.1:8000/db/notes/${id}`, {
      method: "DELETE",
    })
      .then(() => loadNotes()) // nach Löschen neu laden
      .catch((err) => console.error("Fehler beim Löschen:", err));
  }

  // 🟢 Notiz zum Bearbeiten auswählen
  function handleEdit(note: Note) {
    setText(note.text);    // setzt Input-Feld auf die Notiz
    setEditId(note.id);    // merkt sich, welche Notiz bearbeitet wird
  }

  // 🟢 Änderung speichern
// 🟢 Änderung speichern
function handleSave() {
  if (editId !== null) {
    const updatedNote = { text: text };

    fetch(`http://127.0.0.1:8000/db/notes/${editId}`, {
      method: "PUT",                          // PUT = bestehende Notiz ändern
      headers: {
        "Content-Type": "application/json",   // wir schicken JSON
      },
      body: JSON.stringify(updatedNote),      // neuen Text als JSON senden
    })
      // Antwort vom Backend prüfen
      .then(async (res) => {
        if (!res.ok) {
          // Falls Fehler → Nachricht vom Backend holen
          const err = await res.json();

          // Nutzer informieren
          alert("Fehler: " + err.detail);

          // Abbrechen und Fehler werfen
          throw new Error(err.detail);
        }

        // Wenn alles OK → JSON zurückgeben
        return res.json();
      })
      // Wenn es geklappt hat → Notizen neu laden
      .then(() => {
        loadNotes();      // frisch laden
        setText("");      // Eingabefeld leeren
        setEditId(null);  // Bearbeitungsmodus beenden
      })
      .catch((err) => console.error("Fehler beim Aktualisieren:", err));
  }
}


  function handleClearAll() {
    // löscht alle Notizen (einzeln durchgehen)
    Promise.all(notes.map(note =>
      fetch(`http://127.0.0.1:8000/db/notes/${note.id}`, { method: "DELETE" })
    ))
    .then(() => loadNotes())
    .catch((err) => console.error("Fehler beim Alles-Löschen:", err));
  }

  return (
    <div>
      <h1>Notiz-App (mit Datenbank)</h1>

      <input 
        type="text" 
        placeholder="neue Notiz"
        value={text} 
        onChange={(e) => setText(e.target.value)}
      />
      {/* Input-Feld mit State "text" verbunden */}

      {editId === null ? (
        <button onClick={handleAdd}>Hinzufügen</button>
        // wenn keine Notiz bearbeitet wird → Hinzufügen
      ) : (
        <button onClick={handleSave}>Speichern</button>
        // wenn editId gesetzt ist → Speichern
      )}

      <p>Du tippst....: {text}</p>
      {/* zeigt live den aktuellen Input-Text */}

      <input
        type="text"
        placeholder="Notizen durchsuchen..."
        value={searchText}
        onChange={(e)=> setSearchText(e.target.value)}  
      />
        {/* Suchfeld → filtert die Liste der Notizen */}

        {filteredNotes.length === 0 ? (
        <p>Keine Notizen vorhanden.</p>
        // Hinweis: wenn Liste leer oder keine Notiz zur Suche passt
      ) : (
        <div>
            <ul>
              {filteredNotes.map((note) => (
                <li key={note.id} className="note-item">
                  <span className="note-text">{note.text}</span>
                  {/* 🟢 Neues Datum-Feld anzeigen */}
                  <span className="note-date">
                  {new Date(note.date).toLocaleString("de-DE")}
                  </span>
                  <div className="actions">
                    <button className="edit" onClick={() => handleEdit(note)}>Bearbeiten</button>
                    <button className="delete" onClick={() => handleDelete(note.id!)}>Löschen</button>
                  </div>
                </li>
              ))}
            </ul>

          {/* 🟠 Button jetzt mit eigener Klasse "clear" */}
          <button className="clear-all" onClick={handleClearAll}>Alle löschen</button>
          {/* Button: leert die gesamte Liste */}
        </div>
      )}
    </div>
  );
}

export default App;




// macht die Komponente App von außen nutzbar








// ..\.venv\Scripts\Activate.ps1
//uvicorn main:app --reload
































// import { useState } from "react";

// function App() {
//   const [count, setCount] = useState(0); // State für die Zahl

//   return (
//     <div>
//       <h1>Zähler: {count}</h1>
//       <button onClick={() => setCount(count + 1)}>+1</button>
//       <button onClick={() => setCount(count - 1)}>-1</button>
//     </div>
//   );
// }

// export default App;
