# 🚀 Quick Start Guide - PUE Datenbank

## Schnellstart in 3 Schritten

### 1️⃣ Installation (einmalig)
```bash
# Python-Pakete installieren
pip install flask openpyxl pandas --break-system-packages
```

### 2️⃣ Server starten
```bash
# Im Projektordner ausführen
python app.py
```

Sie sollten folgende Ausgabe sehen:
```
============================================================
PUE Datenbank Server gestartet!
============================================================
Öffnen Sie Ihren Browser und navigieren Sie zu:
  http://localhost:5000
============================================================
```

### 3️⃣ Browser öffnen
Öffnen Sie: `http://localhost:5000`

---

## 📝 Verwendung

### Workflow mit Ihrem GPT

```
1. PDF-Datenblatt an Ihren GPT senden
   ↓
2. GPT extrahiert Daten und gibt JSON aus
   ↓
3. JSON kopieren
   ↓
4. In Web-Interface einfügen (http://localhost:5000)
   ↓
5. "Zu Excel hinzufügen" klicken
   ↓
6. ✓ Fertig! Daten sind in PUE_Datenbank.xlsx
```

### Beispiel JSON von Ihrem GPT

```json
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
```

---

## 🎯 Alternative: Ohne Web-Interface

### Python-Script direkt verwenden

```python
from pue_data_collector import PUEDataCollector

# Collector initialisieren
collector = PUEDataCollector()

# JSON von GPT einfügen
json_data = '''[{"Hersteller": "...", ...}]'''

# Zu Excel hinzufügen
collector.add_json_data(json_data)

# Fertig!
```

Speichern Sie als `add_data.py` und führen Sie aus:
```bash
python add_data.py
```

---

## 📊 Excel-Datei finden

Nach dem ersten Eintrag wird automatisch erstellt:
- **Dateiname:** `PUE_Datenbank.xlsx`
- **Ort:** Im gleichen Ordner wie die Python-Dateien

Die Datei wird **automatisch aktualisiert** jedes Mal wenn Sie neue Daten hinzufügen!

---

## ⚡ Tipps & Tricks

### ✅ DO's
- Schließen Sie Excel vor dem Hinzufügen neuer Daten
- Validieren Sie JSON im Web-Interface vor dem Senden
- Erstellen Sie regelmäßig Backups der Excel-Datei
- Verwenden Sie konsistente Einheiten

### ❌ DON'Ts
- Nicht manuell in Excel bearbeiten während Server läuft
- Nicht mehrere Instanzen des Servers gleichzeitig starten
- Nicht die Spaltenreihenfolge in Excel manuell ändern

---

## 🔧 Fehlerbehebung

### Problem: Port 5000 bereits belegt
```bash
# Anderen Port verwenden
# In app.py ändern: app.run(port=5001)
```

### Problem: Excel-Datei kann nicht geöffnet werden
```bash
# Schließen Sie alle Excel-Instanzen und versuchen Sie erneut
```

### Problem: JSON-Fehler
```bash
# Prüfen Sie das JSON-Format online: https://jsonlint.com/
```

---

## 📞 Häufige Fragen (FAQ)

**Q: Kann ich mehrere Geräte gleichzeitig hinzufügen?**  
A: Ja! Ihr GPT kann ein JSON-Array mit mehreren Geräten ausgeben.

**Q: Werden alte Daten überschrieben?**  
A: Nein! Neue Daten werden immer als neue Zeilen **hinzugefügt**.

**Q: Kann ich die Excel-Datei umbenennen?**  
A: Ja, aber passen Sie den Dateinamen in `app.py` oder beim Initialisieren an:
```python
collector = PUEDataCollector(excel_file='MeineDatei.xlsx')
```

**Q: Funktioniert das auch ohne Internet?**  
A: Ja! Alles läuft lokal auf Ihrem Computer.

**Q: Wie exportiere ich die Daten?**  
A: Die Excel-Datei ist bereits fertig formatiert. Öffnen Sie einfach `PUE_Datenbank.xlsx`.

---

## 🎓 Nächste Schritte

1. ✅ Server starten
2. ✅ Erstes Gerät hinzufügen
3. ✅ Excel-Datei prüfen
4. 🚀 Weitere Datenblätter verarbeiten
5. 📊 Datenbank aufbauen

---

**Happy Data Collecting! 🎉**
