from starlette.middleware.cors import CORSMiddleware

# Middleware = eine Art „Zwischenschicht“, die bei jeder Anfrage automatisch läuft,
#bevor die Anfrage in die Routen (z. B. /notes) reingeht.

def setup_cors(app):
    """
    Fügt CORS-Middleware zur App hinzu.
    CORS = Cross-Origin Resource Sharing.
    Damit kann unser Frontend (z. B. React oder HTML/JS)
    mit dem Backend sprechen, auch wenn es auf einer anderen Domain/Port läuft.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],       ## "*" = alle Domains erlaubt (z. B. localhost:3000, google.com ...)
        allow_credentials=True,    ## erlaubt Cookies / Authentifizierung mitzuschicken
        allow_methods=["*"],       ## erlaubt alle HTTP-Methoden (GET, POST, PUT, DELETE usw.)
        allow_headers=["*"],       ## erlaubt alle Header (z. B. Content-Type, Authorization)

    )
