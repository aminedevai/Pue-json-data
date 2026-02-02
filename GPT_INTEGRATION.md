# 🤖 GPT Integration Guide

## Übersicht

Diese Anleitung erklärt, wie Sie Ihren konfigurierten GPT mit der PUE Excel-Datenbank verbinden.

---

## 🔄 Workflow-Übersicht

```
┌─────────────────┐
│  PDF-Datenblatt │
│   hochladen     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   GPT extrahiert│
│   PUE-Daten     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ JSON/CSV Output │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Web-Interface   │
│ oder Python     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Excel-Datenbank │
│  aktualisiert   │
└─────────────────┘
```

---

## 🎯 Methode 1: Manuelle Verarbeitung (Einfach)

### Schritt für Schritt

#### 1. Server starten
```bash
cd /pfad/zu/projekt
python app.py
```

#### 2. Browser öffnen
Gehen Sie zu: `http://localhost:5000`

#### 3. GPT verwenden
1. Öffnen Sie Ihren GPT in einer anderen Browser-Tab
2. Laden Sie ein PDF-Datenblatt hoch
3. Warten Sie auf die Ausgabe (JSON und CSV)

#### 4. Daten kopieren
Der GPT gibt Ihnen drei Ausgaben:
- **Checkliste** (überspringen)
- **JSON** ← Das brauchen wir!
- **CSV** (Alternative)
- **Zusammenfassung** (überspringen)

Kopieren Sie den kompletten JSON-Block, z.B.:
```json
[
  {
    "Hersteller": "Schneider Electric",
    "Produktkategorie": "USV",
    ...
  }
]
```

#### 5. Einfügen und Speichern
1. Wechseln Sie zurück zum Web-Interface (`http://localhost:5000`)
2. Stellen Sie sicher, dass "JSON" ausgewählt ist
3. Fügen Sie das JSON ein
4. Klicken Sie "Zu Excel hinzufügen"
5. ✓ Fertig!

#### 6. Excel prüfen
Öffnen Sie `PUE_Datenbank.xlsx` - Ihre Daten sind drin!

---

## 🚀 Methode 2: API-Integration (Fortgeschritten)

Falls Sie die Anthropic API direkt verwenden, können Sie den Prozess automatisieren:

### Python-Script für vollständige Automatisierung

```python
#!/usr/bin/env python3
"""
Vollautomatische PUE-Datenextraktion und Speicherung
"""

import anthropic
import base64
import json
import re
from pue_data_collector import PUEDataCollector

# Konfiguration
ANTHROPIC_API_KEY = "your-api-key-here"  # Ihre API Key
PDF_PATH = "datenblatt.pdf"               # Pfad zum PDF

def extract_pue_data_from_pdf(pdf_path):
    """Extrahiert PUE-Daten aus PDF via Claude API"""
    
    # PDF zu Base64 konvertieren
    with open(pdf_path, 'rb') as f:
        pdf_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Claude API Client
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # GPT-Instruktion laden (Ihre Konfiguration)
    with open('gpt_instructions.txt', 'r', encoding='utf-8') as f:
        instructions = f.read()
    
    # API Request
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    },
                    {
                        "type": "text",
                        "text": "Extrahiere die PUE-relevanten Daten aus diesem Dokument."
                    }
                ]
            }
        ],
        system=instructions
    )
    
    # Response verarbeiten
    response_text = message.content[0].text
    
    # JSON extrahieren (zwischen JSON-Markern)
    json_match = re.search(r'\[[\s\S]*?\]', response_text)
    if json_match:
        return json_match.group(0)
    
    return None

def main():
    """Hauptprozess"""
    print("🚀 Starte automatische PUE-Datenextraktion...")
    
    # Schritt 1: Daten aus PDF extrahieren
    print(f"📄 Verarbeite PDF: {PDF_PATH}")
    json_data = extract_pue_data_from_pdf(PDF_PATH)
    
    if not json_data:
        print("❌ Fehler: Keine Daten extrahiert")
        return
    
    print("✓ Daten erfolgreich extrahiert")
    
    # Schritt 2: Zu Excel hinzufügen
    print("💾 Füge Daten zu Excel hinzu...")
    collector = PUEDataCollector()
    
    if collector.add_json_data(json_data):
        print("✓ Erfolgreich zu Excel hinzugefügt!")
        
        # Statistik anzeigen
        summary = collector.get_summary()
        print(f"\n📊 Datenbank-Status:")
        print(f"   Gesamtanzahl: {summary['Gesamtanzahl']}")
        print(f"   Hersteller: {summary['Hersteller']}")
        print(f"   Kategorien: {summary['Produktkategorien']}")
    else:
        print("❌ Fehler beim Hinzufügen zu Excel")

if __name__ == "__main__":
    main()
```

### Verwendung

```bash
# 1. API Key setzen (im Script oder als Umgebungsvariable)
export ANTHROPIC_API_KEY="your-key-here"

# 2. PDF-Pfad anpassen
# In Script: PDF_PATH = "ihr_datenblatt.pdf"

# 3. Ausführen
python auto_extract.py
```

---

## 📦 Batch-Verarbeitung

Mehrere PDFs auf einmal verarbeiten:

