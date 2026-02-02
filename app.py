#!/usr/bin/env python3
"""
Flask Web Application for PUE Data Collection
Provides REST API and web interface for adding data to Excel
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from pue_data_collector import PUEDataCollector
import json
from datetime import datetime

app = Flask(__name__)
collector = PUEDataCollector()

# HTML Template (embedded for simplicity)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PUE Datenbank - Dateneingabe</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #366092 0%, #2c4d75 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        .main-content {
            padding: 30px;
        }
        .format-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .format-btn {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }
        .format-btn:hover {
            border-color: #667eea;
            background: #f8f9ff;
        }
        .format-btn.active {
            border-color: #667eea;
            background: #667eea;
            color: white;
        }
        textarea {
            width: 100%;
            min-height: 300px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            resize: vertical;
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }
        .btn {
            flex: 1;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        .status-box {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        .status-box.success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .status-box.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-card h3 {
            font-size: 32px;
            color: #366092;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 PUE Datenbank</h1>
            <p>Rechenzentrum Geräte-Datenbank | Automatische Excel-Aktualisierung</p>
        </div>
        <div class="main-content">
            <div class="format-selector">
                <button class="format-btn active" onclick="selectFormat('json')">JSON</button>
                <button class="format-btn" onclick="selectFormat('csv')">CSV</button>
            </div>
            <textarea id="dataInput" placeholder="Fügen Sie hier Ihre JSON oder CSV Daten ein..."></textarea>
            <div class="button-group">
                <button class="btn btn-primary" onclick="submitData()">✓ Zu Excel hinzufügen</button>
                <button class="btn btn-secondary" onclick="clearInput()">✕ Leeren</button>
                <button class="btn btn-secondary" onclick="downloadExcel()">📥 Excel herunterladen</button>
            </div>
            <div id="statusBox" class="status-box"></div>
            <div class="stats-grid" id="statsGrid" style="display: none;">
                <div class="stat-card">
                    <h3 id="totalRecords">0</h3>
                    <p>Gesamtanzahl Datensätze</p>
                </div>
                <div class="stat-card">
                    <h3 id="totalManufacturers">0</h3>
                    <p>Hersteller</p>
                </div>
                <div class="stat-card">
                    <h3 id="totalCategories">0</h3>
                    <p>Produktkategorien</p>
                </div>
                <div class="stat-card">
                    <h3 id="lastUpdate">-</h3>
                    <p>Letzte Aktualisierung</p>
                </div>
            </div>
        </div>
    </div>
    <script>
        let currentFormat = 'json';
        
        function selectFormat(format) {
            currentFormat = format;
            document.querySelectorAll('.format-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }
        
        async function submitData() {
            const data = document.getElementById('dataInput').value.trim();
            if (!data) {
                showStatus('Bitte geben Sie Daten ein!', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        data: data,
                        format: currentFormat
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showStatus(result.message, 'success');
                    updateStats();
                    setTimeout(() => clearInput(), 2000);
                } else {
                    showStatus(result.message, 'error');
                }
            } catch (error) {
                showStatus('Fehler beim Speichern: ' + error.message, 'error');
            }
        }
        
        function clearInput() {
            document.getElementById('dataInput').value = '';
            document.getElementById('statusBox').style.display = 'none';
        }
        
        function showStatus(message, type) {
            const statusBox = document.getElementById('statusBox');
            statusBox.className = `status-box ${type}`;
            statusBox.textContent = message;
            statusBox.style.display = 'block';
        }
        
        async function updateStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('totalRecords').textContent = stats.Gesamtanzahl;
                document.getElementById('totalManufacturers').textContent = stats.Hersteller;
                document.getElementById('totalCategories').textContent = stats.Produktkategorien;
                document.getElementById('lastUpdate').textContent = stats.Letzte_Aktualisierung || '-';
                document.getElementById('statsGrid').style.display = 'grid';
            } catch (error) {
                console.error('Fehler beim Laden der Statistiken:', error);
            }
        }
        
        function downloadExcel() {
            window.location.href = '/api/download';
        }
        
        // Load stats on page load
        updateStats();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/add', methods=['POST'])
def add_data():
    """API endpoint to add data to Excel"""
    try:
        request_data = request.get_json()
        data = request_data.get('data')
        format_type = request_data.get('format', 'json')
        
        if not data:
            return jsonify({'success': False, 'message': 'Keine Daten empfangen'}), 400
        
        # Add data based on format
        if format_type == 'json':
            success = collector.add_json_data(data)
        elif format_type == 'csv':
            success = collector.add_csv_data(data)
        else:
            return jsonify({'success': False, 'message': 'Ungültiges Format'}), 400
        
        if success:
            return jsonify({
                'success': True,
                'message': '✓ Daten erfolgreich zur Excel-Datei hinzugefügt!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Fehler beim Hinzufügen der Daten'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Fehler: {str(e)}'
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API endpoint to get database statistics"""
    try:
        summary = collector.get_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({
            'Gesamtanzahl': 0,
            'Hersteller': 0,
            'Produktkategorien': 0,
            'Letzte_Aktualisierung': None,
            'error': str(e)
        })

@app.route('/api/download', methods=['GET'])
def download_excel():
    """API endpoint to download the Excel file"""
    try:
        return send_file(
            collector.excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'PUE_Datenbank_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("PUE Datenbank Server gestartet!")
    print("="*60)
    print("Öffnen Sie Ihren Browser und navigieren Sie zu:")
    print("  http://localhost:5000")
    print()
    print("API Endpoints:")
    print("  POST /api/add     - Daten hinzufügen")
    print("  GET  /api/stats   - Statistiken abrufen")
    print("  GET  /api/download - Excel herunterladen")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
