# PUE Datenbank - Automatische Excel-Aktualisierung

Ein System zur automatischen Erfassung und Speicherung von PUE-relevanten Gerätedaten aus technischen Datenblättern in einer Excel-Datenbank.

## 📋 Übersicht

Dieses System besteht aus:
1. **Python-Backend** (`pue_data_collector.py`) - Verarbeitet JSON/CSV und aktualisiert Excel
2. **Web-Interface** (`pue_interface.html`) - Einfache Benutzeroberfläche für Dateneingabe
3. **Excel-Datenbank** (`PUE_Datenbank.xlsx`) - Zentrale Datenspeicherung

## 🚀 Installation

### Voraussetzungen
```bash
pip install openpyxl pandas --break-system-packages
```

### Dateien
1. `pue_data_collector.py` - Haupt-Python-Script
2. `pue_interface.html` - Web-Interface (optional)
3. `PUE_Datenbank.xlsx` - Wird automatisch erstellt

## 💻 Verwendung

### Methode 1: Python-Script direkt verwenden

```python
from pue_data_collector import PUEDataCollector

# Initialisierung
collector = PUEDataCollector(
    excel_file='PUE_Datenbank.xlsx',
    sheet_name='Geräte'
)

# JSON-Daten hinzufügen
json_data = '''
[
  {
    "Hersteller": "Schneider Electric",
    "Produktkategorie": "USV",
    "Modellbezeichnung": "Galaxy VS 100kVA",
    ...
  }
]
'''
collector.add_json_data(json_data)

# CSV-Daten hinzufügen
csv_data = '''Hersteller,Produktkategorie,Modellbezeichnung,...
Schneider Electric,USV,Galaxy VS 100kVA,...'''
collector.add_csv_data(csv_data)

# Zusammenfassung anzeigen
summary = collector.get_summary()
print(summary)
```

### Methode 2: Web-Interface verwenden

1. Öffnen Sie `pue_interface.html` in Ihrem Browser
2. Wählen Sie das Datenformat (JSON oder CSV)
3. Fügen Sie die Daten von Ihrem GPT ein
4. Klicken Sie auf "Zu Excel hinzufügen"

### Methode 3: Kommandozeile

```bash
# Script mit Beispieldaten ausführen
python pue_data_collector.py

# Oder eigenes Script erstellen:
python -c "
from pue_data_collector import PUEDataCollector
collector = PUEDataCollector()
collector.add_json_data('YOUR_JSON_DATA_HERE')
"
```

## 📊 Excel-Struktur

Die Excel-Datei enthält folgende Spalten:

| Spalte | Beschreibung |
|--------|--------------|
| Hersteller | Gerätehersteller |
| Produktkategorie | USV, PDU, Chiller, etc. |
| Produktfamilie | Produktlinie/Serie |
| Modellbezeichnung | Genaue Modellnummer |
| Nennleistung | Nennleistung mit Einheit |
| Kühlleistung | Kühlleistung (falls zutreffend) |
| Elektrische Aufnahmeleistung | Stromverbrauch |
| Wirkungsgrad_oder_Verlustleistung | Effizienz |
| COP_EER_IPLV | Leistungszahl |
| Teillast_25% | Teillast bei 25% |
| Teillast_50% | Teillast bei 50% |
| Teillast_75% | Teillast bei 75% |
| Teillast_100% | Teillast bei 100% |
| Betriebsbedingungen | Betriebsparameter |
| Quelle_Dateiname | PDF-Dateiname |
| Quelle_Seitenzahl | Seitenzahl im PDF |
| Quelle_Zitat | Relevantes Zitat |
| Fehlende_Angaben | Liste fehlender Werte |
| Verarbeitungsfehler | Fehler beim Processing |
| Zeitstempel | Zeitpunkt der Erfassung |

## 🔄 Workflow: Integration mit GPT

### Schritt 1: GPT konfigurieren
Ihr GPT ist bereits konfiguriert, um Daten in folgendem Format auszugeben:
- JSON-Format (strukturiert)
- CSV-Format (tabellarisch)

### Schritt 2: Daten erfassen
1. PDF-Datenblatt an Ihren GPT hochladen
2. GPT extrahiert die relevanten Daten
3. GPT gibt JSON und CSV aus

### Schritt 3: Daten speichern

**Option A: Kopieren & Einfügen**
```
1. JSON/CSV von GPT kopieren
2. In Web-Interface oder Python-Script einfügen
3. Automatische Speicherung in Excel
```

**Option B: Automatisierung mit API**
```python
# Wenn Sie die Anthropic API verwenden:
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

# Dokument hochladen und verarbeiten
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{
        "role": "user",
        "content": "Extrahiere PUE-Daten aus diesem Dokument"
    }]
)

# Antwort an Collector senden
collector = PUEDataCollector()
collector.add_json_data(response.content)
```

## 🎯 Beispiel-Workflow

