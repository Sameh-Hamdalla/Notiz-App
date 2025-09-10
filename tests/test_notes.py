"""
Dieses Skript testet die Home-Route ("/") einer FastAPI/Starlette-Anwendung.
Es wird das Modul unittest verwendet, um automatisch Tests laufen zu lassen.
"""

import sys, os
import unittest
from starlette.testclient import TestClient

"""
sys und os:
  - sys.path.append(): Damit können wir eigene Verzeichnisse zum Python-Pfad hinzufügen.
  - os.path.abspath("Backend"): Wandelt den relativen Pfad "Backend" in einen absoluten Pfad um.

Warum? 
Python muss wissen, wo es die Datei main.py findet, sonst kann man sie nicht importieren.
"""
sys.path.append(os.path.abspath("Backend"))

"""
Jetzt können wir main.py aus dem Ordner Backend importieren.
Dort ist in der Regel die FastAPI-App definiert (app = FastAPI()).
"""
from Backend.main import app

"""
TestClient:
  - Ein Werkzeug von Starlette/FastAPI, um Requests (GET, POST, etc.) 
    an die App zu schicken, so als würde ein echter Browser oder Client 
    sie aufrufen.
"""
client = TestClient(app)


class TestHomeRoute(unittest.TestCase):
    """
    Diese Klasse enthält Unit-Tests für die Route "/".
    unittest.TestCase bedeutet: Jede Methode mit "test_" wird als Test ausgeführt.
    """

    def test_home_route(self):
        """
        Testet die Home-Route ("/"):

        1. client.get("/") → Sendet GET-Anfrage an die Route "/".
        2. response.status_code == 200 → Prüft, ob die Antwort "OK" ist.
        3. response.json() == {"message": "Hello World"} → Prüft, ob der Inhalt genau so ist.
           Wichtig: Es wird ein dict erwartet, nicht ein String!
        """
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})


if __name__ == '__main__':
    """
    Wenn man die Datei direkt ausführt (python test_file.py),
    dann startet unittest.main() und führt alle Tests aus.
    """
    unittest.main()


