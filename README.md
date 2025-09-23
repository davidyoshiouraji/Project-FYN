# Project-FYN

Projekt zur Entwicklung eines MVP für automatisierte Financial Due Diligence.

## 🚀 Überblick

Dieses Projekt automatisiert die Extraktion und Analyse von Finanzdaten aus verschiedenen Quellen (Excel, PDF, CSV) für Due Diligence Prozesse. Das System verarbeitet Kontodaten, Transaktionen und erstellt standardisierte Reports.

## 📁 Projektstruktur

```
Project-FYN/
├── README.md                    # Diese Datei
├── requirements.txt             # Python Dependencies
├── .gitignore                  # Git Ignore Rules
│
├── src/                        # Quellcode
│   └── data_preprocessing/     # Datenverarbeitung
│       └── account_extractor.py
│
├── data/                       # Daten (nicht in Git)
│   ├── raw/                    # Rohdaten (Excel, CSV, PDF)
│   └── processed/              # Verarbeitete Daten
│
├── notebooks/                  # Jupyter Notebooks
│   └── data_exploration.ipynb  # Datenanalyse & Prototyping
│
├── output/                     # Generierte Reports (nicht in Git)
│
└── tests/                      # Unit Tests
```

## 🛠️ Setup & Installation

### 1. Repository klonen
```bash
git clone https://github.com/DEIN-USERNAME/Project-FYN.git
cd Project-FYN
```

### 2. Virtual Environment erstellen
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux  
python -m venv .venv
source .venv/bin/activate
```

### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 4. Ordnerstruktur vorbereiten
```bash
# Erstelle notwendige Ordner (falls nicht vorhanden)
mkdir -p data/raw data/processed output
```

## 🔧 Verwendung

### Daten hinzufügen
1. Rohdaten in `data/raw/` ablegen
2. Excel-Dateien, CSVs oder PDFs werden automatisch erkannt

### Scripts ausführen
```bash
# Hauptverarbeitung starten
python src/data_preprocessing/account_extractor.py

# Jupyter Notebook für Analyse
jupyter notebook notebooks/data_exploration.ipynb
```

## 📊 Features

- **Automatische Datenextraktion** aus Excel und CSV
- **PDF-Processing** für Kontoauszüge  
- **Datenvalidierung** und -bereinigung
- **Standardisierte Reports** für Due Diligence
- **Jupyter Notebooks** für interaktive Analyse

## 🤝 Entwicklung

### Code hinzufügen
```bash
git add .
git commit -m "Feature: Beschreibung der Änderung"
git push origin main
```

### Tests ausführen
```bash
python -m pytest tests/
```

## 📋 Requirements

- Python 3.8+
- pandas, numpy
- openpyxl (Excel-Support)
- jupyter (Notebooks)
- Weitere siehe `requirements.txt`

## ⚠️ Wichtige Hinweise

- **Daten werden nicht ins Git gepusht** (siehe `.gitignore`)
- Rohdaten lokal in `data/raw/` ablegen
- Sensible Daten nie committen
- `.env` für Umgebungsvariablen nutzen

## 📈 Roadmap

- [ ] PDF-Extraktion implementieren
- [ ] Database Integration
- [ ] Web Interface für Reports  
- [ ] API Endpoints
- [ ] Docker Deployment

---

**Status:** 🚧 In Entwicklung | **Version:** MVP