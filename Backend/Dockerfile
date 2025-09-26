# 🟢 Basis-Image mit Python
FROM python:3.11-slim

# 🟢 Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# 🟢 requirements installieren (falls du eine requirements.txt hast)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🟢 Restlichen Code ins Image kopieren
COPY . .

# 🟢 Uvicorn starten (Server)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
