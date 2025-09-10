import { useState } from "react"; 
// React-Hook "useState" importieren → brauchen wir, um State (Zustand) zu speichern

type Note ={
  text: string,
  date: string
}
//Wir legen fest, wie eine Notiz aussieht: sie hat Text und Datum.

function App() {
  const [text, setText] = useState(""); 
  //Hier speichern wir, was gerade im Eingabefeld steht.

  const [notes, setNotes] = useState<Note[]>([]);
  // Hier speichern wir alle Notizen. Am Anfang ist die Liste leer.

  const [editIndex, setEditIndex] = useState<number | null>(null);  
  // editIndex = merkt sich, welche Notiz gerade bearbeitet wird
  // TypeScript: number | null → der Wert kann eine Zahl (Index) oder null sein
  // Startwert = null → bedeutet: keine Notiz wird bearbeitet

  const [searchText, setSearchText] = useState("");
  // merkt sich den aktuellen Text im Suchfeld

  const filteredNotes = notes.filter(note =>
    note.text.toLowerCase().includes(searchText.toLowerCase())
  )

  /**
 * Ablauf:
 * 1. notes.filter(...) → geht durch alle Notizen und baut eine neue Liste.
 * 2. note.text.toLowerCase() → wandelt den Notiz-Text in Kleinbuchstaben um.
 * 3. searchText.toLowerCase() → wandelt den Suchtext auch in Kleinbuchstaben um.
 * 4. includes(...) → prüft, ob der Notiz-Text den Suchtext enthält.
 * 5. Wenn ja (true) → Notiz bleibt in der Liste.
 *    Wenn nein (false) → Notiz wird rausgefiltert.

 */
   // filtert die Notizen je nach Suchtext
  function handleAdd() {
    const newNote : Note ={
      text: text,
      date: new Date().toLocaleString()
    };
    // fügt eine neue Notiz hinzu, Sie nimmt den Text aus dem Input,Hängt das Datum dran,Speichert alles in der Liste notes, Danach wird das Eingabefeld geleert
    setNotes([...notes, newNote]); 
    // neue Liste = alte Notizen + neue Notiz
    setText(""); 
    // Input nach Hinzufügen leeren
  }

  function handleDelete(index: number) {
    // löscht eine Notiz
    setNotes(notes.filter((_, i) => i !== index));
  }

  function handleEdit(index: number) {
    // setzt Input-Feld auf die Notiz mit diesem Index
    setText(notes[index].text);
    // merkt sich, welche Notiz bearbeitet wird
    setEditIndex(index);
  }

  function handleSave() {
    // speichert die Änderung einer Notiz
    if (editIndex !== null) {
      const updatedNotes = [...notes];
      // Kopie der Liste erstellen
      updatedNotes[editIndex] = {
        text: text,
        date: new Date().toLocaleString()
      };
      // Notiz an Position editIndex überschreiben
      setNotes(updatedNotes);

      setText("");     
      // Input-Feld wieder leeren
      setEditIndex(null); 
      // Bearbeitungsmodus beenden
    }
  }

  function handleClearAll() {
    // löscht alle Notizen
    setNotes([]);
  }

  return (
    <div>
      <h1>Notiz-App</h1>

      <input 
        type="text" 
        placeholder="neue Notiz"
        value={text} 
        onChange={(e) => setText(e.target.value)}
      />
      {/* Input-Feld mit State "text" verbunden */}

      {editIndex === null ? (
        <button onClick={handleAdd}>Hinzufügen</button>
        // wenn keine Notiz bearbeitet wird → Hinzufügen
      ) : (
        <button onClick={handleSave}>Speichern</button>
        // wenn editIndex gesetzt ist → Speichern
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
            {notes.map((note, index) => (
              <li key={index}>
                {note.text} – {note.date}
                {/* zeigt Text + Datum der Notiz */}
                <button onClick={() => handleEdit(index)}>Bearbeiten</button>
                {/* setzt Input-Feld auf diese Notiz */}
                <button onClick={() => handleDelete(index)}>Löschen</button>
                {/* löscht diese Notiz */}
              </li>
            ))}
          </ul>

          <button onClick={handleClearAll}>Alle löschen</button>
          {/* Button: leert die gesamte Liste */}
        </div>
      )}
    </div>
  );
}

export default App; 
// macht die Komponente App von außen nutzbar






































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