```python
# 1. Initialisierung
from pue_data_collector import PUEDataCollector
collector = PUEDataCollector()

# 2. Daten von GPT (JSON-Format)
gpt_output = '''
[
  {
    "Hersteller": "Schneider Electric",
    "Produktkategorie": "USV",
    "Produktfamilie": "Galaxy VS",
    "Modellbezeichnung": "Galaxy VS 100kVA",
    "Nennleistung": "100 kVA",
    "Kühlleistung": null,
    "Elektrische Aufnahmeleistung": "102 kW",
    "Wirkungsgrad_oder_Verlustleistung": "96.5%",
    "COP_EER_IPLV": null,
    "Teillastdaten": {
      "25%": "97.0%",
      "50%": "97.5%",
      "75%": "97.0%",
      "100%": "96.5%"
    },
    "Betriebsbedingungen": "25°C, 50% Last",
    "Quelle": {
      "Dateiname": "schneider_galaxy_vs.pdf",
      "Seitenzahl": "5",
      "Zitat": "Efficiency at 50% load: 97.5%"
    },
    "Fehlende_Angaben": ["COP_EER_IPLV", "Kühlleistung"],
    "Verarbeitungsfehler": null
  }
]
'''

# 3. Zu Excel hinzufügen
collector.add_json_data(gpt_output)

# 4. Status prüfen
summary = collector.get_summary()
print(f"✓ Datensätze gesamt: {summary['Gesamtanzahl']}")
print(f"✓ Hersteller: {summary['Hersteller']}")
print(f"✓ Letzte Aktualisierung: {summary['Letzte_Aktualisierung']}")
```

## 📈 Erweiterte Funktionen

### Mehrere Geräte gleichzeitig
```python
# JSON mit mehreren Geräten
multi_device_json = '''
[
  {"Hersteller": "Schneider", ...},
  {"Hersteller": "APC", ...},
  {"Hersteller": "Eaton", ...}
]
'''
collector.add_json_data(multi_device_json)
# Alle 3 Geräte werden als separate Zeilen hinzugefügt
```

### Datenbank-Statistiken
```python
summary = collector.get_summary()
# Returns: {
#   'Gesamtanzahl': 150,
#   'Hersteller': 25,
#   'Produktkategorien': 7,
#   'Letzte_Aktualisierung': '2026-02-02 14:30:00'
# }
```

### Batch-Verarbeitung
```python
import os
import json

# Alle JSON-Dateien in einem Ordner verarbeiten
json_folder = '/path/to/json/files'
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        with open(os.path.join(json_folder, filename), 'r') as f:
            data = json.load(f)
            collector.add_json_data(data)
            print(f"✓ {filename} verarbeitet")
```

## 🛠️ Anpassung

### Eigene Excel-Datei
```python
collector = PUEDataCollector(
    excel_file='Meine_Datenbank.xlsx',
    sheet_name='Mein_Sheet'
)
```

### Spalten anpassen
Bearbeiten Sie in `pue_data_collector.py` die `headers` Liste in der `_initialize_excel` Methode.

## ❗ Fehlerbehebung

### Problem: "Datei wird bereits verwendet"
**Lösung:** Schließen Sie die Excel-Datei vor dem Ausführen des Scripts.

### Problem: "Module nicht gefunden"
**Lösung:**
```bash
pip install openpyxl pandas --break-system-packages
```

### Problem: JSON-Parsing-Fehler
**Lösung:** Überprüfen Sie, ob das JSON-Format gültig ist:
```python
import json
json.loads(your_json_string)  # Sollte keinen Fehler werfen
```

### Problem: Daten werden nicht hinzugefügt
**Lösung:** Prüfen Sie:
1. Ist die Excel-Datei geschlossen?
2. Sind die Feldnamen korrekt?
3. Ist das JSON-Format valide?

## 📝 Best Practices

1. **Backup erstellen:** Sichern Sie regelmäßig Ihre Excel-Datei
2. **Konsistente Daten:** Verwenden Sie immer die gleiche Einheitenkonvention
3. **Validierung:** Prüfen Sie die Daten vor dem Hinzufügen
4. **Dokumentation:** Notieren Sie Änderungen am System

## 🔐 Datensicherheit

- Excel-Datei wird lokal gespeichert
- Keine Cloud-Verbindung erforderlich
- Zeitstempel für Audit-Trail
- Quellenangaben für Nachvollziehbarkeit

## 📞 Support

Bei Fragen oder Problemen:
1. Prüfen Sie die Fehlermeldung
2. Konsultieren Sie diese README
3. Überprüfen Sie die JSON/CSV-Formatierung
4. Testen Sie mit den Beispieldaten

## 🎓 Lizenz

Dieses Tool ist für den internen Gebrauch zur Rechenzentrumsplanung entwickelt.

---

**Version:** 1.0  
**Letzte Aktualisierung:** Februar 2026  
**Kompatibilität:** Python 3.8+, Excel 2016+
