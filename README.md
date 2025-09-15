# Project-FYN

Projekt zur Entwicklung eines MVP für automatisierte Financial Due Diligence.

## Struktur
- `data/` : Inputdaten (Excel, CSV)
- `notebooks/` : Erste Analysen & Prototypen
- `src/` : Python Skripte (ETL, DB-Loader, Reports)
- `output/` : Generierte Reports

## Setup
1. Repository klonen:
    ```bash
    git clone https://github.com/DEIN-USERNAME/Project-FYN.git
    cd Project-FYN
    python -m venv venv
    venv\Scripts\activate   # Windows
    source venv/bin/activate   # macOS/Linux
    pip install -r requirements.txt