```python
import os
from pathlib import Path

pdf_folder = "/pfad/zu/pdfs"
collector = PUEDataCollector()

for pdf_file in Path(pdf_folder).glob("*.pdf"):
    print(f"Verarbeite: {pdf_file.name}")
    
    # Daten extrahieren (mit API oder GPT)
    json_data = extract_pue_data_from_pdf(str(pdf_file))
    
    # Zu Excel hinzufügen
    if json_data:
        collector.add_json_data(json_data)
        print(f"✓ {pdf_file.name} fertig")
    else:
        print(f"✗ {pdf_file.name} fehlgeschlagen")

print("\n🎉 Alle PDFs verarbeitet!")
summary = collector.get_summary()
print(f"Gesamtanzahl: {summary['Gesamtanzahl']} Geräte")
```

---

## 🔧 Erweiterte Konfiguration

### Custom Excel-Vorlage verwenden

```python
# Eigene Excel-Vorlage mit speziellen Formeln/Formatierungen
collector = PUEDataCollector(
    excel_file='Meine_Vorlage.xlsx',
    sheet_name='Geräteliste'
)
```

### Datenvalidierung hinzufügen

```python
def validate_json(json_data):
    """Validiert JSON vor dem Speichern"""
    data = json.loads(json_data)
    
    for record in data:
        # Pflichtfelder prüfen
        required_fields = ['Hersteller', 'Produktkategorie', 'Modellbezeichnung']
        for field in required_fields:
            if not record.get(field):
                raise ValueError(f"Fehlendes Pflichtfeld: {field}")
        
        # Einheiten prüfen
        if record.get('Nennleistung'):
            if not any(unit in record['Nennleistung'] for unit in ['kW', 'kVA', 'W']):
                raise ValueError("Nennleistung muss Einheit enthalten")
    
    return True

# Verwendung
try:
    validate_json(json_from_gpt)
    collector.add_json_data(json_from_gpt)
except ValueError as e:
    print(f"Validierungsfehler: {e}")
```

---

## 🎛️ GPT-Konfiguration optimieren

### Empfohlene Anpassungen für bessere Integration

1. **Konsistente Ausgabe erzwingen:**
   Fügen Sie zu Ihrer GPT-Instruktion hinzu:
   ```
   WICHTIG: Gib das JSON IMMER zwischen diesen Markern aus:
   
   ===JSON_START===
   [...]
   ===JSON_END===
   ```

2. **Fehlerbehandlung verbessern:**
   ```
   Falls keine Daten extrahierbar sind, gib folgendes JSON aus:
   [{
     "Hersteller": null,
     "Verarbeitungsfehler": "Beschreibung des Problems"
   }]
   ```

3. **Einheiten standardisieren:**
   ```
   Alle Leistungsangaben in kW konvertieren.
   Alle Effizienzangaben als Prozent (z.B. "96.5%").
   ```

---

## 📊 Dashboard erstellen (Optional)

Erweitern Sie `app.py` für ein Dashboard:

```python
@app.route('/dashboard')
def dashboard():
    df = pd.read_excel(collector.excel_file)
    
    # Statistiken berechnen
    stats = {
        'total': len(df),
        'by_category': df['Produktkategorie'].value_counts().to_dict(),
        'by_manufacturer': df['Hersteller'].value_counts().to_dict(),
        'avg_efficiency': df['Wirkungsgrad_oder_Verlustleistung'].mean()
    }
    
    return render_template('dashboard.html', stats=stats)
```

---

## 🔐 Best Practices

### Sicherheit
- ✅ API Keys niemals im Code speichern
- ✅ Verwenden Sie Umgebungsvariablen
- ✅ `.gitignore` für Excel-Dateien

### Datenqualität
- ✅ Validieren Sie JSON vor dem Speichern
- ✅ Prüfen Sie Einheiten-Konsistenz
- ✅ Backup vor großen Batch-Jobs

### Performance
- ✅ Batch-Verarbeitung für viele PDFs
- ✅ Rate Limiting bei API-Nutzung
- ✅ Caching für wiederholte Anfragen

---

## 🆘 Troubleshooting

### Problem: GPT gibt kein valides JSON aus
**Lösung:** 
```python
# Funktion zum "Reparieren" von JSON
def fix_json(text):
    # Extrahiere JSON-Teil
    json_match = re.search(r'\[[\s\S]*?\]', text)
    if json_match:
        return json_match.group(0)
    return None

json_data = fix_json(gpt_output)
```

### Problem: Zu viele API-Anfragen
**Lösung:**
```python
import time

for pdf in pdf_list:
    process_pdf(pdf)
    time.sleep(2)  # 2 Sekunden Pause zwischen Anfragen
```

### Problem: Excel-Datei zu groß
**Lösung:**
```python
# Daten in mehrere Excel-Dateien aufteilen
# oder
# Alte Daten in Archiv verschieben
```

---

## 📞 Support

Bei Fragen zur Integration:
1. Prüfen Sie die Logs in der Konsole
2. Validieren Sie JSON auf jsonlint.com
3. Testen Sie mit den Beispieldaten
4. Prüfen Sie API-Limits

---

**Viel Erfolg mit Ihrer automatisierten PUE-Datenbank! 🎉**
