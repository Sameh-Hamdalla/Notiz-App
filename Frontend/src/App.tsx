import { useEffect, useState } from "react";
import "./App.css";


// React-Hook "useState" importieren → brauchen wir, um State (Zustand) zu speichern

type Note = {
  id: number,       // id kommt jetzt sicher von der DB
  text: string
}
//Wir legen fest, wie eine Notiz aussieht: sie hat Text und ID (aus DB).

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
      .then((res) => res.json())
      .then(() => {
        loadNotes();  // frisch vom Backend holen
        setText("");  // Eingabefeld leeren
      })
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
  function handleSave() {
    if (editId !== null) {
      const updatedNote = { text: text };

      fetch(`http://127.0.0.1:8000/db/notes/${editId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedNote),
      })
        .then(() => {
          loadNotes();      // neu laden
          setText("");      // Input-Feld leeren
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
