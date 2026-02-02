from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
excel_file_path = 'data.xlsx'  # The path to the Excel file in the repo

@app.route('/upload', methods=['POST'])
def upload_data():
    # Handle JSON input
    if request.is_json:
        data = request.get_json()
        df = pd.DataFrame(data)
    # Handle CSV input
    elif request.files['file'].filename.endswith('.csv'):
        file = request.files['file']
        df = pd.read_csv(file)
    else:
        return jsonify({"error": "Invalid input format. Please submit JSON or a CSV file."}), 400

    # Load the existing Excel file, or create a new one if it doesn't exist
    if os.path.exists(excel_file_path):
        existing_df = pd.read_excel(excel_file_path)
        df = pd.concat([existing_df, df], ignore_index=True)

    # Save the updated DataFrame to the Excel file
    df.to_excel(excel_file_path, index=False)
    return jsonify({"message": "Data uploaded successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)